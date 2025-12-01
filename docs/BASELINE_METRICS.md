
## Identify Baseline Metrics Measurement

Before adding any noise, establish baseline quality metrics on the downloaded thermal imagery.

### Tasks

- [x] Recommend basic metrics for characterizing thermal image quality:

### Recommended Baseline Metrics

**1. Statistical Metrics**
- Mean intensity: Average pixel value (characterizes overall brightness)
- Standard deviation: Intensity variation (indicates contrast/dynamic range usage)
- Min/Max values: Intensity range (shows dynamic range utilization)
- Histogram distribution: Full intensity distribution (identifies clipping, bimodal distributions)

**2. Sharpness Metrics**
- Laplacian variance: Measures edge sharpness (higher = sharper)
- Gradient magnitude: Edge content and strength
- Useful for: Detecting blur, focus issues, or processing artifacts

**3. Contrast Metrics**
- Michelson contrast: (max - min) / (max + min)
- RMS contrast: Standard deviation of normalized intensities
- Local contrast: Spatial variation within regions

**4. Noise Estimation**
- Estimated noise sigma: Inherent sensor noise level
- Method: Use robust median absolute deviation (MAD) on high-frequency components
- Provides baseline for comparison with added noise

**5. Information Content**
- Entropy: Measures information content (higher = more detail/texture)
- Edge density: Percentage of edge pixels (indicates scene complexity)

**6. Dynamic Range Utilization**
- Effective bit depth: Actual bits used vs available (8-bit)
- Histogram spread: Percentage of available range utilized
- Saturation: Percentage of clipped pixels (0 or 255)

**Rationale:**
- These metrics characterize thermal image quality without requiring reference images
- Establish baseline before noise injection
- Enable detection of dataset inconsistencies or quality issues
- Provide context for interpreting denoising performance

## Implement Baseline Metrics Measurements
- [x] Implement a Python metrics test script that takes an input image argument and runs either a specified metric measurent or the full suite if none is specified
- [x] Implement Python utilities to measure each metrics so they can be called individually

## Run baseline metrics
- [x] Run baseline metrics on downloaded dataset
- [x] Document baseline metric values for later comparison

**Results**:
- Baseline metrics saved to: `~/data/noise/metrics/baseline_metrics.json`
- Summary documentation: `~/data/noise/metadata/baseline_metrics_summary.md`
- Images processed: 1
- Timestamp: 2025-11-30

**Key Baseline Values**:
- Mean Intensity: 136.64 ± 70.30
- Laplacian Variance: 289.99 (sharpness)
- Estimated Noise Sigma: 13.34
- Entropy: 7.91 bits
- Edge Density: 17.62%
- Dynamic Range: 100% (full 8-bit utilization)
