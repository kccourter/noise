#!/usr/bin/env python3
"""
Test script to demonstrate noise parameter logging system.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from noise_logger import load_noise_parameters, create_noise_parameter_summary


def main():
    # Load central noise log
    central_log = Path.home() / 'data' / 'noise' / 'metadata' / 'noise_params.json'

    if not central_log.exists():
        print(f"ERROR: Central log not found: {central_log}")
        print("Run add_noise.py first to create noise applications.")
        sys.exit(1)

    import json
    with open(central_log, 'r') as f:
        log_data = json.load(f)

    entries = log_data.get('entries', [])

    if not entries:
        print("No noise applications logged yet.")
        sys.exit(0)

    print(create_noise_parameter_summary(entries))


if __name__ == "__main__":
    main()
