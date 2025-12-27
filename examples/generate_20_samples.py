#!/usr/bin/env python3
import json, os, tempfile
from cell_lab.generator.cell_generator import generate_cell_sample
import random

def main():
    rng = random.Random(123)
    samples = []
    for i in range(1, 21):
        s = generate_cell_sample(rng, i, burst_prob=0.10, chronic_prob=0.05)
        samples.append(s)

    # Print a couple quick sanity stats (no proprietary logic)
    pathologies = {}
    for s in samples:
        p = s["params"]["pathology"]
        pathologies[p] = pathologies.get(p, 0) + 1

    print("Generated:", len(samples))
    print("Pathologies:", pathologies)
    print("Example series length:", len(samples[0]["series"]))

if __name__ == "__main__":
    main()
