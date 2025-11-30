#!/usr/bin/env python3
"""
Utility for logging metadata about experiments for reproducibility.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def get_package_version(package_name):
    """Get version of an installed package."""
    try:
        import importlib.metadata
        return importlib.metadata.version(package_name)
    except Exception:
        return "unknown"


def get_environment_info():
    """Collect environment information for reproducibility."""
    info = {
        'python_version': sys.version,
        'platform': sys.platform,
        'timestamp': datetime.now().isoformat(),
    }

    # Core packages for noise study
    packages = [
        'numpy',
        'pillow',
        'opencv-python',
        'scikit-image',
        'imageio',
        'ptwt',
        'pywavelets',
        'bm3d',
        'pandas',
        'matplotlib',
        'seaborn',
        'torch',
    ]

    info['package_versions'] = {}
    for pkg in packages:
        # Handle package name variations
        pkg_import = pkg.replace('-', '_').lower()
        if pkg == 'pillow':
            pkg_import = 'PIL'
        elif pkg == 'opencv-python':
            pkg_import = 'cv2'

        info['package_versions'][pkg] = get_package_version(pkg_import)

    return info


def save_metadata(output_path, metadata_dict):
    """Save metadata to JSON file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Add environment info
    full_metadata = {
        'environment': get_environment_info(),
        **metadata_dict
    }

    with open(output_path, 'w') as f:
        json.dump(full_metadata, f, indent=2)

    print(f"Metadata saved to {output_path}")


def load_metadata(input_path):
    """Load metadata from JSON file."""
    with open(input_path, 'r') as f:
        return json.load(f)


def main():
    """Test the metadata logger."""
    import argparse

    parser = argparse.ArgumentParser(description='Create environment metadata file')
    parser.add_argument('--output', type=str, default='metadata/environment.json',
                        help='Output path for metadata file')
    args = parser.parse_args()

    metadata = {
        'description': 'Environment snapshot for noise removal experiments'
    }

    save_metadata(args.output, metadata)
    print("\nEnvironment information:")
    env_info = get_environment_info()
    print(f"Python version: {env_info['python_version'].split()[0]}")
    print(f"Platform: {env_info['platform']}")
    print("\nPackage versions:")
    for pkg, version in env_info['package_versions'].items():
        print(f"  {pkg}: {version}")


if __name__ == "__main__":
    main()
