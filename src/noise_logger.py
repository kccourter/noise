#!/usr/bin/env python3
"""
Parameter logging system for tracking noise configurations.
"""

import json
from datetime import datetime
from pathlib import Path
import sys


def log_noise_parameters(output_path, noise_type, parameters, seed, additional_info=None):
    """
    Log noise configuration parameters to JSON file.

    Args:
        output_path: Path to save the log file
        noise_type: Type of noise applied (gaussian, poisson, saltpepper, speckle)
        parameters: Dict of noise parameters (sigma, density, variance, etc.)
        seed: Random seed used for reproducibility
        additional_info: Optional dict with extra information
    """
    output_path = Path(output_path)

    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'noise_type': noise_type,
        'parameters': parameters,
        'random_seed': seed,
        'python_version': sys.version.split()[0]
    }

    if additional_info:
        log_entry.update(additional_info)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(log_entry, f, indent=2)

    return log_entry


def load_noise_parameters(input_path):
    """
    Load noise configuration parameters from JSON file.

    Args:
        input_path: Path to the log file

    Returns:
        dict: Loaded parameters
    """
    with open(input_path, 'r') as f:
        return json.load(f)


def append_to_noise_log(log_file, noise_type, parameters, seed, source_images, output_dir):
    """
    Append noise application entry to a central log file.

    Args:
        log_file: Path to central log file
        noise_type: Type of noise applied
        parameters: Noise parameters dict
        seed: Random seed
        source_images: List of source image paths
        output_dir: Output directory for noisy images
    """
    log_file = Path(log_file)

    # Load existing log or create new
    if log_file.exists():
        with open(log_file, 'r') as f:
            log_data = json.load(f)
    else:
        log_data = {
            'log_created': datetime.now().isoformat(),
            'entries': []
        }

    # Create new entry
    entry = {
        'entry_id': len(log_data['entries']),
        'timestamp': datetime.now().isoformat(),
        'noise_type': noise_type,
        'parameters': parameters,
        'random_seed': seed,
        'num_images': len(source_images),
        'source_images': [str(p) for p in source_images],
        'output_directory': str(output_dir),
        'python_version': sys.version.split()[0]
    }

    log_data['entries'].append(entry)

    # Save updated log
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)

    return entry


def create_noise_parameter_summary(log_entries):
    """
    Create a human-readable summary of noise parameters from log entries.

    Args:
        log_entries: List of log entries from noise application

    Returns:
        str: Formatted summary text
    """
    summary_lines = []
    summary_lines.append("=" * 70)
    summary_lines.append("NOISE APPLICATION SUMMARY")
    summary_lines.append("=" * 70)
    summary_lines.append(f"Total Applications: {len(log_entries)}")
    summary_lines.append("")

    for i, entry in enumerate(log_entries, 1):
        summary_lines.append(f"[{i}] {entry['noise_type'].upper()}")
        summary_lines.append(f"    Timestamp: {entry['timestamp']}")
        summary_lines.append(f"    Seed: {entry['random_seed']}")
        summary_lines.append(f"    Parameters:")

        for key, value in entry['parameters'].items():
            summary_lines.append(f"      - {key}: {value}")

        if 'num_images' in entry:
            summary_lines.append(f"    Images processed: {entry['num_images']}")
        if 'output_directory' in entry:
            summary_lines.append(f"    Output: {entry['output_directory']}")

        summary_lines.append("")

    summary_lines.append("=" * 70)

    return "\n".join(summary_lines)


def get_noise_configs_from_file(config_path):
    """
    Load noise configurations from JSON config file.

    Args:
        config_path: Path to noise configuration JSON file

    Returns:
        dict: Noise configurations by type
    """
    with open(config_path, 'r') as f:
        config = json.load(f)

    return config.get('noise_types', {})


def load_active_noise_params(config_path=None):
    """
    Load active noise parameters from config file.

    Args:
        config_path: Path to active params file (default: config/active_noise_params.json)

    Returns:
        dict: Config with current_params, random_seed, and data_paths
    """
    if config_path is None:
        # Default to project config
        script_dir = Path(__file__).parent
        config_path = script_dir.parent / 'config' / 'active_noise_params.json'

    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Active noise params file not found: {config_path}")

    with open(config_path, 'r') as f:
        config = json.load(f)

    return config


def get_enabled_noise_types(config):
    """
    Get list of enabled noise types from active params config.

    Args:
        config: Active params config dict

    Returns:
        list: List of (noise_type, params) tuples for enabled types
    """
    enabled = []
    current_params = config.get('current_params', {})

    for noise_type, params in current_params.items():
        if params.get('enabled', True):
            # Remove 'enabled' from params dict
            noise_params = {k: v for k, v in params.items() if k != 'enabled'}
            enabled.append((noise_type, noise_params))

    return enabled


def format_output_folder_name(noise_type, parameters):
    """
    Generate standardized output folder name based on noise type and parameters.

    Args:
        noise_type: Type of noise
        parameters: Noise parameters dict

    Returns:
        str: Formatted folder name
    """
    if noise_type == 'gaussian':
        sigma = parameters.get('sigma', 10)
        return f"gaussian_sigma{int(sigma)}"

    elif noise_type == 'poisson':
        lambda_val = parameters.get('lambda', 1)
        return f"poisson_lambda{int(lambda_val)}"

    elif noise_type == 'saltpepper':
        density = parameters.get('density', 0.01)
        # Format density as integer (0.01 -> 001, 0.05 -> 005, 0.1 -> 010)
        density_int = int(density * 100)
        return f"saltpepper_d{density_int:03d}"

    elif noise_type == 'speckle':
        variance = parameters.get('variance', 0.01)
        # Format variance as integer (0.01 -> 001, 0.05 -> 005, 0.1 -> 010)
        var_int = int(variance * 100)
        return f"speckle_var{var_int:03d}"

    else:
        return f"{noise_type}_default"
