
## Noise Characterization and Application

Apply well-characterized noise of several statistical types to the downloaded thermal imagery. This allows controlled testing of denoising algorithms.

### Tasks

- [ ] Identify Python packages for noise generation (NumPy, scikit-image)
- [ ] Implement noise application functions for each noise type
- [ ] Define random seed management strategy for reproducibility
- [ ] Create parameter logging system to track noise configurations:
  - Noise type
  - Parameters (σ, λ, density, etc.)
  - Random seed
  - Timestamp
- [ ] Generate noisy versions of dataset with multiple noise types/levels
- [ ] Create systematic naming convention for noisy variants

## Metrics Measurement on Noisy Data

Measure the same quality metrics on noise-corrupted images to quantify degradation.

### Tasks

- [ ] Apply metric measurement to all noise-corrupted image variants
- [ ] Log metrics alongside noise parameters in structured format (JSON/CSV)
- [ ] Create visualization/comparison of metric degradation vs noise level:
  - PSNR vs noise level plots
  - SSIM vs noise level plots
  - Per noise-type comparison charts
- [ ] Document observations on how different noise types affect metrics
- [ ] Identify which metrics are most sensitive to which noise types

## Denoising

Apply various denoising algorithms to the noise-corrupted images.

### Candidate Denoising Algorithms

**Classical Filters:**
- Median filter
- Bilateral filter
- Non-local means (NLM)
- Gaussian filter
- Wiener filter

**Advanced Methods:**
- Wavelet-based denoising
- Total variation (TV) denoising
- BM3D (Block-Matching and 3D filtering)
- Anisotropic diffusion

**ML-Based (if time permits):**
- Deep learning denoisers (pre-trained models)

### Tasks

- [ ] Research and select 3-5 denoising algorithms suitable for thermal imagery
- [ ] Identify Python libraries/implementations:
  - scikit-image (median, bilateral, NLM, etc.)
  - OpenCV (various filters)
  - PyWavelets (wavelet denoising)
  - bm3d package
- [ ] Document tunable parameters for each algorithm
- [ ] Define parameter sweep ranges for algorithm optimization
- [ ] Apply denoising algorithms to all noise-corrupted variants
- [ ] Organize denoised outputs with clear naming convention
- [ ] Log denoising parameters used for each result

## Comparison and Evaluation

Compare denoised results with original downloaded images to evaluate algorithm performance.

### Tasks

- [ ] Measure all metrics on denoised images
- [ ] Calculate metric improvements (denoised vs noisy):
  - PSNR improvement
  - SSIM improvement
  - MSE reduction
- [ ] Calculate residual errors (denoised vs original):
  - Absolute difference maps
  - Error distribution histograms
- [ ] Create comparison visualizations:
  - Original vs Noisy vs Denoised side-by-side
  - Metric comparison tables
  - Per-algorithm performance bar charts
  - Noise-type vs algorithm performance matrices
- [ ] Generate evaluation report with:
  - Best-performing algorithm per noise type
  - Parameter recommendations
  - Visual quality assessment
  - Computational performance notes (runtime)
- [ ] Document trade-offs (quality vs speed, parameter sensitivity)

## Data Organization

Organize data to support the workflow and maintain traceability:

```
data/
    ├── thermal/
    │   ├── original/           # Downloaded 
    │   │   ├── train/
    │   │   ├── valid/
    │   │   └── test/
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
