# Denoising Implementation Summary

## Overview

Implemented **6 denoising algorithms** (Priority 1 and Priority 2) for thermal imagery noise removal study.

## Implemented Algorithms

### Priority 1 (Essential)

#### 1. Median Filter
- **Function**: `denoise_median()`
- **Library**: OpenCV
- **Best for**: Salt-and-pepper noise, impulse noise
- **Parameters**: ksize (kernel size)
- **Variations**: k3, k5, k7
- **Speed**: Very fast
- **Edge preservation**: Good

#### 2. Bilateral Filter
- **Function**: `denoise_bilateral()`
- **Library**: OpenCV
- **Best for**: Gaussian noise, edge preservation
- **Parameters**: d (diameter), sigma_color, sigma_space
- **Variations**: Multiple d and sigma combinations
- **Speed**: Fast
- **Edge preservation**: Excellent

#### 3. Non-Local Means (NLM)
- **Function**: `denoise_nlm()`
- **Library**: OpenCV (optimized)
- **Best for**: Gaussian noise, Poisson noise, texture preservation
- **Parameters**: h (filter strength), template_window_size, search_window_size
- **Variations**: Multiple h and window size combinations
- **Speed**: Moderate
- **Edge preservation**: Excellent

#### 4. BM3D
- **Function**: `denoise_bm3d()`
- **Library**: bm3d package
- **Best for**: All noise types - **state-of-the-art quality**
- **Parameters**: sigma_psd (noise level), stage, profile
- **Variations**: Matched to noise levels (sigma5, sigma10, sigma15, sigma20)
- **Speed**: Moderate-slow
- **Edge preservation**: Excellent
- **Note**: Expected to have best PSNR/SSIM

### Priority 2 (Advanced)

#### 5. Wavelet Denoising
- **Function**: `denoise_wavelet()`
- **Library**: scikit-image
- **Best for**: Gaussian noise, multi-scale analysis
- **Parameters**: wavelet family, mode (soft/hard), sigma
- **Variations**: db4, haar, sym8
- **Speed**: Fast
- **Edge preservation**: Excellent

#### 6. Total Variation (TV)
- **Function**: `denoise_tv()`
- **Library**: scikit-image
- **Best for**: Gaussian noise, piecewise-constant images
- **Parameters**: weight, max_num_iter
- **Variations**: w01, w02, w03 (different weights)
- **Speed**: Moderate
- **Edge preservation**: Excellent (sharp boundaries)

## Module Structure

### `src/denoise.py`
Core denoising module with:
- Individual function for each algorithm
- `apply_denoise()` - unified interface
- `DENOISE_ALGORITHMS` - algorithm registry with metadata
- Consistent uint8 input/output (0-255)
- Automatic float conversion for algorithms requiring it

### `config/denoise_configs.json`
Configuration file containing:
- Parameter variations for each algorithm
- Noise-to-algorithm mappings
- Recommended parameter sets per noise type
- Default configurations

### `scripts/test_denoise.py`
Test script that:
- Tests all 6 algorithms
- Uses default parameters
- Saves test outputs
- Verifies each algorithm works

### `scripts/apply_denoise.py`
Application script that:
- Applies denoising to noisy images
- Supports single algorithm or all recommended algorithms
- Saves metadata with each result
- Organizes outputs by noise type and algorithm
- Can process single noise variant or all

## Usage Examples

### Test All Algorithms
```bash
python3 scripts/test_denoise.py
```

### Denoise with Specific Algorithm
```bash
# BM3D on gaussian_sigma10
python3 scripts/apply_denoise.py --noise gaussian_sigma10 --algo bm3d --variation sigma10

# Median filter on salt-pepper
python3 scripts/apply_denoise.py --noise saltpepper_d001 --algo median --variation k3
```

### Denoise with All Recommended Algorithms
```bash
# Uses config to apply best algorithms for this noise type
python3 scripts/apply_denoise.py --noise gaussian_sigma10 --algo all
```

### Batch Processing
```bash
# Process all noise variants with all recommended algorithms
python3 scripts/apply_denoise.py --noise all --algo all
```

## Output Organization

```
~/data/noise/thermal/denoised/
├── gaussian_sigma10/
│   ├── bm3d_sigma10/
│   │   ├── frame-000591.jpg
│   │   └── denoise_metadata.json
│   ├── bilateral_d9_sc75_ss75/
│   ├── nlm_h10_t7_s21/
│   └── wavelet_db4_soft/
├── saltpepper_d001/
│   ├── median_k3/
│   ├── bilateral_d9_sc75_ss75/
│   └── nlm_h10_t7_s21/
└── ...
```

## Noise-to-Algorithm Recommendations

Based on noise characteristics, the config provides optimal algorithm/parameter combinations:

**Gaussian Noise** (σ=5-20):
- BM3D (matched sigma_psd)
- Bilateral filter
- NLM
- Wavelet
- TV

**Poisson Noise**:
- BM3D
- NLM
- Wavelet

**Salt-and-Pepper** (density 0.01-0.1):
- **Median filter** (best)
- Bilateral
- NLM

**Speckle** (variance 0.01-0.1):
- BM3D
- Wavelet
- TV

## Performance Characteristics

### Speed (fastest to slowest)
1. Median
2. Bilateral
3. Wavelet
4. TV
5. NLM
6. BM3D

### Expected Quality (best to worst for Gaussian noise)
1. BM3D
2. NLM
3. Wavelet
4. Bilateral
5. TV
6. Median

### Edge Preservation (best to worst)
1. TV
2. BM3D
3. Bilateral
4. Wavelet
5. NLM
6. Median

## Testing Results

All 6 algorithms tested successfully:
- ✓ Median filter
- ✓ Bilateral filter
- ✓ Non-Local Means
- ✓ BM3D
- ✓ Wavelet denoising
- ✓ Total Variation

Test outputs saved to `test_output/`

## Next Steps

1. Apply denoising to all 11 noise variations
2. Measure metrics on denoised images
3. Compare performance (PSNR, SSIM, visual quality)
4. Generate comparison reports
5. Identify best algorithm per noise type
