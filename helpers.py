import random
import string
import numpy as np


def getRandId(N):
    # using random.choices()
    # generating random strings 
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
    return res

def fftAsGray(fft2_array):
    # Shift to get the DC component in the center rather than in the upper left corner
    shifted_fft = np.fft.fftshift(fft2_array)
    # Get the absulute values as the transformed values by fft are imaginary values
    abs_fft = np.abs(shifted_fft)
    # Get log scaling in order to aviod the DC component will be domenant and all the image will be white
    # Adding 1 to avoid getting log 0 which is not defined
    log_fft = np.log(abs_fft + 1)
    return (log_fft / np.max(log_fft))

def notchFilter(fft_with_noise, thre=0.7):
    img_sh = fft_with_noise.shape
    gray_fft = fftAsGray(fft_with_noise)
    center = (int(img_sh[0]/2), int(img_sh[1]/2))
    rows = set([x[0] for x in np.argwhere((gray_fft > thre) == 1) if x[0] not in range(center[0]-5, center[0]+5)])
    cols = set([x[1] for x in np.argwhere((gray_fft > thre) == 1) if x[1] not in range(center[1]-5, center[1]+5)])
    fft_array_notch_shifted = np.fft.fftshift(fft_with_noise)
    for row in rows:
        fft_array_notch_shifted[row, :] = 0
    for col in cols:
        fft_array_notch_shifted[:, col] = 0
    fft_filtered = np.fft.ifftshift(fft_array_notch_shifted)
    return fft_filtered

def bandRejectFilter(fft_with_noise, circle_width=6, thre=0.75):
    img_sh = fft_with_noise.shape
    half_width = int(circle_width/2)
    gray_fft = fftAsGray(fft_with_noise)
    center = (int(img_sh[0]/2), int(img_sh[1]/2))
    points = [(x[0], x[1]) for x in np.argwhere((gray_fft > thre) == 1) if x[0] not in range(center[0]-5, center[0]+5)]
    x, y = np.meshgrid(range(-center[0], center[0]+1), range(-center[1], center[1]))
    z = np.sqrt(x**2 + y**2).T
    radius_list = [np.linalg.norm((center[0]-point[0], center[1]-point[1])) for point in points]
    radius = np.mean(radius_list)
    c = np.where((z > radius-half_width) & (z < radius+(circle_width-half_width)), True, False)
    c = np.invert(c)
    fft_array_band_reject_shifted = np.fft.fftshift(fft_with_noise)
    fft_filtered = np.fft.ifftshift(fft_array_band_reject_shifted * c)
    return fft_filtered

def ifft(fft_array):
    img = np.fft.ifft2(fft_array)
    abs_img = np.abs(img)
    return abs_img

