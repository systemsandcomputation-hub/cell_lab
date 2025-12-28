## Invariant Engine — Domain #1: Cell Lab

---

# Cell Lab — Synthetic Cell Generator

This directory contains a **synthetic time-series generator** used as a
public reference artifact for **Cell Lab**.

The generator produces small, fully inspectable JSON samples that model
simplified cell health trajectories under different conditions.

It is designed to provide **transparent, regime-aware input data** —
not analysis, scoring, or invariant discovery.

---

## Purpose

The purpose of this generator is to provide:

- Reproducible reference inputs

- Explicit regime labeling

- Fully inspectable artifacts

It exists to support evaluation, testing, and demonstration — not to
represent a full analysis pipeline

---

## What This Generator Does

The generator creates **independent time-series samples**, where each sample:

- Represents a single synthetic “cell”
- Evolves over discrete time steps
- Remains bounded in the range `[0.0, 1.0]`
- Is generated under **explicit, labeled parameters**

Each output file is self-contained and can be inspected directly.

---

## What This Generator Is Not

This generator does not:

- Perform anomaly detection

- Compute scores or predictions

- Discover invariants

- Train or use machine learning models

Those capabilities exist only in the private invariant engine
and are intentionally excluded from this repository.

---

## Output Structure

Each generated file (e.g. `sample_000001.json`) contains:

'''json
{
  "sample_id": 1,
  "created_utc": "...",
  "params": {
    "pathology": "normal | burst | chronic",
    "damage_rate": <float>,
    "repair_rate": <float>,
    "stress_burst": <bool>,
    "chronic_drift_per_step": <float>
  },
  "series": [ <float>, <float>, ... ]
}
'''json

params describe the generative regime.

series is the resulting time-series trajectory.

No hidden state or post-processing is applied.

## Generative Regimes

The generator supports multiple regimes:

Normal
Balanced damage and repair dynamics.

Burst
Temporary high-stress damage windows.

Chronic
Slow, persistent degradation without discrete bursts.

Some generated samples may appear stable or nearly flat.
This is intentional — stable regimes are first-class cases and
important for invariant-based analysis.

---

## Usage

python3 cell_generator.py \
  --outdir ./out_samples \
  --target 20

This will generate 20 JSON samples in ./out_samples.

---

## Common Options

--outdir <path>        Output directory (required)
--target <int>         Number of samples to generate
--seed <int>           RNG seed (default: 123)
--burst-prob <float>   Probability of burst pathology
--chronic-prob <float> Probability of chronic pathology
--sleep <seconds>      Pause between samples

---

## Example with mixed regimes:

python3 cell_generator.py \
  --outdir ./out_samples \
  --target 50 \
  --burst-prob 0.15 \
  --chronic-prob 0.10

---

## Citation
If you use this generator in your research, please cite:
[Benjamin Freeman / Systems & Computation], Cell Lab Synthetic Generator (2025)
GitHub: [https://github.com/systemsandcomputation-hub/cell_lab]



