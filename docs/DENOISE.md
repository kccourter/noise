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