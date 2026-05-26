"""Stable input contracts for SIDInspector adapters.

Adapters for ReSID, GRID, CARD, or sanity baselines should emit tables that
match these contracts before diagnostic metrics run.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


SID_ASSIGNMENTS_REQUIRED: tuple[str, ...] = (
    "item_id",
    "sid",
    "method",
    "dataset",
)

ITEM_METADATA_REQUIRED: tuple[str, ...] = ("item_id",)

INTERACTIONS_REQUIRED: tuple[str, ...] = (
    "user_id",
    "item_id",
)

GENERATOR_OUTPUTS_REQUIRED: tuple[str, ...] = (
    "user_id",
    "rank",
    "item_id",
)


@dataclass(frozen=True)
class TableContract:
    """Column contract for one toolkit input table."""

    name: str
    required_columns: tuple[str, ...]
    optional_columns: tuple[str, ...] = ()


@dataclass(frozen=True)
class AuditSidTables:
    """Filesystem paths for a normalized SIDInspector artifact bundle."""

    sid_assignments: Path
    item_metadata: Path
    interactions: Path
    generator_outputs: Path | None = None


CONTRACTS: Mapping[str, TableContract] = {
    "sid_assignments": TableContract(
        name="sid_assignments",
        required_columns=SID_ASSIGNMENTS_REQUIRED,
        optional_columns=("sid_level_0", "sid_level_1", "sid_level_2", "sid_level_3"),
    ),
    "item_metadata": TableContract(
        name="item_metadata",
        required_columns=ITEM_METADATA_REQUIRED,
        optional_columns=("category", "title", "brand", "text"),
    ),
    "interactions": TableContract(
        name="interactions",
        required_columns=INTERACTIONS_REQUIRED,
        optional_columns=("timestamp", "split"),
    ),
    "generator_outputs": TableContract(
        name="generator_outputs",
        required_columns=GENERATOR_OUTPUTS_REQUIRED,
        optional_columns=("sid", "score"),
    ),
}


def missing_columns(columns: Iterable[str], required: Sequence[str]) -> tuple[str, ...]:
    """Return required columns that are absent from a table-like object."""

    present = set(columns)
    return tuple(column for column in required if column not in present)


def validate_columns(table_name: str, columns: Iterable[str]) -> None:
    """Validate a normalized table against its required column contract."""

    if table_name not in CONTRACTS:
        known = ", ".join(sorted(CONTRACTS))
        raise KeyError(f"Unknown table contract {table_name!r}; known: {known}")

    contract = CONTRACTS[table_name]
    missing = missing_columns(columns, contract.required_columns)
    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"{table_name} is missing required columns: {missing_text}")
