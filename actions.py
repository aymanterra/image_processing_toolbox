from scipy.ndimage.filters import median_filter
from skimage import io, color, exposure, filters
import numpy as np
import matplotlib.pyplot as plt
from logger import logger
from scipy.fftpack import fft2 ,fftshift
from scipy.ndimage import convolve
import json
from helpers import notchFilter, bandRejectFilter, ifft, fftAsGray


def image_histogram(random_id):
    try:
        original_img_path = f'./static/images/original-{random_id}.jpeg'
        img = io.imread(original_img_path, as_gray=True)
        io.imsave(f'./static/images/original_gray-{random_id}.jpeg', img)
        plt.close()
        plt.hist(img.ravel(), 256)
        plt.savefig(f'./static/images/original_histogram-{random_id}.jpeg')
        plt.close()
        return True
    except Exception as e:
        logger.exception(e)
        return False

def histogram_equalization(random_id):
    try:
        original_img_path = f'./static/images/original-{random_id}.jpeg'
        img = io.imread(original_img_path, as_gray=True)
        io.imsave(f'./static/images/original_gray-{random_id}.jpeg', img)
        plt.close()
        plt.hist(img.ravel(), 256)
        plt.savefig(f'./static/images/original_histogram-{random_id}.jpeg')
        plt.close()
        equalized_img = exposure.equalize_hist(img)
        io.imsave(f'./static/images/equalized_image-{random_id}.jpeg', equalized_img)
        plt.hist(equalized_img.ravel(), 256)
        plt.savefig(f'./static/images/equalized_histogram-{random_id}.jpeg')
        plt.close()
        return True
    except Exception as e:
        logger.exception(e)
        return False

def edge_detection(random_id, filtering_technique):
    try:
        original_img_path = f'./static/images/original-{random_id}.jpeg'
        img = io.imread(original_img_path, as_gray=True)
        io.imsave(f'./static/images/original_gray-{random_id}.jpeg', img)
        if filtering_technique == "Sobel":
            filtered_img = filters.sobel(img)
            io.imsave(f'./static/images/filtered-{random_id}.jpeg', filtered_img)
        elif filtering_technique == "Laplace":
            filtered_img = filters.laplace(img)
            io.imsave(f'./static/images/filtered-{random_id}.jpeg', filtered_img)
        return True
    except Exception as e:
        logger.exception(e)
        return False

def image_fourier_transformation(random_id):
    try:
        original_img_path = f'./static/images/original-{random_id}.jpeg'
        img = io.imread(original_img_path, as_gray=True)
        io.imsave(f'./static/images/original_gray-{random_id}.jpeg', img)
        fft2_img=fft2(img)
        fftshift_img=fftshift(fft2_img)
        abs_img=np.abs(fftshift_img)
        log_fft2_image = 20*np.log(abs_img)
        io.imsave(f'./static/images/fourier_transformation-{random_id}.jpeg', log_fft2_image)
        return True
    except Exception as e:
        logger.exception(e)
        return False

def adding_noise(random_id, noise_type, params={}):
    try:
        original_img_path = f'./static/images/original-{random_id}.jpeg'
        img = io.imread(original_img_path)
        if len(img.shape) == 3:
            gray_img = color.rgb2gray(img)
            io.imsave(f'./static/images/original_gray-{random_id}.jpeg', gray_img)
        elif len(img.shape) == 2:
            gray_img = np.copy(img)
        else:
            raise Exception("Invalid numer of channels.")
        io.imsave(f'./static/images/original_gray-{random_id}.jpeg', gray_img)
        noisy = np.copy(img)
        if noise_type == "Salt and Pepper":
            s_to_p_ratio = float(params["s_to_p_ratio"]) if ("s_to_p_ratio" in params and params["s_to_p_ratio"]) else 0.5
            amount = float(params["amount"]) if ("amount" in params and params["amount"]) else 0.04
            # Salt mode
            num_salt = np.ceil(amount * img.size * s_to_p_ratio)
            coords = [np.random.randint(0, i - 1, int(num_salt))
                    for i in img.shape]
            noisy[tuple(coords)] = 255
            # Pepper mode
            num_pepper = np.ceil(amount* img.size * (1. - s_to_p_ratio))
            coords = [np.random.randint(0, i - 1, int(num_pepper))
                    for i in img.shape]
            noisy[tuple(coords)] = 0
        elif noise_type == "Gaussian":
            mean = float(params["mean"]) if ("mean" in params and params["mean"]) else 0
            sigma = float(params["sigma"]) if ("sigma" in params and params["sigma"]) else 0.1
            noise = np.random.normal(mean , sigma, img.shape)
            noisy = img / 255 + noise
        elif noise_type == "Periodic":
            sh = gray_img.shape
            noise = np.zeros(sh, dtype='float64')
            X, Y = np.meshgrid(range(sh[0]), range(sh[1]))
            A = 0.3
            x_axis_frequency = float(params["x_axis_frequency"]) if ("x_axis_frequency" in params and params["x_axis_frequency"]) else 0.5
            y_axis_frequency = float(params["y_axis_frequency"]) if ("y_axis_frequency" in params and params["y_axis_frequency"]) else 0.5
            noise += A * np.sin(X * x_axis_frequency + Y * y_axis_frequency).T
            noisy = gray_img + noise
        io.imsave(f'./static/images/noisy-{random_id}.jpeg', noisy)
        return True
    except Exception as e:
        logger.exception(e)
        return False

def removing_noise(random_id, noise_type, params):
    try:
        original_img_path = f'./static/images/original-{random_id}.jpeg'
        img = io.imread(original_img_path)
        if len(img.shape) == 3:
            gray_img = color.rgb2gray(img)
            io.imsave(f'./static/images/original_gray-{random_id}.jpeg', gray_img)
        elif len(img.shape) == 2:
            gray_img = np.copy(img)
        else:
            raise Exception("Invalid numer of channels.")
        denoised_img = np.copy(img)
        if noise_type == "Salt and Pepper":
            if len(img.shape) == 3:
                for ch in range(img.shape[2]):
                    denoised_img[:, :, ch] = median_filter(img[:, :, ch], 3)
            elif len(img.shape) == 2:
                denoised_img = median_filter(img, 3)
        elif noise_type == "Gaussian":
            avarage_kernel = np.array([
                [ 1/15,  2/15,  1/15],
                [ 2/15,  3/15,  2/15],
                [ 1/15,  2/15,  1/15]
            ])
            if len(img.shape) == 3:
                for ch in range(img.shape[2]):
                    denoised_img[:, :, ch] = convolve(img[:, :, ch], avarage_kernel)
            elif len(img.shape) == 2:
                denoised_img = convolve(img, avarage_kernel)
            denoised_img = denoised_img + filters.sobel(img)
        elif noise_type == "Periodic":
            if "removal_type" in params and params["removal_type"] == "Notch":
                image_fourier_transformation(random_id)
                fft_with_noise = np.fft.fft2(gray_img)
                denoised_fft = notchFilter(fft_with_noise, 0.8)
                io.imsave(f'./static/images/denoised_fourier_transformation-{random_id}.jpeg', fftAsGray(denoised_fft))
                denoised_img = ifft(denoised_fft)
            elif "removal_type" in params and params["removal_type"] == "Band Reject":
                image_fourier_transformation(random_id)
                fft_with_noise = np.fft.fft2(gray_img)
                denoised_fft = bandRejectFilter(fft_with_noise, thre=0.8)
                io.imsave(f'./static/images/denoised_fourier_transformation-{random_id}.jpeg', fftAsGray(denoised_fft))
                denoised_img = ifft(denoised_fft)
            elif "removal_type" in params and params["removal_type"] == "Mask":
                image_fourier_transformation(random_id)
                fft_with_noise = np.fft.fft2(gray_img)
                selected_pixels = json.loads(params["selected_pixels"])
                H, W = fft_with_noise.shape
                denoised_shifted_fft = np.fft.fftshift(fft_with_noise)
                padding = 5
                for pixel in selected_pixels:
                    x_start = pixel["x"] - padding if pixel["x"] >= padding else pixel["x"]
                    x_end = pixel["x"] + padding if (pixel["x"] + padding) <= W else pixel["x"]
                    y_start = pixel["y"] - padding if pixel["y"] >= padding else pixel["y"]
                    y_end = pixel["y"] + padding if (pixel["y"] + padding) <= H else pixel["y"]
                    denoised_shifted_fft[y_start:y_end, x_start:x_end] = 0
                denoised_fft = np.fft.ifftshift(denoised_shifted_fft)
                io.imsave(f'./static/images/denoised_fourier_transformation-{random_id}.jpeg', fftAsGray(denoised_fft))
                denoised_img = ifft(denoised_fft)
        io.imsave(f'./static/images/denoised-{random_id}.jpeg', denoised_img)
        return True
    except Exception as e:
        logger.exception(e)
        return False
