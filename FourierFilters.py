import numpy as np
import matplotlib.pyplot as plt

from skimage.io import imread, imshow
from skimage.color import rgb2hsv, rgb2gray, rgb2yuv
from skimage import color, exposure, transform
from skimage.exposure import equalize_hist

class FourierFilters:
    @staticmethod
    def sharpening(image_path, factor):
        image = imread(image_path)
        transformed_channels = []
        frequency_domain = []
        for i in range(3):
            rgb_fft = np.fft.fftshift(np.fft.fft2((image[:, :, i])))
            transformed_channels.append(abs(np.fft.ifft2(rgb_fft)))


        final_image = np.dstack([transformed_channels[0].astype(int), 
                             transformed_channels[1].astype(int), 
                             transformed_channels[2].astype(int)])
        
        plt.imshow(final_image)
        
        plt.show()

if __name__=="__main__":
    FourierFilters.sharpening("image1.jpeg",3)