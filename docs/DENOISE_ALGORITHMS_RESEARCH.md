# Denoising Algorithms Research - Thermal Imagery

## Overview

Thermal/IR imagery has specific characteristics that affect denoising algorithm selection:
- Lower resolution than visible imagery
- Different noise characteristics (sensor noise, quantization)
- Edge preservation is critical (thermal boundaries indicate temperature gradients)
- Often grayscale (single channel)
- Limited dynamic range in some sensors

## Candidate Algorithms

### 1. Median Filter

**Type**: Classical non-linear filter

**How it works**: Replaces each pixel with the median value in a local neighborhood

**Strengths**:
- Excellent for salt-and-pepper noise removal
- Preserves edges better than linear filters
- Simple and fast
- No parameter tuning beyond kernel size

**Weaknesses**:
- Can blur fine details
- Not effective for Gaussian noise
- May remove small features

**Suitable for thermal imagery**: ✓ Good
- Preserves thermal edges well
- Fast processing suitable for thermal video streams
- Effective for dead/hot pixel removal (common in thermal sensors)

**Best for**: Salt-and-pepper noise, impulse noise

**Parameters**:
- Kernel size (must be odd): 3, 5, 7, 9

---

### 2. Bilateral Filter

**Type**: Classical edge-preserving filter

**How it works**: Spatial averaging that preserves edges by weighting pixels based on both spatial distance and intensity similarity

**Strengths**:
- Excellent edge preservation
- Smooths noise while maintaining boundaries
- Works well with Gaussian noise
- Preserves fine details

**Weaknesses**:
- Computationally expensive
- Multiple parameters to tune
- Can introduce artifacts at high parameter values

**Suitable for thermal imagery**: ✓✓ Excellent
- Edge preservation critical for thermal boundaries
- Maintains temperature gradients
- Smooths sensor noise without blurring thermal features

**Best for**: Gaussian noise, read noise

**Parameters**:
- d: Diameter of pixel neighborhood (5, 9, 15)
- sigmaColor: Filter sigma in color space (75, 100, 150)
- sigmaSpace: Filter sigma in coordinate space (75, 100, 150)

---

### 3. Non-Local Means (NLM)

**Type**: Advanced patch-based filter

**How it works**: Denoises by averaging similar patches found throughout the image, not just local neighbors

**Strengths**:
- Superior performance on textured regions
- Preserves fine details and edges
- Works well with Gaussian noise
- State-of-the-art among classical methods

**Weaknesses**:
- Very computationally expensive
- Multiple parameters to tune
- Can over-smooth if parameters not tuned

**Suitable for thermal imagery**: ✓✓ Excellent
- Thermal scenes often have repetitive patterns (buildings, objects)
- Preserves texture information
- Excellent for sensor noise reduction

**Best for**: Gaussian noise, Poisson noise

**Parameters**:
- h: Filter strength (5, 10, 15, 20)
- templateWindowSize: Template patch size (7, 9, 11)
- searchWindowSize: Search area size (21, 31, 41)

---

### 4. Gaussian Filter

**Type**: Classical linear filter

**How it works**: Convolution with Gaussian kernel

**Strengths**:
- Very fast
- Simple to implement
- Well-understood behavior
- Good for uniform noise

**Weaknesses**:
- Blurs edges significantly
- Not suitable when edge preservation needed
- Poor performance on impulse noise

**Suitable for thermal imagery**: ✗ Limited
- Blurs thermal boundaries (bad for thermal analysis)
- Not recommended for thermal imagery analysis
- Only useful for severe noise with no edge requirements

**Best for**: High-frequency noise when edge preservation not needed

**Parameters**:
- Kernel size: 3, 5, 7
- Sigma: 0.5, 1.0, 2.0

---

### 5. Wiener Filter

**Type**: Classical optimal filter (frequency domain)

**How it works**: Minimizes mean square error assuming known noise and signal statistics

**Strengths**:
- Theoretically optimal for Gaussian noise
- Good PSNR performance
- Works well when noise characteristics known

**Weaknesses**:
- Requires noise variance estimation
- Can over-smooth
- Assumes stationary statistics
- Complex implementation

**Suitable for thermal imagery**: ✓ Moderate
- Good if noise characteristics well-known
- Useful for sensor-specific noise models
- Computational cost moderate

**Best for**: Gaussian noise with known statistics

**Parameters**:
- Noise variance estimate
- Window size for local statistics

---

### 6. Wavelet Denoising

**Type**: Advanced transform-domain method

**How it works**: Transform to wavelet domain, threshold coefficients, inverse transform

**Strengths**:
- Excellent edge preservation
- Multi-scale decomposition
- Good for various noise types
- Theoretical foundation

**Weaknesses**:
- Many parameters (wavelet type, levels, threshold method)
- Can introduce ringing artifacts
- Requires careful tuning

**Suitable for thermal imagery**: ✓✓ Excellent
- Multi-scale matches thermal features
- Preserves edges at all scales
- Effective for mixed noise types
- No blurring of thermal boundaries

**Best for**: Gaussian noise, mixed noise

**Parameters**:
- Wavelet family: 'db4', 'haar', 'sym8', 'coif1'
- Decomposition level: 2, 3, 4, 5
- Threshold method: 'soft', 'hard'
- Threshold type: 'BayesShrink', 'VisuShrink'

---

### 7. Total Variation (TV) Denoising

**Type**: Advanced variational method

**How it works**: Minimizes total variation while preserving data fidelity

**Strengths**:
- Excellent edge preservation
- Piecewise-constant regions preserved
- Good theoretical properties
- Effective for various noise types

**Weaknesses**:
- Can create "staircase" artifacts
- Iterative (can be slow)
- Single parameter but requires tuning

**Suitable for thermal imagery**: ✓✓ Excellent
- Thermal scenes often piecewise constant
- Preserves sharp thermal boundaries
- No edge blurring
- Well-suited to thermal characteristics

**Best for**: Gaussian noise, preserving discontinuities

**Parameters**:
- Weight/lambda: 0.05, 0.1, 0.2, 0.3

---

### 8. BM3D (Block-Matching and 3D Filtering)

**Type**: State-of-the-art classical method

**How it works**: Groups similar patches into 3D arrays, collaborative filtering in transform domain

**Strengths**:
- Best PSNR among classical methods
- Excellent visual quality
- Preserves fine details
- Works across noise levels

**Weaknesses**:
- Computationally expensive
- Complex algorithm
- Limited parameter tuning
- May over-smooth at low noise

**Suitable for thermal imagery**: ✓✓✓ Outstanding
- Best objective performance
- Excellent edge preservation
- Handles thermal texture well
- Industry standard for quality

**Best for**: All noise types, especially Gaussian

**Parameters**:
- sigma_psd: Noise standard deviation (should match noise level)
- profile: 'np' (normal), 'lc' (low complexity), 'high' (high quality)

---

### 9. Anisotropic Diffusion

**Type**: Advanced PDE-based method

**How it works**: Diffusion process that smooths within regions but not across edges

**Strengths**:
- Excellent edge preservation
- Adaptive smoothing
- Multi-scale effect
- No kernel size limitation

**Weaknesses**:
- Iterative (slower)
- Multiple parameters
- Can be unstable
- Requires careful tuning

**Suitable for thermal imagery**: ✓✓ Excellent
- Adapts to thermal structure
- Preserves thermal gradients
- Smooths uniform regions
- Good for thermal analysis

**Best for**: Gaussian noise, edge-aware smoothing

**Parameters**:
- niter: Number of iterations (10, 20, 50)
- kappa: Conduction coefficient (20, 50, 100)
- gamma: Rate of diffusion (0.1, 0.2)
- option: Edge detection function (1, 2)

---

## Algorithm Selection Guide

### By Noise Type

**Gaussian Noise**:
1. BM3D (best quality)
2. Non-Local Means (good quality, slower)
3. Wavelet (good quality, fast)
4. Bilateral (fast, good quality)

**Poisson Noise**:
1. Non-Local Means
2. BM3D
3. Wavelet

**Salt-and-Pepper Noise**:
1. Median filter (best)
2. Bilateral filter
3. Non-Local Means

**Speckle Noise**:
1. BM3D
2. Wavelet
3. Total Variation

### By Priority

**Best Quality (computational cost not critical)**:
1. BM3D
2. Non-Local Means
3. Wavelet denoising

**Best Speed**:
1. Median filter
2. Gaussian filter
3. Bilateral filter (GPU-accelerated)

**Best Edge Preservation**:
1. Total Variation
2. BM3D
3. Bilateral filter
4. Anisotropic diffusion

**Best for Thermal Imagery Specifically**:
1. BM3D
2. Bilateral filter
3. Total Variation
4. Wavelet denoising

## Implementation Availability

### Already Installed (from pyproject.toml)

**OpenCV** (`opencv-python`):
- Median filter: `cv2.medianBlur()`
- Bilateral filter: `cv2.bilateralFilter()`
- Non-Local Means: `cv2.fastNlMeansDenoising()`
- Gaussian filter: `cv2.GaussianBlur()`

**scikit-image**:
- Total Variation: `skimage.restoration.denoise_tv_chambolle()`
- Bilateral: `skimage.restoration.denoise_bilateral()`
- Wavelet: `skimage.restoration.denoise_wavelet()`
- Non-Local Means: `skimage.restoration.denoise_nl_means()`
- Wiener: `skimage.restoration.wiener()`

**ptwt** (PyTorch Wavelet Toolbox):
- Wavelet transforms: `ptwt.wavedec2()`, `ptwt.waverec2()`
- Custom wavelet denoising implementation

**bm3d**:
- BM3D: `bm3d.bm3d()`
- BM3D PSNR: `bm3d.bm3d_psnr()`

### Recommended Implementation Stack

**Primary algorithms to implement**:
1. Median filter (OpenCV - fast)
2. Bilateral filter (OpenCV - fast, GPU option)
3. Non-Local Means (OpenCV - optimized)
4. BM3D (bm3d package - best quality)
5. Wavelet (scikit-image - versatile)
6. Total Variation (scikit-image - edge preserving)

**Secondary (if time permits)**:
7. Anisotropic diffusion (custom or scikit-image)
8. Gaussian filter (baseline comparison)

## Recommendations for Thermal Imagery Study

### Must Test (Priority 1)
1. **BM3D**: Best overall performance expected
2. **Bilateral**: Fast, edge-preserving, good for real-time
3. **Non-Local Means**: Excellent quality, good for texture
4. **Median**: Fast baseline, good for impulse noise

### Should Test (Priority 2)
5. **Wavelet**: Good quality, interesting for multi-scale analysis
6. **Total Variation**: Edge preservation, good for piecewise-constant thermal scenes

### Optional (Priority 3)
7. **Anisotropic Diffusion**: Research interest
8. **Gaussian**: Baseline for comparison

## Expected Performance on Thermal Imagery

Based on literature and thermal imaging characteristics:

**For Gaussian Noise** (σ=5-20):
- BM3D: Best PSNR/SSIM
- NLM: Second best quality
- Bilateral: Good quality, fastest
- Median: Poor (not designed for Gaussian)

**For Poisson Noise**:
- BM3D: Best overall
- NLM: Excellent
- Wavelet: Good
- TV: Good

**For Salt-and-Pepper** (density 0.01-0.1):
- Median: Best
- Bilateral: Good for low density
- NLM: Good but slow
- Others: Poor

**For Speckle**:
- BM3D: Best
- Wavelet: Good
- TV: Good
- Bilateral: Moderate

## Next Steps

1. Implement parameter configuration file for all algorithms
2. Create denoising application scripts
3. Define parameter sweep ranges for optimization
4. Apply to all 11 noise variations
5. Measure and compare performance
