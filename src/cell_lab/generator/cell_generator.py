#!/usr/bin/env python3
import os, json, time, argparse, random
from datetime import datetime

def atomic_write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.replace(tmp, path)  # atomic on same filesystem

def generate_cell_sample(rng, sample_id: int, *, burst_prob: float, chronic_prob: float):
    """
    Synthetic 'cell' time-series sample.
    Phase 3A adds a second pathology class: chronic damage (no bursts).
    """
    T = 512

    # Base rates (your original ranges)
    base_damage = rng.uniform(0.001, 0.01)
    base_repair = rng.uniform(0.001, 0.02)

    # Decide pathology class
    u = rng.random()
    if u < chronic_prob:
        pathology = "chronic"
        stress_burst = False
    elif u < chronic_prob + burst_prob:
        pathology = "burst"
        stress_burst = True
    else:
        pathology = "normal"
        stress_burst = False

    # Apply pathology transforms
    damage_rate = base_damage
    repair_rate = base_repair

    # Chronic: slightly higher damage, slightly lower repair, + tiny drift downwards
    # (quiet failure mode: no discrete burst window)
    chronic_drift_per_step = 0.0
    if pathology == "chronic":
        damage_rate *= rng.uniform(1.8, 3.2)      # more damage events
        repair_rate *= rng.uniform(0.25, 0.60)    # fewer repairs
        chronic_drift_per_step = rng.uniform(0.00006, 0.00018)  # slow decay each step

    state = 1.0
    series = []
    for t in range(T):
        # chronic drift (small but relentless)
        if chronic_drift_per_step > 0.0:
            state -= chronic_drift_per_step

        # damage events
        if rng.random() < damage_rate:
            state -= rng.uniform(0.0005, 0.012)

        # burst pathology (your original style)
        if stress_burst and (200 <= t <= 240) and (rng.random() < 0.08):
            state -= rng.uniform(0.01, 0.03)

        # repair events
        if rng.random() < repair_rate:
            state += rng.uniform(0.0005, 0.008)

        state = max(0.0, min(1.0, state))
        series.append(state)

    return {
        "sample_id": sample_id,
        "created_utc": datetime.utcnow().isoformat() + "Z",
        "params": {
            "pathology": pathology,              # NEW label
            "damage_rate": damage_rate,
            "repair_rate": repair_rate,
            "stress_burst": stress_burst,
            "chronic_drift_per_step": chronic_drift_per_step,  # 0 for non-chronic
        },
        "series": series
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--target", type=int, default=100000)
    ap.add_argument("--start-id", type=int, default=1)
    ap.add_argument("--sleep", type=float, default=0.0, help="seconds between samples")
    ap.add_argument("--seed", type=int, default=123)
    ap.add_argument("--max-inbox", type=int, default=5000, help="backpressure: stop generating if inbox has too many files")

    # Phase 3A knobs (defaults preserve your old behavior)
    ap.add_argument("--burst-prob", type=float, default=0.10, help="P(pathology=burst)")
    ap.add_argument("--chronic-prob", type=float, default=0.00, help="P(pathology=chronic)")

    args = ap.parse_args()

    if args.burst_prob < 0 or args.chronic_prob < 0 or (args.burst_prob + args.chronic_prob) > 1.0:
        raise SystemExit("Invalid probs: require burst_prob>=0, chronic_prob>=0, burst_prob+chronic_prob<=1")

    os.makedirs(args.outdir, exist_ok=True)
    rng = random.Random(args.seed)

    sample_id = args.start_id
    while sample_id <= args.target:
        # backpressure
        try:
            if args.max_inbox > 0:
                nfiles = len([x for x in os.listdir(args.outdir) if x.endswith(".json")])
                if nfiles >= args.max_inbox:
                    time.sleep(0.25)
                    continue
        except FileNotFoundError:
            os.makedirs(args.outdir, exist_ok=True)

        obj = generate_cell_sample(
            rng,
            sample_id,
            burst_prob=args.burst_prob,
            chronic_prob=args.chronic_prob,
        )
        fname = f"sample_{sample_id:06d}.json"
        atomic_write_json(os.path.join(args.outdir, fname), obj)

        sample_id += 1
        if args.sleep > 0:
            time.sleep(args.sleep)

    print(f"[generator] done: wrote {args.target - args.start_id + 1} samples")

if __name__ == "__main__":
    main()
