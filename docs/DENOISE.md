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

- [x] Research and candidate denoising algorithms suitable for thermal imagery

**Research completed**: See `docs/DENOISE_ALGORITHMS_RESEARCH.md` for comprehensive analysis

**Summary**: Evaluated 9 denoising algorithms for thermal imagery suitability:

**Excellent for thermal imagery**:
1. BM3D - Best PSNR/SSIM, state-of-the-art
2. Bilateral Filter - Fast, edge-preserving
3. Non-Local Means - Excellent quality, preserves texture
4. Wavelet Denoising - Multi-scale, edge-preserving
5. Total Variation - Excellent edge preservation, piecewise-constant scenes
6. Anisotropic Diffusion - Adaptive edge-aware smoothing

**Good for specific cases**:
7. Median Filter - Best for salt-and-pepper/impulse noise
8. Wiener Filter - Good if noise statistics known

**Limited suitability**:
9. Gaussian Filter - Blurs edges, baseline only

**Recommended priority for implementation**:
- Priority 1: BM3D, Bilateral, NLM, Median
- Priority 2: Wavelet, Total Variation
- Priority 3: Anisotropic Diffusion, Gaussian (baseline)

- [x] Identify Python libraries/implementations:
  - scikit-image (median, bilateral, NLM, etc.)
  - OpenCV (various filters)
  - ptwt (Pytorch wavelet toolbox) (wavelet denoising)
  - bm3d package

**Implementation**: Created `src/denoise.py` module with all Priority 1 and Priority 2 algorithms:

**Priority 1 Algorithms** (Implemented):
- `denoise_median()` - OpenCV medianBlur
- `denoise_bilateral()` - OpenCV bilateralFilter
- `denoise_nlm()` - OpenCV fastNlMeansDenoising
- `denoise_bm3d()` - bm3d package

**Priority 2 Algorithms** (Implemented):
- `denoise_wavelet()` - scikit-image denoise_wavelet
- `denoise_tv()` - scikit-image denoise_tv_chambolle

All algorithms tested and verified working. Test outputs in `test_output/`

- [x] Document tunable parameters for each algorithm

**Parameters documented** in `src/denoise.py` and `config/denoise_configs.json`:

**Median**: ksize (3, 5, 7)
**Bilateral**: d (5, 9, 15), sigma_color (75, 100, 150), sigma_space (75, 100, 150)
**NLM**: h (5, 10, 15, 20), template_window_size (7, 9, 11), search_window_size (21, 31, 41)
**BM3D**: sigma_psd (matches noise level), stage (all/hard/wiener), profile (np/lc/high)
**Wavelet**: wavelet (db4, haar, sym8), mode (soft, hard), sigma (auto or specified)
**TV**: weight (0.05, 0.1, 0.2, 0.3), max_num_iter (200)

- [x] Define parameter sweep ranges for algorithm optimization

**Parameter variations defined** in `config/denoise_configs.json`:
- Multiple parameter sets per algorithm
- Noise-to-algorithm mapping with recommended parameters
- Example: gaussian_sigma10 → bm3d:sigma10, bilateral:d9_sc75_ss75, etc.

Scripts created:
- `scripts/test_denoise.py` - Test all algorithms
- `scripts/apply_denoise.py` - Apply denoising to noisy images
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