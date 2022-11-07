import numpy as np
import cv2
from matplotlib import pyplot as plt

class ImageProcessing:
    def __init__(self, image):
        self.image = image
    
    # Edge Detection with High Pass Filter
    def edge_detection(self):
        img = cv2.imread(self.image, 0)
        dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)

        magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
        
        rows, cols = img.shape
        crow, ccol = int(rows / 2), int(cols / 2)  # center

        # Circular HPF mask, center circle is 0, remaining all ones

        mask = np.ones((rows, cols, 2), np.uint8)
        r = 80
        center = [crow, ccol]
        x, y = np.ogrid[:rows, :cols]
        mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
        mask[mask_area] = 0

        # apply mask and inverse DFT
        fshift = dft_shift * mask

        fshift_mask_mag = 2000 * np.log(cv2.magnitude(fshift[:, :, 0], fshift[:, :, 1]))

        f_ishift = np.fft.ifftshift(fshift)
        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

        plt.figure(figsize=(20, 20))
        plt.subplot(2, 2, 1), plt.imshow(img, cmap='gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 2), plt.imshow(magnitude_spectrum, cmap='gray')
        plt.title('After FFT'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 3), plt.imshow(fshift_mask_mag, cmap='gray')
        plt.title('FFT + Mask'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 4), plt.imshow(img_back, cmap='gray')
        plt.title('After FFT Inverse'), plt.xticks([]), plt.yticks([])
        plt.show()
    
    # Noise Filtering using Low Pass Filter
    def noise_filtering(self):
        img = cv2.imread(self.image, 0)
        dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)

        magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
        
        rows, cols = img.shape
        crow, ccol = int(rows / 2), int(cols / 2)  # center

        # Circular LPF mask, center circle is 1, remaining all zeros
        rows, cols = img.shape
        crow, ccol = int(rows / 2), int(cols / 2)

        mask = np.zeros((rows, cols, 2), np.uint8)
        r = 70
        center = [crow, ccol]
        x, y = np.ogrid[:rows, :cols]
        mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
        mask[mask_area] = 1

        # apply mask and inverse DFT
        fshift = dft_shift * mask

        step1 = cv2.magnitude(fshift[:, :, 0], fshift[:, :, 1])
        fshift_mask_mag = 2000 * np.log(step1)

        f_ishift = np.fft.ifftshift(fshift)
        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

        plt.figure(figsize=(20, 20))
        plt.subplot(2, 2, 1), plt.imshow(img, cmap='gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 2), plt.imshow(magnitude_spectrum, cmap='gray')
        plt.title('After FFT'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 3), plt.imshow(fshift_mask_mag, cmap='gray')
        plt.title('FFT + Mask'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 4), plt.imshow(img_back, cmap='gray')
        plt.title('After FFT Inverse'), plt.xticks([]), plt.yticks([])
        plt.show()