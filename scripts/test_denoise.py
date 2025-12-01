#!/usr/bin/env python3
"""
Test script for denoising algorithms.
"""

import sys
from pathlib import Path
import cv2

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from denoise import DENOISE_ALGORITHMS, apply_denoise


def main():
    # Load a noisy test image
    test_image_path = Path.home() / 'data' / 'noise' / 'thermal' / 'noisy' / 'gaussian_sigma10' / 'frame-000591.jpg'

    if not test_image_path.exists():
        print(f"ERROR: Test image not found: {test_image_path}")
        print("Run generate_noise_suite.py first")
        sys.exit(1)

    print(f"Loading test image: {test_image_path}")
    noisy_image = cv2.imread(str(test_image_path), cv2.IMREAD_GRAYSCALE)

    if noisy_image is None:
        print("ERROR: Failed to load image")
        sys.exit(1)

    print(f"Image shape: {noisy_image.shape}")
    print()

    print("=" * 70)
    print("TESTING DENOISING ALGORITHMS")
    print("=" * 70)
    print()

    # Test each algorithm
    for algo_name, algo_info in DENOISE_ALGORITHMS.items():
        priority = algo_info['priority']
        description = algo_info['description']
        default_params = algo_info['default_params']

        print(f"[Priority {priority}] {algo_name.upper()}")
        print(f"  Description: {description}")
        print(f"  Default params: {default_params}")

        try:
            # Apply denoising
            denoised = apply_denoise(noisy_image, algo_name)
            print(f"  ✓ Success - Output shape: {denoised.shape}")

            # Save test output
            output_dir = Path(__file__).parent.parent / 'test_output'
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f'test_{algo_name}.jpg'
            cv2.imwrite(str(output_path), denoised)
            print(f"  Saved to: {output_path}")

        except Exception as e:
            print(f"  ✗ FAILED: {e}")

        print()

    print("=" * 70)
    print("TESTING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
