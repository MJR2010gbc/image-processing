import numpy as np
import skimage
import matplotlib.pyplot as plt
from ImageProcessing import ImageProcessing 


np.abs(-2)

im = ImageProcessing('image1.jpeg')
colors = ['Red', 'Green', 'Blue']

print(im.magnitude_spectrum[0])
print(im.magnitude_spectrum[0].shape)
im.alex_edge_detection()
plt.imshow(im.filtered_image)
plt.title(f'Image ')
plt.show()


# plt.subplot(121)
# plt.imshow(im.image)
# plt.title('Input Image')
# plt.xticks([]), plt.yticks([])
# plt.subplot(122)
# plt.imshow(im.frequency_image, cmap = 'gray')
# plt.title('Magnitude Spectrum')
# plt.xticks([]), plt.yticks([])
# plt.show()