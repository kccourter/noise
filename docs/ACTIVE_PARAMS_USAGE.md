# Active Noise Parameters Usage

## Overview

The `config/active_noise_params.json` file allows you to configure noise application parameters that persist between script runs. Edit this file to change which noise types are applied and their parameters.

## File Location

```
config/active_noise_params.json
```

## Structure

```json
{
  "random_seed": 42,
  "data_paths": {
    "source": "~/data/noise/thermal/original",
    "destination_base": "~/data/noise/thermal/noisy"
  },
  "current_params": {
    "gaussian": {
      "enabled": true,
      "sigma": 10
    },
    "poisson": {
      "enabled": true
    },
    "saltpepper": {
      "enabled": true,
      "density": 0.01
    },
    "speckle": {
      "enabled": true,
      "variance": 0.01
    }
  }
}
```

## Configuration Options

### Global Settings

- **random_seed**: Integer seed for reproducibility (default: 42)
- **data_paths.source**: Source directory with original images
- **data_paths.destination_base**: Base directory for noisy outputs

### Noise Type Parameters

#### Gaussian Noise
```json
"gaussian": {
  "enabled": true,
  "sigma": 10
}
```
- **enabled**: true/false to enable/disable
- **sigma**: Standard deviation (0-255 scale). Try: 5, 10, 15, 20

#### Poisson Noise
```json
"poisson": {
  "enabled": true
}
```
- **enabled**: true/false to enable/disable
- No additional parameters (signal-dependent noise)

#### Salt-and-Pepper Noise
```json
"saltpepper": {
  "enabled": true,
  "density": 0.01
}
```
- **enabled**: true/false to enable/disable
- **density**: Proportion of noisy pixels (0-1). Try: 0.01, 0.05, 0.1

#### Speckle Noise
```json
"speckle": {
  "enabled": true,
  "variance": 0.01
}
```
- **enabled**: true/false to enable/disable
- **variance**: Noise variance. Try: 0.01, 0.05, 0.1

## Usage Examples

### Example 1: Apply only Gaussian noise with sigma=15

```json
"current_params": {
  "gaussian": {
    "enabled": true,
    "sigma": 15
  },
  "poisson": {
    "enabled": false
  },
  "saltpepper": {
    "enabled": false,
    "density": 0.01
  },
  "speckle": {
    "enabled": false,
    "variance": 0.01
  }
}
```

### Example 2: Test heavy noise

```json
"current_params": {
  "gaussian": {
    "enabled": true,
    "sigma": 20
  },
  "poisson": {
    "enabled": true
  },
  "saltpepper": {
    "enabled": true,
    "density": 0.1
  },
  "speckle": {
    "enabled": true,
    "variance": 0.1
  }
}
```

### Example 3: Change random seed for different realization

```json
{
  "random_seed": 123,
  ...
}
```

## Testing Configuration

View current active parameters:
```bash
python3 scripts/test_active_params.py
```

This displays:
- Random seed
- Data paths
- Enabled noise types
- Parameters for each type
- Output folder names

## Output Folder Naming

Folders are automatically named based on noise type and parameters:
- Gaussian: `gaussian_sigma{value}` → `gaussian_sigma10`
- Poisson: `poisson_lambda{value}` → `poisson_lambda1`
- Salt-pepper: `saltpepper_d{formatted}` → `saltpepper_d001` (density 0.01)
- Speckle: `speckle_var{formatted}` → `speckle_var001` (variance 0.01)

## Workflow

1. Edit `config/active_noise_params.json` with desired parameters
2. Test configuration: `python3 scripts/test_active_params.py`
3. Apply noise using scripts (reads this config file)
4. Repeat with different parameters as needed

## Notes

- Changes to this file take effect immediately on next script run
- Keep backup copies for different experiment configurations
- All noise applications are logged with their parameters for traceability
