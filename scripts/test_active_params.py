#!/usr/bin/env python3
"""
Test script to demonstrate reading active noise parameters.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from noise_logger import load_active_noise_params, get_enabled_noise_types, format_output_folder_name


def main():
    print("Loading active noise parameters...")
    print("=" * 70)

    try:
        config = load_active_noise_params()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print(f"Configuration file loaded successfully")
    print(f"Random seed: {config.get('random_seed', 42)}")
    print(f"Source directory: {config.get('data_paths', {}).get('source', 'N/A')}")
    print(f"Destination base: {config.get('data_paths', {}).get('destination_base', 'N/A')}")
    print()

    # Get enabled noise types
    enabled_types = get_enabled_noise_types(config)

    print(f"Enabled noise types: {len(enabled_types)}")
    print("-" * 70)

    for noise_type, params in enabled_types:
        folder_name = format_output_folder_name(noise_type, params)
        print(f"\nNoise Type: {noise_type.upper()}")
        print(f"  Output folder: {folder_name}")
        print(f"  Parameters:")
        for key, value in params.items():
            print(f"    - {key}: {value}")

    print()
    print("=" * 70)
    print("\nTo modify these parameters, edit: config/active_noise_params.json")


if __name__ == "__main__":
    main()
