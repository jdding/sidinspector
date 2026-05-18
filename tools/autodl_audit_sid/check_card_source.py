"""Check whether the local CARD clone has the source files needed for RQ-VAE."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Check CARD RQ-VAE source integrity.")
    parser.add_argument("--card-dir", type=Path, default=Path("_gate0_repos/CARD"))
    parser.add_argument("--no-import-smoke", action="store_true")
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

    if not args.no_import_smoke:
        sys.path.insert(0, str(args.card_dir.resolve()))
        import torch
        from rqvae4.models.rq import ResidualVectorQuantizer
        from rqvae4.models.rqvae import RQVAE
        from rqvae4.models.vq import VectorQuantizer

        vq = VectorQuantizer(4, 3)
        x = torch.randn(5, 3)
        quantized, loss, indices = vq(x, use_sk=False)
        assert quantized.shape == x.shape
        assert indices.shape == (5,)
        assert torch.isfinite(loss)

        rq = ResidualVectorQuantizer([4, 5], 3, sk_epsilons=[0.0, 0.0])
        rq_out, rq_loss, rq_indices = rq(x, use_sk=False)
        assert rq_out.shape == x.shape
        assert rq_indices.shape == (5, 2)
        assert torch.isfinite(rq_loss)

        model = RQVAE(in_dim=8, num_emb_list=[4, 5], e_dim=3, layers=[6], sk_epsilons=[0.0, 0.0])
        out, model_loss, model_indices = model(torch.randn(7, 8), use_sk=False)
        assert out.shape == (7, 8)
        assert model_indices.shape == (7, 2)
        assert torch.isfinite(model_loss)

    print("[CARD source check] OK")


if __name__ == "__main__":
    main()
