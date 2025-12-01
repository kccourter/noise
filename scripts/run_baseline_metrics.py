#!/usr/bin/env python3
"""
Run baseline metrics on all thermal images in the dataset.
"""

import argparse
import json
import sys
from pathlib import Path
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from metrics import compute_all_metrics


def load_image(image_path):
    """Load image as grayscale."""
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    return img


def compute_summary_statistics(all_results):
    """Compute summary statistics across all images."""

    # Extract metrics into arrays for statistical analysis
    def extract_metric_values(results, path):
        """Extract values from nested dict using path like ['statistical', 'mean']."""
        values = []
        for result in results:
            val = result['metrics']
            for key in path:
                val = val.get(key, None)
                if val is None:
                    break
            if val is not None and not isinstance(val, (dict, list)):
                values.append(val)
        return values

    # Define metric paths to summarize (exclude histogram and lists)
    metric_paths = [
        (['statistical', 'mean'], 'statistical.mean'),
        (['statistical', 'std'], 'statistical.std'),
        (['statistical', 'min'], 'statistical.min'),
        (['statistical', 'max'], 'statistical.max'),
        (['sharpness', 'laplacian_variance'], 'sharpness.laplacian_variance'),
        (['sharpness', 'mean_gradient'], 'sharpness.mean_gradient'),
        (['sharpness', 'max_gradient'], 'sharpness.max_gradient'),
        (['contrast', 'michelson_contrast'], 'contrast.michelson_contrast'),
        (['contrast', 'rms_contrast'], 'contrast.rms_contrast'),
        (['contrast', 'mean_local_contrast'], 'contrast.mean_local_contrast'),
        (['contrast', 'std_local_contrast'], 'contrast.std_local_contrast'),
        (['noise', 'estimated_noise_sigma'], 'noise.estimated_noise_sigma'),
        (['information', 'entropy'], 'information.entropy'),
        (['information', 'edge_density'], 'information.edge_density'),
        (['dynamic_range', 'effective_bit_depth'], 'dynamic_range.effective_bit_depth'),
        (['dynamic_range', 'histogram_spread'], 'dynamic_range.histogram_spread'),
        (['dynamic_range', 'saturation_low_pct'], 'dynamic_range.saturation_low_pct'),
        (['dynamic_range', 'saturation_high_pct'], 'dynamic_range.saturation_high_pct'),
        (['dynamic_range', 'saturation_total_pct'], 'dynamic_range.saturation_total_pct'),
    ]

    summary = {}

    for path, name in metric_paths:
        values = extract_metric_values(all_results, path)
        if values:
            summary[name] = {
                'mean': float(np.mean(values)),
                'std': float(np.std(values)),
                'min': float(np.min(values)),
                'max': float(np.max(values)),
                'median': float(np.median(values))
            }

    return summary


def main():
    parser = argparse.ArgumentParser(description='Run baseline metrics on thermal image dataset')
    parser.add_argument('--src', type=str,
                        default='~/data/noise/thermal/original',
                        help='Source directory with original images')
    parser.add_argument('--output', type=str,
                        default='~/data/noise/metrics/baseline_metrics.json',
                        help='Output JSON file for results')

    args = parser.parse_args()

    src_dir = Path(args.src).expanduser()
    output_path = Path(args.output).expanduser()

    if not src_dir.exists():
        print(f"ERROR: Source directory does not exist: {src_dir}")
        sys.exit(1)

    # Get all image files
    image_files = sorted(src_dir.glob('*.jpg')) + sorted(src_dir.glob('*.jpeg'))

    if len(image_files) == 0:
        print(f"ERROR: No image files found in {src_dir}")
        sys.exit(1)

    print(f"Found {len(image_files)} images in {src_dir}")
    print(f"Computing baseline metrics...\n")

    # Process all images
    all_results = []

    for i, image_path in enumerate(image_files, 1):
        print(f"[{i}/{len(image_files)}] Processing {image_path.name}...")

        try:
            image = load_image(image_path)
            metrics = compute_all_metrics(image)

            result = {
                'filename': image_path.name,
                'image_path': str(image_path),
                'image_shape': list(image.shape),
                'metrics': metrics
            }

            all_results.append(result)

        except Exception as e:
            print(f"  ERROR: Failed to process {image_path.name}: {e}")
            continue

    if len(all_results) == 0:
        print("\nERROR: No images were successfully processed")
        sys.exit(1)

    print(f"\nSuccessfully processed {len(all_results)} images")

    # Compute summary statistics
    print("Computing summary statistics...")
    summary = compute_summary_statistics(all_results)

    # Prepare output
    output_data = {
        'dataset_info': {
            'source_directory': str(src_dir),
            'num_images': len(all_results),
            'timestamp': datetime.now().isoformat(),
        },
        'summary_statistics': summary,
        'per_image_results': all_results
    }

    # Save results
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    # Print summary
    print("\n" + "=" * 70)
    print("BASELINE METRICS SUMMARY")
    print("=" * 70)
    print(f"Dataset: {src_dir}")
    print(f"Images processed: {len(all_results)}")
    print()

    # Print key metrics
    if summary:
        print("Key Metrics (mean ± std):")
        print("-" * 70)

        key_metrics = [
            ('statistical.mean', 'Mean Intensity'),
            ('statistical.std', 'Std Deviation'),
            ('sharpness.laplacian_variance', 'Laplacian Variance'),
            ('noise.estimated_noise_sigma', 'Estimated Noise Sigma'),
            ('information.entropy', 'Entropy (bits)'),
            ('information.edge_density', 'Edge Density (%)'),
            ('dynamic_range.histogram_spread', 'Histogram Spread (%)'),
        ]

        for key, label in key_metrics:
            if key in summary:
                s = summary[key]
                print(f"{label:30s}: {s['mean']:8.2f} ± {s['std']:6.2f}  "
                      f"[{s['min']:.2f}, {s['max']:.2f}]")

        print("=" * 70)


if __name__ == "__main__":
    main()
