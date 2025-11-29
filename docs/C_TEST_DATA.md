# Test Data Planning

To explore the removal of noise using various algorithms and tools, a variety of test data will be generated and downloaded. The focus is on data that is representative of Infrared remote sensing data.

## Generating truth data

Synthetic noise-free images containing test patterns and geometric shapes will be used as truth models. To these truth models, we will add well-characterized noise and then test different algorithms for removal of that noise. The de-noised data can be compared to the truth data to evaluate the performance of the algorithms.

### IR Remote Sensing Data Specifications

Target format specifications for synthetic test data generation:

- **Bit depth**: 12-bit, 14-bit, and 16-bit unsigned integers (typical for IR sensors)
- **Image dimensions**:
  - 640x512 (common for LWIR cameras)
  - 1024x768 (higher resolution sensors)
- **Spectral bands**:
  - LWIR (Long-Wave Infrared): 8-14μm
  - MWIR (Mid-Wave Infrared): 3-5μm
- **File formats**: TIFF (GeoTIFF for georeferenced), HDF5, NetCDF

### Tasks

- [ ] Search web for noise-free synthetic test images compatible with IR formats
- [ ] Identify Python libraries for generating geometric test shapes (e.g., scikit-image, Pillow, OpenCV)
- [ ] Create test pattern generators (checkerboard, edges, gradients, point sources)
- [ ] Generate truth dataset with varying complexity levels (simple to complex scenes)

## Downloaded Data

Additional free datasets representing real remote sensing Infrared band data should be located and instructions for downloading the data provided.

### Target Datasets

- [ ] Landsat-8 TIRS (Thermal Infrared Sensor) - 100m resolution, Band 10 & 11
- [ ] MODIS (Moderate Resolution Imaging Spectroradiometer) - thermal bands
- [ ] Sentinel-3 SLSTR (Sea and Land Surface Temperature Radiometer)

### Tasks

- [ ] Create download scripts using public APIs (e.g., USGS Earth Explorer, Copernicus Open Access Hub)
- [ ] Document licensing and attribution requirements
- [ ] Estimate total dataset size and storage requirements
- [ ] Define subset criteria (geographic region, time period) to limit data volume

## Plan for Applying Noise Sources to Test Data

Raw test data will have deterministic noise - representing fixed-source errors such as from sensor characteristics - as well as stochastic and other common noise patterns applied to it.

### Common Noise Types in IR Imagery

- **Shot noise (Poisson)**: Photon counting statistics
- **Read noise (Gaussian)**: Electronic readout noise
- **Fixed-pattern noise**: Pixel-to-pixel sensitivity variations, dead/hot pixels
- **1/f noise**: Low-frequency noise from electronics
- **Temporal noise**: Frame-to-frame variations

### Statistical Noise Models

1. **Gaussian Noise**
   - Tunable parameters: mean (μ), standard deviation (σ)
   - Typical σ values: 0.1-5% of signal range

2. **Poisson Noise**
   - Tunable parameters: lambda (λ) scaling factor
   - Signal-dependent: variance equals mean

3. **Salt-and-Pepper Noise**
   - Tunable parameters: noise density (0-1)
   - Simulates dead/hot pixels

### Tasks

- [ ] Identify Python packages for noise generation (NumPy, scikit-image, noise library)
- [ ] Implement noise application functions with parameter logging
- [ ] Define random seed management for reproducibility
- [ ] Create parameter sweep ranges for each noise model

## Evaluation Metrics

To quantify denoising algorithm performance, establish objective metrics comparing denoised output to truth data.

### Tasks

- [ ] Implement Peak Signal-to-Noise Ratio (PSNR) calculation
- [ ] Implement Structural Similarity Index (SSIM) calculation
- [ ] Implement Mean Squared Error (MSE) calculation
- [ ] Define acceptable threshold values for each metric
- [ ] Create visualization tools for side-by-side comparisons

## Validation Strategy

Ensure denoising algorithms preserve signal while removing noise.

### Tasks

- [ ] Define edge-preservation tests (compare edge maps before/after denoising)
- [ ] Create synthetic scenes with known features to verify feature retention
- [ ] Establish visual inspection protocol for real-world data
- [ ] Document signal vs. noise characteristics for IR imagery

## Organization

Directory structure to support both generated and downloaded datasets, preserving raw/original data with clear naming conventions for noise-added variants.

### Proposed Structure

```
data/
├── synthetic/
│   ├── truth/                    # Original noise-free images
│   │   ├── simple/               # Basic geometric patterns
│   │   ├── medium/               # Intermediate complexity
│   │   └── complex/              # Realistic scenes
│   └── noisy/
│       ├── gaussian_mu0_sigma1/
│       ├── gaussian_mu0_sigma5/
│       ├── poisson_lambda10/
│       └── saltpepper_density0.01/
├── real/
│   ├── raw/                      # Downloaded datasets
│   │   ├── landsat8/
│   │   ├── modis/
│   │   └── sentinel3/
│   └── noisy/                    # Real data with added synthetic noise
│       └── [same structure as synthetic/noisy]
├── results/                      # Denoised outputs
│   ├── algorithm_name/
│   │   └── [mirrors noisy structure]
│   └── metrics/                  # CSV/JSON with PSNR, SSIM, etc.
└── metadata.json                 # Tracks all parameters, seeds, timestamps
```

### Tasks

- [ ] Create directory structure initialization script
- [ ] Design metadata schema (JSON format with noise params, seeds, timestamps)
- [ ] Implement automatic metadata logging during noise application
- [ ] Create data manifest listing all available test datasets
- [ ] Estimate total storage requirements (target: <50GB for initial exploration)

## Reproducibility

- [ ] Fix random seeds for all stochastic processes
- [ ] Log Python/library versions in metadata
- [ ] Create requirements.txt or environment.yml
- [ ] Document hardware used for generation (if timing/performance relevant)
