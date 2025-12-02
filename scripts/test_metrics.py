#!/usr/bin/env python3
"""
Test script for baseline metrics measurement on thermal images.
"""

import argparse
import json
import sys
from pathlib import Path
import cv2
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from metrics import METRIC_FUNCTIONS, compute_all_metrics


def load_image(image_path):
    """Load image as grayscale."""
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    return img


def format_metrics(metrics, indent=0):
    """Recursively format metrics for display."""
    lines = []
    prefix = "  " * indent

    for key, value in metrics.items():
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            lines.extend(format_metrics(value, indent + 1))
        elif isinstance(value, list):
            # Skip histogram display (too long)
            if key == 'histogram':
                lines.append(f"{prefix}{key}: [256 bins]")
            else:
                lines.append(f"{prefix}{key}: {value}")
        elif isinstance(value, float):
            lines.append(f"{prefix}{key}: {value:.4f}")
        else:
            lines.append(f"{prefix}{key}: {value}")

    return lines


def main():
    parser = argparse.ArgumentParser(
        description='Measure baseline metrics on thermal images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available metrics:
  statistical    - Mean, std, min, max, histogram
  sharpness      - Laplacian variance, gradient magnitude
  contrast       - Michelson, RMS, local contrast
  noise          - Estimated noise sigma (MAD method)
  information    - Entropy, edge density
  dynamic_range  - Effective bit depth, histogram spread, saturation
  all            - All metrics (default)

Examples:
  %(prog)s image.jpg
  %(prog)s image.jpg --metric sharpness
  %(prog)s image.jpg --metric all --json output.json
        """
    )

    parser.add_argument('image', type=str,
                        help='Path to input image')
    parser.add_argument('--metric', type=str, default='all',
                        choices=list(METRIC_FUNCTIONS.keys()),
                        help='Metric to compute (default: all)')
    parser.add_argument('--json', type=str, default=None,
                        help='Save results to JSON file')

    args = parser.parse_args()

    # Load image
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"ERROR: Image not found: {image_path}")
        sys.exit(1)

    print(f"Loading image: {image_path}")
    image = load_image(image_path)
    print(f"Image shape: {image.shape}")
    print()

    # Compute metrics
    metric_func = METRIC_FUNCTIONS[args.metric]
    print(f"Computing metrics: {args.metric}")
    metrics = metric_func(image)

    # Display results
    print("\nResults:")
    print("=" * 60)
    for line in format_metrics(metrics):
        print(line)
    print("=" * 60)

    # Save to JSON if requested
    if args.json:
        output_path = Path(args.json)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_data = {
            'image_path': str(image_path),
            'image_shape': list(image.shape),
            'metric_type': args.metric,
            'metrics': metrics
        }

        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
