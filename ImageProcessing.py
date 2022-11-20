import cv2
import numpy as np
from matplotlib import pyplot as plt


class ImageProcessing:
    
    # Contains the image path, must be passed as argument in the creation of an instance
    image_path : str
    
    # The actual image loaded in memory and stored as numpy array of shape (height, width, colors(BGR))
    image : np.ndarray
    
    # The actual image loaded in memory and stored as numpy array in grayscale of shape (height, width)
    image_gray : np.ndarray
    
    # image dimensions
    row_number : int
    column_number : int 
    
    # center row and col of the image (rounded)
    crow : int 
    ccol : int
    
    # List of matrices (numpy arrays) containing the frequency domain with both natural and immaginary components 
    # of each color (sorted as RGB), already shifted to center the 0 frequencies, shape of each element of the list is (height, width, 2)
    image_frequency_RGB : list
    image_frequency_gray : np.ndarray
    
    # Spectra of the magnitude, logaritmic scale applied 
    magnitude_spectrum_RGB : list           # List divided by color and sorted as RGB
    magnitude_spectrum_gray : np.ndarray
    
    # List of matrices (numpy arrays) containing the frequency domain with both natural and immaginary components 
    # of each color (sorted as RGB), already shifted to center the 0 frequencies, shape of each element of the list is (height, width, 2)
    # POST FILTERING
    filtered_image_frequency_RGB : list
    filtered_image_frequency_gray : np.ndarray

    # List of spectra of the magnitude, divided by color and sorted as RGB, logaritmic scale applied 
    # POST FILTERING
    filtered_magnitude_spectrum_RGB : list
    filtered_magnitude_spectrum_gray : np.ndarray
    
    # The actual image filtered as numpy array of shape (height, width, colors(RGB))
    filtered_image_RGB : np.ndarray
    filtered_image_gray : np.ndarray

# 
#   Initialiazation method -> Defines the class and it's properties and instantiates all the necessary variables for easier access and 
#   faster computation, avoiding redundancies
# 
    def __init__(self, image_path):
        
        self.image_path = image_path
        
        # Reading the image 
        # The image is a matrix in the shape (height, width, colors(BGR)) normally the colors are used as RGB
        image_pre = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        # Converting the image colors from BGR to RGB
        self.image = cv2.cvtColor(image_pre, cv2.COLOR_BGR2RGB)
        self.filtered_image_RGB = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        # Reading the grayscale version
        self.image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.filtered_image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        self.row_number, self.column_number = self.image.shape[0:2]
        self.crow, self.ccol = int(self.row_number / 2), int(self.column_number / 2)  # center
        
        # Declaring the list of frequency domain and magnitude spectrum, it will contain the frequency divided by colors
        # self.image_frequency_RGB[0] will contain the Red component
        # self.image_frequency_RGB[1] will contain the Green component
        # self.image_frequency_RGB[2] will contain the Blue component
        # self.image_frequency_grascale will contain the grayscale
        self.image_frequency_RGB = []
        self.magnitude_spectrum_RGB = []
        self.filtered_image_frequency_RGB = []
        self.filtered_magnitude_spectrum_RGB = []
         
        # iterating over each color to get it's frequency domain
        for i in range(self.image.shape[2]):
            # get the dft of the i-th color with complex output included, this result in a 3D matrix shaped as (height, width, 2)
            # the matrix [:,:,0] contains the real values whereas [:,:,1] represent the imaginary part
            pre_shift_image_frequency_RGB = cv2.dft(np.float32(self.image[:,:,i]), flags=cv2.DFT_COMPLEX_OUTPUT)
            
            # shift to put 0 frequencies in the center
            #   
            #   1  |  2             4  |  3
            #  ---------    -->    ---------
            #   3  |  4             2  |  1
            # 
            # storing the shifted frequency domain in a class variable
            self.image_frequency_RGB.append(np.fft.fftshift(pre_shift_image_frequency_RGB))
            # get the magnitude of the vector defined by real and imaginary part, magnitude is a 2D matrix of shape (height, width)
            magnitude = cv2.magnitude(self.image_frequency_RGB[i][:, :, 0], self.image_frequency_RGB[i][:, :, 1])
            # apply log to have a discernible spectrum
            self.magnitude_spectrum_RGB.append(np.log(magnitude))

        # get grayscale frequency and generate magnitude spectrum
        pre_shift_image_frequency_gray = cv2.dft(np.float32(self.image_gray), flags=cv2.DFT_COMPLEX_OUTPUT)
       
        # shift to put 0 frequencies in the center
        #   
        #   1  |  2             4  |  3
        #  ---------    -->    ---------
        #   3  |  4             2  |  1
        # 
        # storing the shifted frequency domain in a class variable
        self.image_frequency_gray = np.fft.fftshift(pre_shift_image_frequency_gray)
        # get the magnitude of the vector defined by real and imaginary part, magnitude is a 2D matrix of shape (height, width)
        magnitude = cv2.magnitude(self.image_frequency_gray[:, :, 0], self.image_frequency_gray[:, :, 1])
        # apply log to have a discernible spectrum
        self.magnitude_spectrum_gray = np.log(magnitude)
#    
#   Utility methods
#    
    # Generates the (circular) mask to apply, accepts 3 arguments:
    #  - radius -> radius of the mask shape, 
    #  - intensity -> indicates the scaling factor to apply to the parts selected by the mask
    #  - direction -> 0: all the elements inside the circular area are 0s(hpf), Note: the values are not actual 0s but a close approximation to avoid DivideByZero error
    #             1: all elements inside the circular area are 1s(lpf) 
    def define_circular_mask(self, radius: float, intensity: float, direction: int):
        # Circular HPF mask, center circle is 0, remaining all ones
        mask = np.ones((self.row_number, self.column_number, 2), np.float64)
        center = [self.crow, self.ccol]
        x, y = np.ogrid[:self.row_number, :self.column_number]
        #  Mask area is a matrix of boolean, defining to which frequencies the filter will be applied to
        if direction:
            #               This is the formula of a circle         this one means everything OUTSIDE the circle
            mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 > radius*radius
        else:
            #               This is the formula of a circle         this one means everything INSIDE the circle
            mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius*radius
        
        mask[mask_area] = intensity
        return mask

    # Gets back the resulting image from the frequency domain to the spatial domain
    # accepts 1 argument:
    #  - matrix -> the frequency domain version of a single channel of the image (2D np.array) 
    def recompose_image(self, matrix):
        unshifted_frequency = np.fft.ifftshift(matrix)
        image_back = cv2.idft(unshifted_frequency, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)

        return image_back
    
    # Take the filtered frequency domain and generates magnitude spectrum and resulting image of the filtering
    # takes 1 argument:
    #  - color_channels -> list of int where:
    #                            0 coresponds to the Red channel
    #                            1 coresponds to the Green channel
    #                            2 coresponds to the Blue channel
    #                            [] empty list indicates a grayscale image  
    def get_image_back(self, color_channels):
        if(len(color_channels)):
        # apply mask and inverse DFT on each of the selected colors
            for channel in color_channels: 
                magnitude = cv2.magnitude(self.filtered_image_frequency_RGB[channel][:, :, 0], self.filtered_image_frequency_RGB[channel][:, :, 1])
                self.filtered_magnitude_spectrum_RGB.append(200 * np.log(magnitude))
                self.filtered_image_RGB[:, :, channel] = self.recompose_image(self.filtered_image_frequency_RGB[channel])
                
        else:
            magnitude = cv2.magnitude(self.filtered_image_frequency_gray[:, :, 0], self.filtered_image_frequency_gray[:, :, 1])
            self.filtered_magnitude_spectrum_gray = 20 * np.log(magnitude)
            self.filtered_image_gray = self.recompose_image(self.filtered_image_frequency_gray)


    # Sharpening with High Pass Filter
    def sharpening(self, color_channels):
        # Circular HPF mask, center circle is 0, remaining all ones
        mask = self.define_circular_mask(self.column_number/20, .5, 0)
        if len(color_channels):
            for channel in color_channels: 
                self.filtered_image_frequency_RGB.append(self.image_frequency_RGB[channel] * mask)
        else:
            self.filtered_image_frequency_gray = self.image_frequency_gray * mask
        
        self.get_image_back(color_channels)


    # Blurring with Low Pass Filter
    def blurring(self, color_channels):
        # Circular HPF mask, center circle is 0, remaining all ones
        mask = self.define_circular_mask(self.ccol/15, .3, 1)
        if len(color_channels):
            for channel in color_channels: 
                self.filtered_image_frequency_RGB.append(self.image_frequency_RGB[channel] * mask)
        else:
            self.filtered_image_frequency_gray = self.image_frequency_gray * mask

        self.get_image_back(color_channels)

    # Edge Detection with High Pass Filter
    def edge_detection(self, color_channels):
        # Circular HPF mask, center circle is 0, remaining all ones
        mask = self.define_circular_mask(self.ccol/20, 0.0001, 0)
        if len(color_channels):
            for channel in color_channels: 
                self.filtered_image_frequency_RGB.append(self.image_frequency_RGB[channel] * mask)
        else:
            self.filtered_image_frequency_gray = self.image_frequency_gray * mask
        
        self.get_image_back(color_channels)

    # noise filtering with Low Pass Filter
    def noise_filtering(self, color_channels):
        # Circular HPF mask, center circle is 0, remaining all ones
        mask = self.define_circular_mask(self.ccol/2, 0.00001, 1)
        if len(color_channels):
            for channel in color_channels: 
                self.filtered_image_frequency_RGB.append(self.image_frequency_RGB[channel] * mask)
        else:
            self.filtered_image_frequency_gray = self.image_frequency_gray * mask
        
        self.get_image_back(color_channels)
        
        

    
    
    # # Noise Filtering using Low Pass Filter
    # def alex_noise_filtering(self):
    #     # Circular HPF mask, center circle is 0, remaining all ones
    #     mask = np.ones((self.row_number, self.cols, 2), np.float64)
    #     r = 480
    #     center = [self.crow, self.ccol]
    #     x, y = np.ogrid[:self.row_number, :self.cols]
    #     mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 > r*r
    #     mask[mask_area] = 0.0000000000000000000001
       
    #     # apply mask and inverse DFT
    #     for i, color_frequency in enumerate(self.image_frequency_RGB): 
    #         self.filtered_image_frequency_RGB.append(color_frequency * mask)
    #         magnitude = cv2.magnitude(self.filtered_image_frequency_RGB[i][:, :, 0], self.filtered_image_frequency_RGB[i][:, :, 1])
    #         self.filtered_magnitude_spectrum_RGB.append(np.log(magnitude))
            
    #     self.recompose_image()


        
    # # Edge Detection with High Pass Filter
    # def edge_detection(self):
    #     dft = cv2.dft(np.float32(self.image_gray), flags=cv2.DFT_COMPLEX_OUTPUT)
    #     dft_shift = np.fft.fftshift(dft)

    #     magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
        
    #     rows, cols = self.image_gray.shape
    #     crow, ccol = int(rows / 2), int(cols / 2)  # center

    #     # Circular HPF mask, center circle is 0, remaining all ones

    #     mask = np.ones((rows, cols, 2), np.uint8)
    #     r = 80
    #     center = [crow, ccol]
    #     x, y = np.ogrid[:rows, :cols]
    #     mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
    #     mask[mask_area] = 0
    #     print(dft_shift)
    #     # apply mask and inverse DFT
    #     fshift = dft_shift * mask

    #     fshift_mask_mag = 2000 * np.log(cv2.magnitude(fshift[:, :, 0], fshift[:, :, 1]))

    #     f_ishift = np.fft.ifftshift(fshift)
    #     img_back = cv2.idft(f_ishift)
    #     img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    #     plt.figure(figsize=(20, 20))
    #     plt.subplot(2, 2, 1), plt.imshow(self.image, cmap='gray')
    #     plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    #     plt.subplot(2, 2, 2), plt.imshow(magnitude_spectrum, cmap='gray')
    #     plt.title('After FFT'), plt.xticks([]), plt.yticks([])
    #     plt.subplot(2, 2, 3), plt.imshow(fshift_mask_mag, cmap='gray')
    #     plt.title('FFT + Mask'), plt.xticks([]), plt.yticks([])
    #     plt.subplot(2, 2, 4), plt.imshow(img_back, cmap='gray')
    #     plt.title('After FFT Inverse'), plt.xticks([]), plt.yticks([])
    #     plt.show()
    
    # # Noise Filtering using Low Pass Filter
    # def noise_filtering(self):
    #     img = cv2.imread(self.image_path, 0)
    #     dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    #     dft_shift = np.fft.fftshift(dft)

    #     magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
        
    #     rows, cols = img.shape
    #     crow, ccol = int(rows / 2), int(cols / 2)  # center

    #     # Circular LPF mask, center circle is 1, remaining all zeros
    #     rows, cols = img.shape
    #     crow, ccol = int(rows / 2), int(cols / 2)

    #     mask = np.zeros((rows, cols, 2), np.uint8)
    #     r = 70
    #     center = [crow, ccol]
    #     x, y = np.ogrid[:rows, :cols]
    #     mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
    #     mask[mask_area] = 1

    #     # apply mask and inverse DFT
    #     fshift = dft_shift * mask

    #     step1 = cv2.magnitude(fshift[:, :, 0], fshift[:, :, 1])
    #     fshift_mask_mag = 2000 * np.log(step1)

    #     f_ishift = np.fft.ifftshift(fshift)
    #     img_back = cv2.idft(f_ishift)
    #     img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    #     plt.figure(figsize=(20, 20))
    #     plt.subplot(2, 2, 1), plt.imshow(img, cmap='gray')
    #     plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    #     plt.subplot(2, 2, 2), plt.imshow(magnitude_spectrum, cmap='gray')
    #     plt.title('After FFT'), plt.xticks([]), plt.yticks([])
    #     plt.subplot(2, 2, 3), plt.imshow(fshift_mask_mag, cmap='gray')
    #     plt.title('FFT + Mask'), plt.xticks([]), plt.yticks([])
    #     plt.subplot(2, 2, 4), plt.imshow(img_back, cmap='gray')
    #     plt.title('After FFT Inverse'), plt.xticks([]), plt.yticks([])
    #     plt.show()