#!/usr/bin/env python3
"""
Add various types of noise to thermal imagery with reproducible seeds.
"""

import argparse
import json
import numpy as np
from pathlib import Path
from PIL import Image
from skimage.util import random_noise
import sys


def set_seed(seed=42):
    """Set random seeds for reproducibility."""
    np.random.seed(seed)


def add_gaussian_noise(image, sigma=10, seed=42):
    """Add Gaussian noise with specified standard deviation."""
    set_seed(seed)
    # Convert sigma from 0-255 scale to 0-1 scale for skimage
    var = (sigma / 255.0) ** 2
    noisy = random_noise(image, mode='gaussian', var=var, seed=seed)
    return noisy


def add_poisson_noise(image, seed=42):
    """Add Poisson (shot) noise."""
    set_seed(seed)
    noisy = random_noise(image, mode='poisson', seed=seed)
    return noisy


def add_salt_pepper_noise(image, density=0.01, seed=42):
    """Add salt-and-pepper noise."""
    set_seed(seed)
    noisy = random_noise(image, mode='s&p', amount=density, seed=seed)
    return noisy


def add_speckle_noise(image, variance=0.01, seed=42):
    """Add speckle (multiplicative) noise."""
    set_seed(seed)
    noisy = random_noise(image, mode='speckle', var=variance, seed=seed)
    return noisy


def process_image(src_path, dst_path, noise_type, **params):
    """Process a single image with specified noise type."""
    # Load image
    img = Image.open(src_path)
    img_array = np.array(img).astype(np.float32) / 255.0

    # Apply noise
    if noise_type == 'gaussian':
        noisy = add_gaussian_noise(img_array, **params)
    elif noise_type == 'poisson':
        noisy = add_poisson_noise(img_array, **params)
    elif noise_type == 'saltpepper':
        noisy = add_salt_pepper_noise(img_array, **params)
    elif noise_type == 'speckle':
        noisy = add_speckle_noise(img_array, **params)
    else:
        raise ValueError(f"Unknown noise type: {noise_type}")

    # Convert back to uint8 and save
    noisy_uint8 = (np.clip(noisy, 0, 1) * 255).astype(np.uint8)
    noisy_img = Image.fromarray(noisy_uint8)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    noisy_img.save(dst_path)


def main():
    parser = argparse.ArgumentParser(description='Add noise to thermal images')
    parser.add_argument('--src', type=str, required=True,
                        help='Source directory with original images')
    parser.add_argument('--dst', type=str, required=True,
                        help='Destination directory for noisy images')
    parser.add_argument('--noise-type', type=str, required=True,
                        choices=['gaussian', 'poisson', 'saltpepper', 'speckle'],
                        help='Type of noise to add')
    parser.add_argument('--sigma', type=float, default=10,
                        help='Standard deviation for Gaussian noise (0-255 scale)')
    parser.add_argument('--density', type=float, default=0.01,
                        help='Density for salt-and-pepper noise (0-1)')
    parser.add_argument('--variance', type=float, default=0.01,
                        help='Variance for speckle noise')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for reproducibility')

    args = parser.parse_args()

    src_dir = Path(args.src)
    dst_dir = Path(args.dst)

    if not src_dir.exists():
        print(f"ERROR: Source directory does not exist: {src_dir}")
        sys.exit(1)

    # Get all image files
    image_files = sorted(src_dir.glob('*.jpg')) + sorted(src_dir.glob('*.jpeg'))

    if len(image_files) == 0:
        print(f"ERROR: No image files found in {src_dir}")
        sys.exit(1)

    print(f"Found {len(image_files)} images to process")
    print(f"Noise type: {args.noise_type}")

    # Prepare noise parameters
    params = {'seed': args.seed}
    if args.noise_type == 'gaussian':
        params['sigma'] = args.sigma
        print(f"Sigma: {args.sigma}")
    elif args.noise_type == 'saltpepper':
        params['density'] = args.density
        print(f"Density: {args.density}")
    elif args.noise_type == 'speckle':
        params['variance'] = args.variance
        print(f"Variance: {args.variance}")

    print(f"Random seed: {args.seed}")

    # Save metadata
    metadata = {
        'noise_type': args.noise_type,
        'parameters': params,
        'num_images': len(image_files),
        'source_directory': str(src_dir),
        'destination_directory': str(dst_dir)
    }

    metadata_path = dst_dir / 'noise_metadata.json'
    dst_dir.mkdir(parents=True, exist_ok=True)
    with open(metadata_path, 'w') as f:
        json.dump(metadata, indent=2, fp=f)
    print(f"Metadata saved to {metadata_path}")

    # Process images
    for src_path in image_files:
        dst_path = dst_dir / src_path.name
        print(f"Processing {src_path.name}...")
        process_image(src_path, dst_path, args.noise_type, **params)

    print(f"\nCompleted! Processed {len(image_files)} images")
    print(f"Output directory: {dst_dir}")


if __name__ == "__main__":
    main()
