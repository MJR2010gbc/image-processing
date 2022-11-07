import numpy as np
import cv2
from matplotlib import pyplot as plt

class ImageProcessing:
    # Contains the image path, must be passed as argument in the creation of an instance
    image_path : str
    # The actual image loaded in memory and stored as numpy array of shape (height, width, colors(BGR))
    image : np.ndarray
    # List of matrices (numpy arrays) containing the frequency domain with both natural and immaginary components 
    # of each color (sorted as RGB), already shifted to center the 0 frequencies, shape of each element of the list is (height, width, 2)
    image_frequency_on_color : list[np.ndarray]
    # List of spectra of the magnitude, divided by color and sorted as RGB, logaritmic scale applied 
    magnitude_spectrum : list[np.ndarray]

    def __init__(self, image_path):
        self.image_path = image_path
        # Reading the image 
        # The image is a matrix in the shape (height, width, colors(BGR)) normally the colors are used as RGB
        image_pre = cv2.imread(image_path, cv2.IMREAD_COLOR)
        # Converting the image colors from BGR to RGB
        self.image = cv2.cvtColor(image_pre, cv2.COLOR_BGR2RGB)
         
        # Declaring the list of frequency domain and magnitude spectrum, it will contain the frequency divided by colors
        # self.image_frequency_on_color[0] will contain the Red component
        # self.image_frequency_on_color[1] will contain the Green component
        # self.image_frequency_on_color[2] will contain the Blue component
        self.image_frequency_on_color = []
        self.magnitude_spectrum = []
        # iterating over each color to get it's frequency domain
        for i in range(self.image.shape[2]):
            # get the dft of the i-th color with complex output included, this result in a 3D matrix shaped as (height, width, 2)
            # the matrix [:,:,0] contains the real values whereas [:,:,1] represent the imaginary part
            pre_shift_image_frequency_on_color = cv2.dft(np.float32(self.image[:,:,i]), flags=cv2.DFT_COMPLEX_OUTPUT)
            # shift to put 0 frequencies in the center
            #   
            #   1  |  2             4  |  3
            #  ---------    -->    ---------
            #   3  |  4             2  |  1
            # 
            # storing the shifted frequency domain in a class variable
            self.image_frequency_on_color.append(np.fft.fftshift(pre_shift_image_frequency_on_color))
            # get the magnitude of the vector defined by real and imaginary part, magnitude is a 2D matrix of shape (height, width)
            magnitude = cv2.magnitude(self.image_frequency_on_color[i][:, :, 0], self.image_frequency_on_color[i][:, :, 1])
            # apply log to have a discernible spectrum
            self.magnitude_spectrum.append(np.log(magnitude))

    
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