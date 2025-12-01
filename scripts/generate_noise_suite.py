#!/usr/bin/env python3
"""
Generate complete noise suite with all parameter variations from NOISE_STUDY.md.

Creates noisy image variants for:
- Gaussian: σ = 5, 10, 15, 20
- Poisson: (signal-dependent, no params)
- Salt-and-Pepper: density = 0.01, 0.05, 0.1
- Speckle: variance = 0.01, 0.05, 0.1
"""

import argparse
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from skimage.util import random_noise

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from noise_logger import (
    format_output_folder_name,
    log_noise_parameters,
    append_to_noise_log
)


def set_seed(seed=42):
    """Set random seeds for reproducibility."""
    np.random.seed(seed)


def add_gaussian_noise(image, sigma=10, seed=42):
    """Add Gaussian noise with specified standard deviation."""
    set_seed(seed)
    var = (sigma / 255.0) ** 2
    noisy = random_noise(image, mode='gaussian', var=var)
    return noisy


def add_poisson_noise(image, seed=42):
    """Add Poisson (shot) noise."""
    set_seed(seed)
    noisy = random_noise(image, mode='poisson')
    return noisy


def add_salt_pepper_noise(image, density=0.01, seed=42):
    """Add salt-and-pepper noise."""
    set_seed(seed)
    noisy = random_noise(image, mode='s&p', amount=density)
    return noisy


def add_speckle_noise(image, variance=0.01, seed=42):
    """Add speckle (multiplicative) noise."""
    set_seed(seed)
    noisy = random_noise(image, mode='speckle', var=variance)
    return noisy


def apply_noise_to_image(image, noise_type, params, seed):
    """Apply specified noise type to image."""
    params_with_seed = {**params, 'seed': seed}

    if noise_type == 'gaussian':
        return add_gaussian_noise(image, **params_with_seed)
    elif noise_type == 'poisson':
        return add_poisson_noise(image, **params_with_seed)
    elif noise_type == 'saltpepper':
        return add_salt_pepper_noise(image, **params_with_seed)
    elif noise_type == 'speckle':
        return add_speckle_noise(image, **params_with_seed)
    else:
        raise ValueError(f"Unknown noise type: {noise_type}")


def process_image(src_path, dst_path, noise_type, params, seed):
    """Process a single image with specified noise type."""
    # Load image
    img = Image.open(src_path)
    img_array = np.array(img).astype(np.float32) / 255.0

    # Apply noise
    noisy = apply_noise_to_image(img_array, noise_type, params, seed)

    # Convert back to uint8 and save
    noisy_uint8 = (np.clip(noisy, 0, 1) * 255).astype(np.uint8)
    noisy_img = Image.fromarray(noisy_uint8)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    noisy_img.save(dst_path)


def main():
    parser = argparse.ArgumentParser(
        description='Generate complete noise suite as specified in NOISE_STUDY.md'
    )
    parser.add_argument('--src', type=str,
                        default='~/data/noise/thermal/original',
                        help='Source directory with original images')
    parser.add_argument('--dst', type=str,
                        default='~/data/noise/thermal/noisy',
                        help='Destination base directory')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for reproducibility')

    args = parser.parse_args()

    src_dir = Path(args.src).expanduser()
    dst_base = Path(args.dst).expanduser()
    random_seed = args.seed

    if not src_dir.exists():
        print(f"ERROR: Source directory does not exist: {src_dir}")
        sys.exit(1)

    # Get all image files
    image_files = sorted(src_dir.glob('*.jpg')) + sorted(src_dir.glob('*.jpeg'))

    if len(image_files) == 0:
        print(f"ERROR: No image files found in {src_dir}")
        sys.exit(1)

    print("=" * 70)
    print("GENERATING COMPLETE NOISE SUITE")
    print("=" * 70)
    print(f"Source: {src_dir}")
    print(f"Destination: {dst_base}")
    print(f"Images: {len(image_files)}")
    print(f"Random seed: {random_seed}")
    print()

    # Define noise parameter suite from NOISE_STUDY.md
    noise_suite = [
        # Gaussian noise - test σ values: 5, 10, 15, 20
        ('gaussian', {'sigma': 5}),
        ('gaussian', {'sigma': 10}),
        ('gaussian', {'sigma': 15}),
        ('gaussian', {'sigma': 20}),

        # Poisson noise - signal dependent
        ('poisson', {}),

        # Salt-and-pepper - test densities: 0.01, 0.05, 0.1
        ('saltpepper', {'density': 0.01}),
        ('saltpepper', {'density': 0.05}),
        ('saltpepper', {'density': 0.1}),

        # Speckle - test variance: 0.01, 0.05, 0.1
        ('speckle', {'variance': 0.01}),
        ('speckle', {'variance': 0.05}),
        ('speckle', {'variance': 0.1}),
    ]

    print(f"Total noise variations to generate: {len(noise_suite)}")
    print()

    # Process each noise variation
    central_log = Path.home() / 'data' / 'noise' / 'metadata' / 'noise_params.json'

    for idx, (noise_type, params) in enumerate(noise_suite, 1):
        print("=" * 70)
        print(f"[{idx}/{len(noise_suite)}] Applying {noise_type.upper()} noise")
        print("=" * 70)

        # Display parameters
        if params:
            print(f"Parameters:")
            for key, value in params.items():
                print(f"  - {key}: {value}")
        else:
            print(f"Parameters: (none)")

        # Create output directory
        folder_name = format_output_folder_name(noise_type, params)
        output_dir = dst_base / folder_name

        print(f"Output directory: {output_dir}")

        # Check if already exists
        if output_dir.exists() and list(output_dir.glob('*.jpg')):
            print(f"WARNING: Directory exists with images, skipping...")
            print()
            continue

        print()

        # Process images
        for i, src_path in enumerate(image_files, 1):
            dst_path = output_dir / src_path.name
            print(f"  [{i}/{len(image_files)}] Processing {src_path.name}...")
            process_image(src_path, dst_path, noise_type, params, random_seed)

        print(f"\nCompleted {noise_type} noise application")

        # Save metadata
        metadata_path = output_dir / 'noise_metadata.json'
        additional_info = {
            'num_images': len(image_files),
            'source_directory': str(src_dir),
            'destination_directory': str(output_dir),
            'source_files': [f.name for f in image_files]
        }
        log_noise_parameters(metadata_path, noise_type, params, random_seed, additional_info)
        print(f"Metadata saved to {metadata_path}")

        # Append to central log
        append_to_noise_log(central_log, noise_type, params, random_seed, image_files, output_dir)
        print()

    print("=" * 70)
    print("NOISE SUITE GENERATION COMPLETED!")
    print("=" * 70)
    print(f"Generated {len(noise_suite)} noise variations")
    print(f"Processed {len(image_files)} image(s) per variation")
    print()
    print("Noise variations created:")
    print("-" * 70)
    print("Gaussian:")
    for sigma in [5, 10, 15, 20]:
        print(f"  - gaussian_sigma{sigma}")
    print("\nPoisson:")
    print(f"  - poisson_lambda1")
    print("\nSalt-and-Pepper:")
    for density in [0.01, 0.05, 0.1]:
        density_int = int(density * 100)
        print(f"  - saltpepper_d{density_int:03d}")
    print("\nSpeckle:")
    for variance in [0.01, 0.05, 0.1]:
        var_int = int(variance * 100)
        print(f"  - speckle_var{var_int:03d}")
    print("=" * 70)


if __name__ == "__main__":
    main()
