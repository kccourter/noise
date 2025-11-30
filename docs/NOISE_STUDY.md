### Common Noise Types in Thermal/IR Imagery

- **Shot noise (Poisson)**: Photon counting statistics
- **Read noise (Gaussian)**: Electronic readout noise
- **Fixed-pattern noise (FPN)**: Pixel-to-pixel sensitivity variations, dead/hot pixels
- **Salt-and-pepper noise**: Simulates dead/hot pixels
- **Speckle noise**: Multiplicative noise common in coherent imaging

### Statistical Noise Models to Implement

1. **Gaussian Noise**
   - Tunable parameters: mean (μ), standard deviation (σ)
   - Test multiple σ values: 5, 10, 15, 20 (intensity levels)

2. **Poisson Noise**
   - Tunable parameters: lambda (λ) scaling factor
   - Signal-dependent: variance equals mean

3. **Salt-and-Pepper Noise**
   - Tunable parameters: noise density (0-1)
   - Test densities: 0.01, 0.05, 0.1

4. **Speckle Noise**
   - Tunable parameters: variance
   - Test variance levels: 0.01, 0.05, 0.1


## Data Organization

Organize data to support the workflow and maintain traceability:

```
${DATA_FOLDER}/noise/}$
    ├── thermal/
    │   ├── original/
    │   ├── noisy/
    │   │   ├── gaussian_sigma5/
    │   │   ├── gaussian_sigma10/
    │   │   ├── gaussian_sigma15/
    │   │   ├── poisson_lambda1/
    │   │   ├── saltpepper_d001/
    │   │   ├── saltpepper_d005/
    │   │   └── speckle_var001/
    │   └── denoised/
    │       ├── gaussian_sigma5/
    │       │   ├── median_k3/
    │       │   ├── median_k5/
    │       │   ├── bilateral_d9_sc75_ss75/
    │       │   ├── nlm_h10_ps7_pd21/
    │       │   └── wavelet_db4_l3/
    │       ├── gaussian_sigma10/
    │       │   └── [same algorithm variants]
    │       └── ...
    ├── metrics/
    │   ├── baseline_metrics.json      # Original images
    │   ├── noisy_metrics.json         # Noise-corrupted images
    │   └── denoised_metrics.json      # Denoised results
    └── metadata/
        ├── noise_params.json          # Tracks noise parameters and seeds
        ├── denoise_params.json        # Tracks denoising parameters
        └── dataset_info.json          # Roboflow dataset metadata
```

## Python Packages and Tools

### Required Packages

**Image I/O and Processing:**
- Pillow / PIL - Basic image operations
- OpenCV (cv2) - Advanced image processing
- imageio - Flexible image reading/writing
- scikit-image - Image processing algorithms

**Noise Generation:**
- NumPy - Core array operations and random number generation
- scikit-image.util.random_noise - Built-in noise functions

**Denoising:**
- scikit-image.restoration - denoise_tv_chambolle, denoise_bilateral, etc.
- OpenCV - medianBlur, bilateralFilter, fastNlMeansDenoising
- PyWavelets - Wavelet-based denoising
- bm3d - BM3D algorithm implementation

**Metrics Computation:**
- scikit-image.metrics - PSNR, SSIM, MSE
- NumPy - Custom metric implementations

**Roboflow Integration:**
- roboflow - API for dataset download
- requests - Manual API calls if needed

**Data Management:**
- pandas - Metrics tracking and analysis
- json - Metadata logging

**Visualization:**
- matplotlib - Plotting and visualization
- seaborn - Statistical visualizations (optional)

### Tasks

- [ ] Create requirements.txt with all dependencies
- [ ] Document any format conversion needs for thermal imagery
- [ ] Test compatibility with different bit depths (8-bit, 16-bit)
- [ ] Create utility functions for format conversion if needed

## Reproducibility

### Tasks

- [ ] Fix random seeds for all stochastic processes (NumPy, Python random)
- [ ] Log Python version and library versions in metadata
- [ ] Create requirements.txt or environment.yml
- [ ] Document dataset version/download date from Roboflow
- [ ] Store all experiment configurations in version-controlled config files
