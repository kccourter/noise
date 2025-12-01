#!/usr/bin/env python3
"""
Apply denoising algorithms to noisy images.

Usage:
  # Denoise specific noisy variant with specific algorithm
  python3 apply_denoise.py --noise gaussian_sigma10 --algo bm3d

  # Denoise specific noisy variant with all suitable algorithms
  python3 apply_denoise.py --noise gaussian_sigma10 --algo all

  # Denoise all noisy variants
  python3 apply_denoise.py --noise all --algo all
"""

import argparse
import json
import sys
from pathlib import Path
import cv2
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from denoise import DENOISE_ALGORITHMS, apply_denoise


def load_denoise_config(config_path=None):
    """Load denoising configuration."""
    if config_path is None:
        script_dir = Path(__file__).parent
        config_path = script_dir.parent / 'config' / 'denoise_configs.json'

    with open(config_path, 'r') as f:
        return json.load(f)


def get_noise_folders(base_dir):
    """Get all noise variant folders."""
    base_path = Path(base_dir).expanduser()
    if not base_path.exists():
        return []

    # Get all directories
    noise_folders = [d for d in base_path.iterdir() if d.is_dir()]
    return sorted(noise_folders)


def format_denoise_folder_name(algo_name, variation_name):
    """Format output folder name for denoised images."""
    return f"{algo_name}_{variation_name}"


def save_denoise_metadata(output_dir, algo_name, params, noise_type, num_images):
    """Save denoising metadata to JSON."""
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'algorithm': algo_name,
        'parameters': params,
        'noise_type': noise_type,
        'num_images': num_images,
        'output_directory': str(output_dir)
    }

    metadata_path = output_dir / 'denoise_metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    return metadata_path


def main():
    parser = argparse.ArgumentParser(
        description='Apply denoising algorithms to noisy images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Denoise gaussian_sigma10 with BM3D
  %(prog)s --noise gaussian_sigma10 --algo bm3d

  # Denoise gaussian_sigma10 with all suitable algorithms
  %(prog)s --noise gaussian_sigma10 --algo all

  # Denoise all noise variants with all algorithms
  %(prog)s --noise all --algo all

  # Denoise with specific algorithm variation
  %(prog)s --noise gaussian_sigma10 --algo bm3d --variation sigma10
        """
    )

    parser.add_argument('--noise', type=str, required=True,
                        help='Noise variant to denoise (e.g., gaussian_sigma10) or "all"')
    parser.add_argument('--algo', type=str, required=True,
                        help='Algorithm to use (median, bilateral, nlm, bm3d, wavelet, tv, all)')
    parser.add_argument('--variation', type=str, default=None,
                        help='Specific parameter variation name (optional)')
    parser.add_argument('--noisy-base', type=str,
                        default='~/data/noise/thermal/noisy',
                        help='Base directory for noisy images')
    parser.add_argument('--output-base', type=str,
                        default='~/data/noise/thermal/denoised',
                        help='Base directory for denoised outputs')

    args = parser.parse_args()

    # Load configuration
    print("Loading denoising configuration...")
    config = load_denoise_config()

    noisy_base = Path(args.noisy_base).expanduser()
    output_base = Path(args.output_base).expanduser()

    if not noisy_base.exists():
        print(f"ERROR: Noisy base directory does not exist: {noisy_base}")
        sys.exit(1)

    # Get noise folders to process
    if args.noise == 'all':
        noise_folders = get_noise_folders(noisy_base)
        if not noise_folders:
            print(f"ERROR: No noise folders found in {noisy_base}")
            sys.exit(1)
    else:
        noise_folder = noisy_base / args.noise
        if not noise_folder.exists():
            print(f"ERROR: Noise folder not found: {noise_folder}")
            sys.exit(1)
        noise_folders = [noise_folder]

    print(f"Found {len(noise_folders)} noise variant(s) to process")
    print(f"Output base: {output_base}")
    print()

    # Process each noise variant
    total_processed = 0

    for noise_folder in noise_folders:
        noise_type = noise_folder.name
        print("=" * 70)
        print(f"Processing noise variant: {noise_type}")
        print("=" * 70)

        # Get images in this noise folder
        image_files = sorted(noise_folder.glob('*.jpg')) + sorted(noise_folder.glob('*.jpeg'))
        # Exclude metadata
        image_files = [f for f in image_files if 'metadata' not in f.name.lower()]

        if not image_files:
            print(f"  No images found, skipping...")
            print()
            continue

        print(f"  Found {len(image_files)} image(s)")

        # Get suitable algorithms for this noise type
        if args.algo == 'all':
            # Use recommended algorithms from config
            noise_algo_mapping = config.get('noise_to_algorithm_mapping', {})
            if noise_type in noise_algo_mapping:
                algo_specs = noise_algo_mapping[noise_type]
                print(f"  Using recommended algorithms: {', '.join(algo_specs)}")
            else:
                # Use all Priority 1 algorithms
                algo_specs = [f"{name}:default" for name, info in DENOISE_ALGORITHMS.items() if info['priority'] == 1]
                print(f"  Using default Priority 1 algorithms")
        else:
            # Single algorithm
            if args.variation:
                algo_specs = [f"{args.algo}:{args.variation}"]
            else:
                algo_specs = [f"{args.algo}:default"]

        # Process each algorithm
        for algo_spec in algo_specs:
            if ':' in algo_spec:
                algo_name, variation_name = algo_spec.split(':', 1)
            else:
                algo_name = algo_spec
                variation_name = 'default'

            if algo_name not in DENOISE_ALGORITHMS:
                print(f"  WARNING: Unknown algorithm '{algo_name}', skipping...")
                continue

            print(f"\n  [{algo_name.upper()}:{variation_name}]")

            # Get parameters
            if variation_name == 'default':
                params = DENOISE_ALGORITHMS[algo_name]['default_params'].copy()
            else:
                # Look up variation in config
                algo_config = config['algorithms'].get(algo_name, {})
                variations = algo_config.get('parameter_variations', [])
                variation_params = None
                for var in variations:
                    if var['name'] == variation_name:
                        variation_params = {k: v for k, v in var.items() if k != 'name'}
                        break

                if variation_params is None:
                    print(f"    WARNING: Variation '{variation_name}' not found, using default")
                    params = DENOISE_ALGORITHMS[algo_name]['default_params'].copy()
                else:
                    params = variation_params

            print(f"    Parameters: {params}")

            # Create output directory
            folder_name = format_denoise_folder_name(algo_name, variation_name)
            output_dir = output_base / noise_type / folder_name
            output_dir.mkdir(parents=True, exist_ok=True)

            # Check if already processed
            if list(output_dir.glob('*.jpg')):
                print(f"    WARNING: Output already exists, skipping...")
                continue

            # Process images
            for i, img_path in enumerate(image_files, 1):
                print(f"    [{i}/{len(image_files)}] Processing {img_path.name}...")

                # Load image
                noisy_img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                if noisy_img is None:
                    print(f"      ERROR: Failed to load image")
                    continue

                # Apply denoising
                try:
                    denoised_img = apply_denoise(noisy_img, algo_name, **params)

                    # Save
                    output_path = output_dir / img_path.name
                    cv2.imwrite(str(output_path), denoised_img)

                except Exception as e:
                    print(f"      ERROR: Denoising failed: {e}")
                    continue

            # Save metadata
            metadata_path = save_denoise_metadata(
                output_dir, algo_name, params, noise_type, len(image_files)
            )
            print(f"    Metadata saved: {metadata_path.name}")

            total_processed += 1

        print()

    print("=" * 70)
    print(f"DENOISING COMPLETED")
    print("=" * 70)
    print(f"Processed {total_processed} algorithm/noise combinations")
    print("=" * 70)


if __name__ == "__main__":
    main()
