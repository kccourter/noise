# Noise - Image Denoising for Infrared Remote Sensing

Exploration and evaluation of noise removal techniques for synthetic and real-world infrared imagery, with focus on remote sensing applications.

## Overview

This project investigates various filtering algorithms for removing noise from infrared (IR) images while preserving signal integrity. The approach uses controlled synthetic data with known ground truth to quantitatively evaluate denoising performance before applying techniques to real-world remote sensing datasets.

## Motivation

Infrared remote sensing data suffers from multiple noise sources:
- **Shot noise**: Photon counting statistics
- **Read noise**: Electronic readout variations
- **Fixed-pattern noise**: Pixel-to-pixel sensitivity differences
- **Temporal noise**: Frame-to-frame variations

Effective noise removal improves downstream analysis (object detection, temperature measurement, change detection) but must not destroy actual signal content. This project evaluates algorithms using objective metrics against ground truth data.

## Approach

### 1. Synthetic Data Generation
- Create noise-free test patterns and geometric shapes as truth models
- Apply well-characterized noise models (Gaussian, Poisson, salt-and-pepper)
- Test denoising algorithms with known ground truth for quantitative evaluation

### 2. Real-World Data Testing
- Download public IR remote sensing datasets (Landsat-8 TIRS, MODIS, Sentinel-3)
- Apply algorithms validated on synthetic data
- Assess performance on real noise characteristics

### 3. Objective Evaluation
- **PSNR** (Peak Signal-to-Noise Ratio): Overall fidelity
- **SSIM** (Structural Similarity Index): Perceptual quality
- **MSE** (Mean Squared Error): Pixel-level accuracy
- Edge preservation analysis to verify signal retention

## Target Data Specifications

**Infrared Remote Sensing Formats:**
- Bit depth: 12-bit, 14-bit, 16-bit unsigned
- Dimensions: 640×512 (standard), 1024×768 (high-res)
- Spectral bands: LWIR (8-14μm), MWIR (3-5μm)
- Formats: TIFF/GeoTIFF, HDF5, NetCDF

## Technology Stack

- **Python**: Primary implementation language for rapid iteration
- **NumPy**: Array operations and noise generation
- **scikit-image**: Image processing and metric calculation
- **Pillow/OpenCV**: Image I/O and manipulation
- **Matplotlib**: Visualization and comparison

## Project Status

**Current Phase**: Test data planning and infrastructure setup

See [docs/C_TEST_DATA.md](docs/C_TEST_DATA.md) for detailed test data generation and organization plan.

## Directory Structure

```
data/
├── synthetic/          # Generated test data with ground truth
│   ├── truth/         # Noise-free originals
│   └── noisy/         # Known noise models applied
├── real/              # Downloaded remote sensing datasets
│   ├── raw/           # Original data
│   └── noisy/         # Real data + synthetic noise
└── results/           # Denoised outputs and metrics

docs/                  # Planning and documentation
src/                   # Python implementation
```

## Goals

- **NOT** building production denoising software
- **YES** exploring and comparing filtering techniques
- **YES** understanding trade-offs between noise removal and signal preservation
- **YES** quantitative evaluation using reproducible methods

## Design Principles

- Minimize code complexity
- Iterate quickly with Python
- Validate assumptions with objective metrics
- Document parameters and seeds for reproducibility
- Preserve raw data; never modify originals

## Future Considerations

C++ and CUDA optimization deferred until algorithmic approach validated on Python implementation.
