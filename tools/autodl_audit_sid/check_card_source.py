"""Check whether the local CARD clone has the source files needed for RQ-VAE."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Check CARD RQ-VAE source integrity.")
    parser.add_argument("--card-dir", type=Path, default=Path("_gate0_repos/CARD"))
    args = parser.parse_args()

    required = [
        args.card_dir / "rqvae4/main.py",
        args.card_dir / "rqvae4/generate_code.py",
        args.card_dir / "rqvae4/models/rqvae.py",
        args.card_dir / "rqvae4/models/layers.py",
        args.card_dir / "rqvae4/models/rq.py",
        args.card_dir / "rqvae4/models/vq.py",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        print("[CARD source check] MISSING")
        for path in missing:
            print(path)
        raise SystemExit(2)

    print("[CARD source check] OK")


if __name__ == "__main__":
    main()
