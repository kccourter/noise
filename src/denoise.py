#!/usr/bin/env python3
"""
Denoising algorithms for thermal imagery.

Implements Priority 1 and Priority 2 algorithms:
- Priority 1: BM3D, Bilateral, NLM, Median
- Priority 2: Wavelet, Total Variation
"""

import numpy as np
import cv2
import bm3d
from skimage.restoration import (
    denoise_tv_chambolle,
    denoise_wavelet as skimage_denoise_wavelet,
    denoise_nl_means,
    estimate_sigma
)


# ============================================================================
# PRIORITY 1 ALGORITHMS
# ============================================================================

def denoise_median(image, ksize=5):
    """
    Apply median filter denoising.

    Best for: Salt-and-pepper noise, impulse noise

    Args:
        image: Input image (uint8, 0-255)
        ksize: Kernel size (must be odd): 3, 5, 7, 9

    Returns:
        Denoised image (uint8)
    """
    if ksize % 2 == 0:
        raise ValueError("Kernel size must be odd")

    denoised = cv2.medianBlur(image, ksize)
    return denoised


def denoise_bilateral(image, d=9, sigma_color=75, sigma_space=75):
    """
    Apply bilateral filter denoising.

    Best for: Gaussian noise, edge preservation

    Args:
        image: Input image (uint8, 0-255)
        d: Diameter of pixel neighborhood (5, 9, 15)
        sigma_color: Filter sigma in color space (75, 100, 150)
        sigma_space: Filter sigma in coordinate space (75, 100, 150)

    Returns:
        Denoised image (uint8)
    """
    denoised = cv2.bilateralFilter(image, d, sigma_color, sigma_space)
    return denoised


def denoise_nlm(image, h=10, template_window_size=7, search_window_size=21):
    """
    Apply Non-Local Means denoising (OpenCV implementation - fast).

    Best for: Gaussian noise, Poisson noise, texture preservation

    Args:
        image: Input image (uint8, 0-255)
        h: Filter strength (5, 10, 15, 20) - higher removes more noise
        template_window_size: Template patch size (7, 9, 11) - must be odd
        search_window_size: Search area size (21, 31, 41) - must be odd

    Returns:
        Denoised image (uint8)
    """
    denoised = cv2.fastNlMeansDenoising(
        image,
        None,
        h=h,
        templateWindowSize=template_window_size,
        searchWindowSize=search_window_size
    )
    return denoised


def denoise_bm3d(image, sigma_psd, stage='all', profile='np'):
    """
    Apply BM3D denoising (state-of-the-art).

    Best for: All noise types, especially Gaussian - highest quality

    Args:
        image: Input image (uint8, 0-255)
        sigma_psd: Noise standard deviation on 0-1 scale
                   For noise σ on 0-255 scale, use sigma_psd = σ/255
                   Examples: σ=10 → sigma_psd=10/255 ≈ 0.039
                            σ=15 → sigma_psd=15/255 ≈ 0.059
        stage: 'all' (both stages), 'hard' (step 1), 'wiener' (step 2)
        profile: 'np' (normal), 'lc' (low complexity), 'high' (best quality)

    Returns:
        Denoised image (uint8)
    """
    # Convert to float 0-1
    image_float = image.astype(np.float32) / 255.0

    # Select stage
    if stage == 'all':
        stage_arg = bm3d.BM3DStages.ALL_STAGES
    elif stage == 'hard':
        stage_arg = bm3d.BM3DStages.HARD_THRESHOLDING
    elif stage == 'wiener':
        stage_arg = bm3d.BM3DStages.WIENER_FILTERING
    else:
        stage_arg = bm3d.BM3DStages.ALL_STAGES

    # Apply BM3D
    denoised_float = bm3d.bm3d(
        image_float,
        sigma_psd=sigma_psd,
        stage_arg=stage_arg,
        profile=profile
    )

    # Convert back to uint8
    denoised = (np.clip(denoised_float, 0, 1) * 255).astype(np.uint8)
    return denoised


# ============================================================================
# PRIORITY 2 ALGORITHMS
# ============================================================================

def denoise_wavelet(image, wavelet='db4', mode='soft', sigma=None):
    """
    Apply wavelet denoising.

    Best for: Gaussian noise, multi-scale analysis, edge preservation

    Args:
        image: Input image (uint8, 0-255)
        wavelet: Wavelet family ('db4', 'haar', 'sym8', 'coif1')
        mode: Thresholding mode ('soft', 'hard')
        sigma: Noise standard deviation estimate (None = auto-estimate)

    Returns:
        Denoised image (uint8)
    """
    # Convert to float 0-1
    image_float = image.astype(np.float32) / 255.0

    # Estimate sigma if not provided
    if sigma is None:
        sigma = estimate_sigma(image_float, channel_axis=None)
    else:
        # Convert from 0-255 scale to 0-1 scale
        sigma = sigma / 255.0

    # Apply wavelet denoising
    denoised_float = skimage_denoise_wavelet(
        image_float,
        sigma=sigma,
        wavelet=wavelet,
        mode=mode,
        rescale_sigma=True
    )

    # Convert back to uint8
    denoised = (np.clip(denoised_float, 0, 1) * 255).astype(np.uint8)
    return denoised


def denoise_tv(image, weight=0.1, max_num_iter=200):
    """
    Apply Total Variation denoising.

    Best for: Gaussian noise, piecewise-constant images, edge preservation

    Args:
        image: Input image (uint8, 0-255)
        weight: Denoising weight (0.05, 0.1, 0.2, 0.3)
                Higher = more denoising, lower = preserve more detail
        max_num_iter: Maximum iterations (200 default)

    Returns:
        Denoised image (uint8)
    """
    # Convert to float 0-1
    image_float = image.astype(np.float32) / 255.0

    # Apply TV denoising
    denoised_float = denoise_tv_chambolle(
        image_float,
        weight=weight,
        max_num_iter=max_num_iter
    )

    # Convert back to uint8
    denoised = (np.clip(denoised_float, 0, 1) * 255).astype(np.uint8)
    return denoised


# ============================================================================
# ALGORITHM REGISTRY
# ============================================================================

DENOISE_ALGORITHMS = {
    # Priority 1
    'median': {
        'function': denoise_median,
        'priority': 1,
        'description': 'Median filter - best for salt-and-pepper noise',
        'best_for': ['saltpepper', 'impulse'],
        'default_params': {'ksize': 5}
    },
    'bilateral': {
        'function': denoise_bilateral,
        'priority': 1,
        'description': 'Bilateral filter - fast, edge-preserving',
        'best_for': ['gaussian'],
        'default_params': {'d': 9, 'sigma_color': 75, 'sigma_space': 75}
    },
    'nlm': {
        'function': denoise_nlm,
        'priority': 1,
        'description': 'Non-Local Means - excellent quality, texture preservation',
        'best_for': ['gaussian', 'poisson'],
        'default_params': {'h': 10, 'template_window_size': 7, 'search_window_size': 21}
    },
    'bm3d': {
        'function': denoise_bm3d,
        'priority': 1,
        'description': 'BM3D - state-of-the-art, best PSNR',
        'best_for': ['gaussian', 'poisson', 'speckle'],
        'default_params': {'sigma_psd': 0.039, 'stage': 'all', 'profile': 'np'}
    },

    # Priority 2
    'wavelet': {
        'function': denoise_wavelet,
        'priority': 2,
        'description': 'Wavelet denoising - multi-scale, edge-preserving',
        'best_for': ['gaussian', 'mixed'],
        'default_params': {'wavelet': 'db4', 'mode': 'soft', 'sigma': None}
    },
    'tv': {
        'function': denoise_tv,
        'priority': 2,
        'description': 'Total Variation - excellent edge preservation',
        'best_for': ['gaussian', 'piecewise_constant'],
        'default_params': {'weight': 0.1, 'max_num_iter': 200}
    }
}


def get_algorithm_info(algorithm_name):
    """Get information about a denoising algorithm."""
    if algorithm_name not in DENOISE_ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    return DENOISE_ALGORITHMS[algorithm_name]


def apply_denoise(image, algorithm_name, **params):
    """
    Apply specified denoising algorithm to image.

    Args:
        image: Input image (uint8, 0-255)
        algorithm_name: Algorithm to use (median, bilateral, nlm, bm3d, wavelet, tv)
        **params: Algorithm-specific parameters

    Returns:
        Denoised image (uint8)
    """
    algo_info = get_algorithm_info(algorithm_name)
    denoise_func = algo_info['function']

    # Merge default params with provided params
    final_params = {**algo_info['default_params'], **params}

    return denoise_func(image, **final_params)
