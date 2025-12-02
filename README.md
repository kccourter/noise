# Noise - Thermal Image Denoising Study

Comprehensive evaluation of denoising algorithms for thermal infrared imagery using controlled noise models and quantitative metrics.

## Overview

This project evaluates denoising algorithm performance on thermal imagery corrupted by well-characterized noise models. Using real thermal images from the FLIR ADAS dataset, we apply controlled noise, measure baseline and degraded metrics, then test multiple denoising algorithms to quantify their effectiveness.

## Motivation

Thermal infrared sensors are affected by multiple noise sources that degrade image quality and downstream analysis:
- **Read noise (Gaussian)**: Electronic readout variations from sensor amplifiers
- **Shot noise (Poisson)**: Photon counting statistics inherent to imaging
- **Fixed-pattern noise**: Dead/hot pixels and pixel-to-pixel sensitivity variations
- **Speckle noise**: Multiplicative noise affecting coherent imaging systems

Effective denoising must remove noise while preserving critical thermal features like edges (temperature gradients) and texture. This study provides quantitative comparison of classical and advanced denoising algorithms on thermal imagery.

## Approach

### 1. Test Data Acquisition
- Source: **FLIR ADAS v2 Dataset** (thermal imagery for autonomous driving)
- Dataset: Real-world thermal images (8-bit, grayscale)
- Location: `~/data/noise/thermal/original/`

### 2. Baseline Characterization
- Measure quality metrics on original thermal images before noise addition
- Metrics: Mean intensity, standard deviation, sharpness (Laplacian variance), estimated noise sigma, entropy, edge density, dynamic range utilization
- Establishes ground truth for comparison

### 3. Controlled Noise Application
Four statistical noise models implemented with configurable parameters:

**Gaussian Noise**
- Simulates: Read noise, amplifier noise
- Parameter: Ïƒ (standard deviation)
- Test levels: 5, 10, 15, 20

**Poisson Noise**
- Simulates: Shot noise, photon counting statistics
- Signal-dependent (variance = mean)
- Test level: Î» = 1

**Salt-and-Pepper Noise**
- Simulates: Dead/hot pixels, impulse noise
- Parameter: density (fraction of affected pixels)
- Test levels: 0.01, 0.05, 0.10

**Speckle Noise**
- Simulates: Multiplicative noise
- Parameter: variance
- Test levels: 0.01, 0.05, 0.10

**Total noise variations**: 11 different noise configurations

### 4. Denoising Algorithms
Six denoising algorithms implemented (Priority 1 and Priority 2):

#### Priority 1: Essential Algorithms

**1. Median Filter** (OpenCV)
- Best for: Salt-and-pepper noise, impulse noise
- Speed: Very fast
- Parameters: Kernel size (3, 5, 7)

**2. Bilateral Filter** (OpenCV)
- Best for: Gaussian noise with edge preservation
- Speed: Fast
- Parameters: Diameter, sigma_color, sigma_space

**3. Non-Local Means (NLM)** (OpenCV)
- Best for: Gaussian/Poisson noise, texture preservation
- Speed: Moderate
- Parameters: Filter strength (h), template window, search window

**4. BM3D** (bm3d package)
- Best for: All noise types - **state-of-the-art quality**
- Speed: Moderate-slow
- Expected: Best PSNR/SSIM performance
- Parameters: Noise sigma (matched to noise level), profile

#### Priority 2: Advanced Algorithms

**5. Wavelet Denoising** (scikit-image)
- Best for: Gaussian noise, multi-scale analysis
- Speed: Fast
- Parameters: Wavelet family (db4, haar, sym8), mode

**6. Total Variation (TV)** (scikit-image)
- Best for: Piecewise-constant images, sharp edges
- Speed: Moderate
- Parameters: Weight (regularization strength)

### 5. Quantitative Evaluation
Compare denoised results against original images using:
- **PSNR** (Peak Signal-to-Noise Ratio): Overall fidelity
- **SSIM** (Structural Similarity Index): Perceptual quality
- **MSE** (Mean Squared Error): Pixel-level accuracy
- **Edge preservation**: Critical for thermal analysis
- **Processing time**: Algorithm efficiency

## Technology Stack

**Core Libraries:**
- **NumPy**: Array operations, noise generation with reproducible seeds
- **OpenCV (cv2)**: Fast implementations of median, bilateral, NLM filters
- **scikit-image**: Metrics (PSNR, SSIM), wavelet denoising, TV denoising
- **bm3d**: State-of-the-art BM3D algorithm
- **Pillow**: Image I/O operations

**Data Management:**
- **JSON**: Parameter and metadata logging for full traceability
- Reproducible experiments with fixed random seeds

## Project Structure

```
data/noise/
â"œâ"€â"€ thermal/
â"‚   â"œâ"€â"€ original/              # Downloaded FLIR thermal images
â"‚   â"œâ"€â"€ noisy/                 # Noise-corrupted images (11 variations)
â"‚   â"‚   â"œâ"€â"€ gaussian_sigma5/
â"‚   â"‚   â"œâ"€â"€ gaussian_sigma10/
â"‚   â"‚   â"œâ"€â"€ gaussian_sigma15/
â"‚   â"‚   â"œâ"€â"€ gaussian_sigma20/
â"‚   â"‚   â"œâ"€â"€ poisson_lambda1/
â"‚   â"‚   â"œâ"€â"€ saltpepper_d001/
â"‚   â"‚   â"œâ"€â"€ saltpepper_d005/
â"‚   â"‚   â"œâ"€â"€ saltpepper_d010/
â"‚   â"‚   â"œâ"€â"€ speckle_var001/
â"‚   â"‚   â"œâ"€â"€ speckle_var005/
â"‚   â"‚   â""â"€â"€ speckle_var010/
â"‚   â""â"€â"€ denoised/              # Algorithm outputs
â"‚       â"œâ"€â"€ gaussian_sigma10/
â"‚       â"‚   â"œâ"€â"€ bm3d_sigma10/
â"‚       â"‚   â"œâ"€â"€ bilateral_d9_sc75_ss75/
â"‚       â"‚   â"œâ"€â"€ nlm_h10_t7_s21/
â"‚       â"‚   â"œâ"€â"€ wavelet_db4_soft/
â"‚       â"‚   â""â"€â"€ tv_w02/
â"‚       â""â"€â"€ [other noise types]/
â"œâ"€â"€ metrics/
â"‚   â"œâ"€â"€ baseline_metrics.json      # Original image metrics
â"‚   â"œâ"€â"€ noisy_metrics.json         # Noise-degraded metrics
â"‚   â""â"€â"€ denoised_metrics.json      # Denoised results metrics
â""â"€â"€ metadata/
    â"œâ"€â"€ noise_params.json          # Complete noise parameter log
    â"œâ"€â"€ denoise_params.json        # Complete denoising parameter log
    â""â"€â"€ baseline_metrics_summary.md

config/
â"œâ"€â"€ active_noise_params.json    # Editable noise configuration
â""â"€â"€ denoise_configs.json        # Algorithm parameters and mappings

src/
â"œâ"€â"€ noise_logger.py             # Parameter logging utilities
â"œâ"€â"€ denoise.py                  # Denoising algorithm implementations
â""â"€â"€ metrics.py                  # Quality metrics computation

scripts/
â"œâ"€â"€ apply_noise.py              # Apply noise to images
â"œâ"€â"€ generate_noise_suite.py     # Generate all 11 noise variations
â"œâ"€â"€ apply_denoise.py            # Apply denoising algorithms
â"œâ"€â"€ test_denoise.py             # Test all denoising algorithms
â"œâ"€â"€ test_active_params.py       # View current noise configuration
â""â"€â"€ measure_metrics.py          # Compute quality metrics

docs/
â"œâ"€â"€ NOISE_STUDY.md              # Noise types and organization
â"œâ"€â"€ APPLY_NOISE.md              # Noise application workflow
â"œâ"€â"€ ACTIVE_PARAMS_USAGE.md      # Configuration guide
â"œâ"€â"€ BASELINE_METRICS.md         # Baseline characterization
â"œâ"€â"€ DENOISE.md                  # Denoising workflow
â"œâ"€â"€ DENOISE_ALGORITHMS_RESEARCH.md  # Algorithm analysis
â""â"€â"€ DENOISE_IMPLEMENTATION_SUMMARY.md # Implementation details
```

## Current Status

### âœ" Completed

**Infrastructure**
- Noise parameter logging system with JSON metadata
- Configurable noise application (`active_noise_params.json`)
- Automated folder naming and organization
- Full traceability with timestamps and random seeds

**Baseline Characterization**
- Baseline metrics measured on original thermal images
- Mean intensity: 136.64 Â± 70.30
- Laplacian variance: 289.99 (sharpness)
- Estimated noise sigma: 13.34
- Entropy: 7.91 bits
- Results saved to `baseline_metrics.json`

**Noise Generation**
- 11 noise variations generated with reproducible seeds
- All noise types implemented: Gaussian (4 levels), Poisson, Salt-pepper (3 levels), Speckle (3 levels)
- Complete metadata logging for each variation

**Denoising Implementation**
- 6 algorithms fully implemented and tested
- Configuration system with noise-to-algorithm mappings
- Organized output structure by noise type and algorithm
- Parameter variation support for optimization studies

### â³ In Progress

**Metrics Measurement**
- Apply metrics to all noise-corrupted variants
- Apply metrics to all denoised results
- Log metrics in structured format

**Evaluation and Comparison**
- Calculate metric improvements (denoised vs noisy)
- Generate visualizations (PSNR/SSIM vs noise level)
- Create comparison matrices (algorithm vs noise type)
- Identify best algorithm per noise type

## Quick Start

### 1. View Current Configuration
```bash
python3 scripts/test_active_params.py
```

### 2. Generate All Noise Variations
```bash
python3 scripts/generate_noise_suite.py
```

### 3. Test Denoising Algorithms
```bash
python3 scripts/test_denoise.py
```

### 4. Apply Denoising
```bash
# Denoise specific noise type with all recommended algorithms
python3 scripts/apply_denoise.py --noise gaussian_sigma10 --algo all

# Denoise with specific algorithm
python3 scripts/apply_denoise.py --noise gaussian_sigma10 --algo bm3d --variation sigma10

# Batch process all noise types
python3 scripts/apply_denoise.py --noise all --algo all
```

### 5. Measure Metrics
```bash
# Measure baseline metrics
python3 scripts/measure_metrics.py ~/data/noise/thermal/original

# Measure metrics on noisy images
python3 scripts/measure_metrics.py ~/data/noise/thermal/noisy/gaussian_sigma10

# Measure metrics on denoised results
python3 scripts/measure_metrics.py ~/data/noise/thermal/denoised/gaussian_sigma10/bm3d_sigma10
```

## Reproducibility

All experiments are fully reproducible:
- **Fixed random seed**: 42 (configurable in `active_noise_params.json`)
- **Complete parameter logging**: Every noise/denoise operation logged with timestamp
- **Version tracking**: Python version and library versions recorded
- **Metadata preservation**: All parameters saved with outputs

To replicate experiments:
1. Use same random seed
2. Apply same noise parameters from logged metadata
3. Apply same denoising parameters from config files

## Expected Outcomes

Based on algorithm research and thermal imagery characteristics:

**For Gaussian Noise** (most common in thermal sensors):
- BM3D: Best PSNR/SSIM (state-of-the-art)
- Non-Local Means: Excellent quality, preserves texture
- Bilateral: Good quality, fastest

**For Salt-and-Pepper** (dead/hot pixels):
- Median: Best performance
- Others: Limited effectiveness

**For Poisson Noise** (photon statistics):
- BM3D: Best overall
- NLM: Excellent
- Wavelet: Good

**Trade-offs**:
- BM3D: Best quality but slowest
- Median: Fastest but limited to impulse noise
- Bilateral: Good balance of speed and quality

## Design Principles

- **Objective evaluation**: Quantitative metrics over subjective assessment
- **Reproducibility**: Fixed seeds, complete parameter logging
- **Traceability**: Every step documented and reversible
- **Modularity**: Independent noise/denoise/metrics modules
- **No destructive operations**: Original data never modified
- **Iterate quickly**: Python for rapid algorithm testing
- **Validate first**: Controlled noise before real-world application

## Future Work

- Complete metrics measurement on all noise/denoised variants
- Generate comprehensive comparison reports and visualizations
- Parameter optimization for each algorithm-noise combination
- Processing time benchmarks
- Apply validated techniques to additional thermal datasets
- Explore deep learning denoisers if warranted by classical algorithm limitations

## References

**Dataset**: FLIR ADAS v2 - Thermal imagery for autonomous driving research
- Source: https://adas-dataset-v2.flirconservator.com/

**Key Algorithms**:
- BM3D: Dabov et al., "Image Denoising by Sparse 3-D Transform-Domain Collaborative Filtering"
- Non-Local Means: Buades et al., "A non-local algorithm for image denoising"
- Bilateral Filter: Tomasi and Manduchi, "Bilateral filtering for gray and color images"

## License

This is a research and educational project exploring denoising techniques. Refer to individual dataset and library licenses for their respective usage terms.
