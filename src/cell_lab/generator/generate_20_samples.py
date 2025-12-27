#!/usr/bin/env python3
"""
generate_20_samples.py

Small in-memory demo for the synthetic cell generator.

Run from this directory:

    python3 generate_20_samples.py

Optional:
    python3 generate_20_samples.py --n 50 --seed 123 --burst-prob 0.15 --chronic-prob 0.10
"""

import argparse
import random
from collections import Counter

# Local sibling import (works when executed directly from this directory)
from cell_generator import generate_cell_sample


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20, help="Number of samples to generate in memory")
    ap.add_argument("--seed", type=int, default=123, help="RNG seed")
    ap.add_argument("--burst-prob", type=float, default=0.10, help="P(pathology=burst)")
    ap.add_argument("--chronic-prob", type=float, default=0.05, help="P(pathology=chronic)")
    args = ap.parse_args()

    if args.burst_prob < 0 or args.chronic_prob < 0 or (args.burst_prob + args.chronic_prob) > 1.0:
        raise SystemExit("Invalid probs: require burst_prob>=0, chronic_prob>=0, burst_prob+chronic_prob<=1")

    rng = random.Random(args.seed)
    samples = [
        generate_cell_sample(rng, i, burst_prob=args.burst_prob, chronic_prob=args.chronic_prob)
        for i in range(1, args.n + 1)
    ]

    counts = Counter(s["params"]["pathology"] for s in samples)
    print(f"[example] generated {len(samples)} samples (seed={args.seed})")
    print("[example] pathology counts:", dict(counts))
    print("[example] series length:", len(samples[0]["series"]))


if __name__ == "__main__":
    main()
