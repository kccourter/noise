#!/usr/bin/env python3
"""
Apply noise to images using parameters from active_noise_params.json config file.
Can apply a specific noise type or all enabled types.
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
    load_active_noise_params,
    get_enabled_noise_types,
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
    """
    Apply specified noise type to image.

    Args:
        image: Normalized image array (0-1 range)
        noise_type: Type of noise to apply
        params: Parameters dict for the noise
        seed: Random seed

    Returns:
        Noisy image array (0-1 range)
    """
    # Add seed to params
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
        description='Apply noise to images using config file parameters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Apply all enabled noise types from config
  %(prog)s image.jpg

  # Apply only Gaussian noise
  %(prog)s image.jpg --noise gaussian

  # Process all images in a directory
  %(prog)s ~/data/noise/thermal/original --noise all

  # Use custom config file
  %(prog)s image.jpg --config my_config.json

Configuration is read from: config/active_noise_params.json
        """
    )

    parser.add_argument('input', type=str,
                        help='Input image file or directory')
    parser.add_argument('--noise', type=str, default='all',
                        help='Noise type to apply (gaussian, poisson, saltpepper, speckle, all)')
    parser.add_argument('--config', type=str, default=None,
                        help='Path to config file (default: config/active_noise_params.json)')
    parser.add_argument('--output-base', type=str, default=None,
                        help='Override output base directory from config')

    args = parser.parse_args()

    # Load configuration
    print("Loading configuration...")
    try:
        config = load_active_noise_params(args.config)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    random_seed = config.get('random_seed', 42)
    data_paths = config.get('data_paths', {})

    # Determine output base directory
    if args.output_base:
        output_base = Path(args.output_base).expanduser()
    else:
        output_base = Path(data_paths.get('destination_base', '~/data/noise/thermal/noisy')).expanduser()

    # Get enabled noise types from config
    enabled_types = get_enabled_noise_types(config)

    if not enabled_types:
        print("ERROR: No enabled noise types in configuration")
        sys.exit(1)

    # Filter by requested noise type
    if args.noise != 'all':
        enabled_types = [(nt, p) for nt, p in enabled_types if nt == args.noise]
        if not enabled_types:
            print(f"ERROR: Noise type '{args.noise}' not found or not enabled in config")
            sys.exit(1)

    # Get input files
    input_path = Path(args.input).expanduser()

    if not input_path.exists():
        print(f"ERROR: Input path does not exist: {input_path}")
        sys.exit(1)

    if input_path.is_file():
        image_files = [input_path]
    elif input_path.is_dir():
        image_files = sorted(input_path.glob('*.jpg')) + sorted(input_path.glob('*.jpeg'))
        if not image_files:
            print(f"ERROR: No image files found in {input_path}")
            sys.exit(1)
    else:
        print(f"ERROR: Invalid input path: {input_path}")
        sys.exit(1)

    print(f"Found {len(image_files)} image(s) to process")
    print(f"Random seed: {random_seed}")
    print(f"Output base: {output_base}")
    print()

    # Process each enabled noise type
    for noise_type, params in enabled_types:
        print("=" * 70)
        print(f"Applying {noise_type.upper()} noise")
        print("=" * 70)

        # Display parameters
        print(f"Parameters:")
        for key, value in params.items():
            print(f"  - {key}: {value}")

        # Create output directory
        folder_name = format_output_folder_name(noise_type, params)
        output_dir = output_base / folder_name

        print(f"Output directory: {output_dir}")
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
            'source_directory': str(input_path) if input_path.is_dir() else str(input_path.parent),
            'destination_directory': str(output_dir),
            'source_files': [f.name for f in image_files]
        }
        log_noise_parameters(metadata_path, noise_type, params, random_seed, additional_info)
        print(f"Metadata saved to {metadata_path}")

        # Append to central log
        central_log = Path.home() / 'data' / 'noise' / 'metadata' / 'noise_params.json'
        append_to_noise_log(central_log, noise_type, params, random_seed, image_files, output_dir)
        print(f"Entry added to central log")
        print()

    print("=" * 70)
    print(f"All noise applications completed!")
    print(f"Processed {len(image_files)} image(s) with {len(enabled_types)} noise type(s)")
    print("=" * 70)


if __name__ == "__main__":
    main()
