#!/usr/bin/env python3
"""
Baseline metrics for thermal image quality characterization.
"""

import numpy as np
import cv2
from scipy import ndimage
from skimage.filters import sobel


def compute_statistical_metrics(image):
    """
    Compute basic statistical metrics.

    Returns:
        dict: mean, std, min, max, histogram
    """
    return {
        'mean': float(np.mean(image)),
        'std': float(np.std(image)),
        'min': int(np.min(image)),
        'max': int(np.max(image)),
        'histogram': np.histogram(image, bins=256, range=(0, 256))[0].tolist()
    }


def compute_laplacian_variance(image):
    """
    Compute Laplacian variance as a sharpness metric.
    Higher values indicate sharper images.

    Returns:
        float: Laplacian variance
    """
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    return float(np.var(laplacian))


def compute_gradient_magnitude(image):
    """
    Compute mean gradient magnitude using Sobel operator.

    Returns:
        dict: mean_gradient, max_gradient
    """
    # Sobel gradients
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)

    return {
        'mean_gradient': float(np.mean(gradient_magnitude)),
        'max_gradient': float(np.max(gradient_magnitude))
    }


def compute_sharpness_metrics(image):
    """
    Compute sharpness metrics.

    Returns:
        dict: laplacian_variance, gradient metrics
    """
    metrics = {
        'laplacian_variance': compute_laplacian_variance(image)
    }
    metrics.update(compute_gradient_magnitude(image))
    return metrics


def compute_michelson_contrast(image):
    """
    Compute Michelson contrast: (max - min) / (max + min)

    Returns:
        float: Michelson contrast (0-1)
    """
    img_min = np.min(image)
    img_max = np.max(image)

    if img_max + img_min == 0:
        return 0.0

    return float((img_max - img_min) / (img_max + img_min))


def compute_rms_contrast(image):
    """
    Compute RMS contrast: std of normalized intensities.

    Returns:
        float: RMS contrast
    """
    normalized = image.astype(np.float32) / 255.0
    return float(np.std(normalized))


def compute_local_contrast(image, window_size=15):
    """
    Compute local contrast using sliding window.

    Args:
        window_size: Size of local window (odd number)

    Returns:
        dict: mean_local_contrast, std_local_contrast
    """
    # Compute local mean and std
    kernel = np.ones((window_size, window_size)) / (window_size * window_size)
    local_mean = cv2.filter2D(image.astype(np.float32), -1, kernel)
    local_sq_mean = cv2.filter2D((image.astype(np.float32))**2, -1, kernel)
    local_std = np.sqrt(np.maximum(local_sq_mean - local_mean**2, 0))

    # Local contrast as local_std / local_mean (avoid division by zero)
    local_contrast = np.divide(local_std, local_mean + 1e-6)

    return {
        'mean_local_contrast': float(np.mean(local_contrast)),
        'std_local_contrast': float(np.std(local_contrast))
    }


def compute_contrast_metrics(image):
    """
    Compute all contrast metrics.

    Returns:
        dict: Michelson, RMS, and local contrast metrics
    """
    return {
        'michelson_contrast': compute_michelson_contrast(image),
        'rms_contrast': compute_rms_contrast(image),
        **compute_local_contrast(image)
    }


def estimate_noise_sigma(image):
    """
    Estimate noise sigma using Median Absolute Deviation (MAD) on high-frequency components.
    Uses robust estimation on Laplacian-filtered image.

    Returns:
        float: Estimated noise standard deviation
    """
    # Apply Laplacian to get high-frequency components
    laplacian = cv2.Laplacian(image, cv2.CV_64F)

    # Compute MAD
    median = np.median(laplacian)
    mad = np.median(np.abs(laplacian - median))

    # Convert MAD to sigma (for Gaussian distribution: sigma ≈ 1.4826 * MAD)
    sigma = 1.4826 * mad

    return float(sigma)


def compute_noise_metrics(image):
    """
    Compute noise estimation metrics.

    Returns:
        dict: estimated_noise_sigma
    """
    return {
        'estimated_noise_sigma': estimate_noise_sigma(image)
    }


def compute_entropy(image):
    """
    Compute Shannon entropy of the image.

    Returns:
        float: Entropy in bits
    """
    # Compute histogram
    hist, _ = np.histogram(image, bins=256, range=(0, 256))

    # Normalize to get probability distribution
    hist = hist.astype(np.float32)
    hist = hist / (hist.sum() + 1e-10)

    # Remove zeros
    hist = hist[hist > 0]

    # Compute entropy
    entropy = -np.sum(hist * np.log2(hist))

    return float(entropy)


def compute_edge_density(image, threshold=30):
    """
    Compute percentage of edge pixels using Canny edge detector.

    Args:
        threshold: Lower threshold for Canny detector

    Returns:
        float: Percentage of edge pixels (0-100)
    """
    edges = cv2.Canny(image, threshold, threshold * 2)
    edge_pixels = np.sum(edges > 0)
    total_pixels = edges.size

    return float(100.0 * edge_pixels / total_pixels)


def compute_information_metrics(image):
    """
    Compute information content metrics.

    Returns:
        dict: entropy, edge_density
    """
    return {
        'entropy': compute_entropy(image),
        'edge_density': compute_edge_density(image)
    }


def compute_effective_bit_depth(image):
    """
    Compute effective bit depth (actual bits used).

    Returns:
        float: Effective bit depth
    """
    unique_values = len(np.unique(image))

    if unique_values <= 1:
        return 0.0

    effective_bits = np.log2(unique_values)
    return float(effective_bits)


def compute_histogram_spread(image):
    """
    Compute percentage of available range utilized (0-255).

    Returns:
        float: Percentage of range used (0-100)
    """
    img_range = np.max(image) - np.min(image)
    return float(100.0 * img_range / 255.0)


def compute_saturation_percentage(image):
    """
    Compute percentage of clipped/saturated pixels (0 or 255).

    Returns:
        dict: saturation_low (at 0), saturation_high (at 255), saturation_total
    """
    total_pixels = image.size
    saturated_low = np.sum(image == 0)
    saturated_high = np.sum(image == 255)

    return {
        'saturation_low_pct': float(100.0 * saturated_low / total_pixels),
        'saturation_high_pct': float(100.0 * saturated_high / total_pixels),
        'saturation_total_pct': float(100.0 * (saturated_low + saturated_high) / total_pixels)
    }


def compute_dynamic_range_metrics(image):
    """
    Compute dynamic range utilization metrics.

    Returns:
        dict: effective_bit_depth, histogram_spread, saturation percentages
    """
    metrics = {
        'effective_bit_depth': compute_effective_bit_depth(image),
        'histogram_spread': compute_histogram_spread(image)
    }
    metrics.update(compute_saturation_percentage(image))
    return metrics


def compute_all_metrics(image):
    """
    Compute all baseline metrics for an image.

    Args:
        image: Grayscale image (uint8 numpy array)

    Returns:
        dict: All computed metrics organized by category
    """
    metrics = {
        'statistical': compute_statistical_metrics(image),
        'sharpness': compute_sharpness_metrics(image),
        'contrast': compute_contrast_metrics(image),
        'noise': compute_noise_metrics(image),
        'information': compute_information_metrics(image),
        'dynamic_range': compute_dynamic_range_metrics(image)
    }

    return metrics


# Metric registry for CLI access
METRIC_FUNCTIONS = {
    'statistical': compute_statistical_metrics,
    'sharpness': compute_sharpness_metrics,
    'contrast': compute_contrast_metrics,
    'noise': compute_noise_metrics,
    'information': compute_information_metrics,
    'dynamic_range': compute_dynamic_range_metrics,
    'all': compute_all_metrics
}
