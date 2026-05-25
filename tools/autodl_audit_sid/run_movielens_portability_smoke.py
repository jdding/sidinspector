"""Run a bounded non-Amazon SIDInspector portability smoke on MovieLens."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import pandas as pd

from audit_sid.adapters.sanity import category_prefix_sid, mod_collision_sid, popularity_balanced_sid
from audit_sid.metrics import alignment, collision, deployment_cost, head_tail_capacity, utilization, validate_inputs


def _read_zip_csv(zip_path: Path, member: str, **kwargs) -> pd.DataFrame:
    with zipfile.ZipFile(zip_path) as archive:
        with archive.open(member) as handle:
            return pd.read_csv(handle, **kwargs)


def _read_ratings_prefix(zip_path: Path, max_ratings: int) -> pd.DataFrame:
    chunks = []
    seen = 0
    with zipfile.ZipFile(zip_path) as archive:
        with archive.open("ml-25m/ratings.csv") as handle:
            for chunk in pd.read_csv(handle, chunksize=250_000):
                remaining = max_ratings - seen
                if remaining <= 0:
                    break
                if len(chunk) > remaining:
                    chunk = chunk.head(remaining)
                chunks.append(chunk[["userId", "movieId", "timestamp"]])
                seen += len(chunk)
    if not chunks:
        raise ValueError("No ratings rows were read")
    return pd.concat(chunks, ignore_index=True)


def _genre_maps(movies: pd.DataFrame) -> tuple[dict[str, int], dict[int, str]]:
    genres = sorted(
        {
            genre
            for value in movies["genres"].fillna("(no genres listed)")
            for genre in str(value).split("|")
            if genre
        }
    )
    genre_to_id = {genre: idx + 1 for idx, genre in enumerate(genres)}
    id_to_genre = {idx: genre for genre, idx in genre_to_id.items()}
    return genre_to_id, id_to_genre


def _primary_genre(value: object) -> str:
    parts = [part for part in str(value).split("|") if part]
    return parts[0] if parts else "(no genres listed)"


def build_inputs(zip_path: Path, output_dir: Path, max_ratings: int, max_items: int, dataset_name: str) -> tuple[Path, Path, Path]:
    movies = _read_zip_csv(zip_path, "ml-25m/movies.csv")
    ratings = _read_ratings_prefix(zip_path, max_ratings=max_ratings)
    selected_items = sorted(ratings["movieId"].drop_duplicates().astype(int).head(max_items).tolist())
    selected_set = set(selected_items)
    ratings = ratings[ratings["movieId"].astype(int).isin(selected_set)].copy()
    movies = movies[movies["movieId"].astype(int).isin(selected_set)].copy()
    missing_movies = selected_set - set(movies["movieId"].astype(int))
    if missing_movies:
        raise ValueError(f"ratings reference movies missing metadata: {len(missing_movies)}")

    genre_to_id, id_to_genre = _genre_maps(movies)
    movies["primary_genre"] = movies["genres"].map(_primary_genre)
    movies["category_l1"] = movies["primary_genre"].map(genre_to_id).astype(int)
    movies["category_l2"] = movies["category_l1"]
    movies["category_l3"] = movies["category_l1"]
    item_metadata = pd.DataFrame(
        {
            "dataset": dataset_name,
            "item_id": movies["movieId"].astype(int),
            "category": movies["primary_genre"].astype(str),
            "category_l1": movies["category_l1"],
            "category_l2": movies["category_l2"],
            "category_l3": movies["category_l3"],
            "title": movies["title"].astype(str),
        }
    ).sort_values("item_id")
    interactions = pd.DataFrame(
        {
            "dataset": dataset_name,
            "user_id": ratings["userId"].astype(int),
            "item_id": ratings["movieId"].astype(int),
            "split": "train",
            "timestamp": ratings["timestamp"].astype(int),
        }
    )

    input_dir = output_dir / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    item_metadata_path = input_dir / "item_metadata.parquet"
    interactions_path = input_dir / "interactions.parquet"
    item_metadata.to_parquet(item_metadata_path, index=False)
    interactions.to_parquet(interactions_path, index=False)
    (input_dir / "genre_map.json").write_text(json.dumps(id_to_genre, indent=2, sort_keys=True), encoding="utf-8")
    return item_metadata_path, interactions_path, input_dir / "genre_map.json"


def run_metrics(item_metadata_path: Path, interactions_path: Path, output_dir: Path, dataset_name: str) -> Path:
    item_metadata = pd.read_parquet(item_metadata_path)
    interactions = pd.read_parquet(interactions_path)
    sid = pd.concat(
        [
            mod_collision_sid(item_metadata, dataset_name, width=256, levels=4),
            category_prefix_sid(item_metadata, dataset_name),
            popularity_balanced_sid(item_metadata, interactions, dataset_name, width=256),
        ],
        ignore_index=True,
    )
    sid_dir = output_dir / "sanity"
    metrics_dir = output_dir / "metrics"
    sid_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)
    sid_path = sid_dir / "sid_assignments.parquet"
    sid.to_parquet(sid_path, index=False)
    tables = {
        "coverage_report.csv": validate_inputs(sid, item_metadata, interactions),
        "d1_utilization.csv": utilization(sid),
        "d2_collision.csv": collision(sid, interactions),
        "d3_alignment.csv": alignment(sid, item_metadata, interactions, max_pair_events=250_000),
        "d4_head_tail.csv": head_tail_capacity(sid, interactions),
        "d5a_deployment_cost.csv": deployment_cost(sid),
    }
    for name, table in tables.items():
        table.to_csv(metrics_dir / name, index=False)
    return sid_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Bounded MovieLens portability smoke for SIDInspector.")
    parser.add_argument("--zip-path", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="MovieLens_25M_smoke")
    parser.add_argument("--max-ratings", type=int, default=1_000_000)
    parser.add_argument("--max-items", type=int, default=10_000)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    item_metadata_path, interactions_path, genre_map_path = build_inputs(
        args.zip_path,
        args.output_dir,
        max_ratings=args.max_ratings,
        max_items=args.max_items,
        dataset_name=args.dataset_name,
    )
    sid_path = run_metrics(item_metadata_path, interactions_path, args.output_dir, args.dataset_name)
    print(
        json.dumps(
            {
                "dataset": args.dataset_name,
                "item_metadata": str(item_metadata_path),
                "interactions": str(interactions_path),
                "genre_map": str(genre_map_path),
                "sid_assignments": str(sid_path),
                "metrics": str(args.output_dir / "metrics"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
