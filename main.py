import numpy as np
import skimage
import matplotlib.pyplot as plt
from ImageProcessing import ImageProcessing 
import cv2
import math
import matplotlib
from os.path import exists


def show_images(images, col_n):
    row_n = math.ceil(len(images)/col_n)
    for i, curr_image in enumerate(images):
        plt.subplot(row_n, col_n, i+1)
        plt.imshow(curr_image[0], cmap=curr_image[1])
        plt.title(curr_image[2])

    plt.show()

def user_filter_choice():
    print('What transformation do you want to apply? (1 to 4)')
    print('1 - blur (LPF)')
    print('2 - sharpening (HPF)')
    print('3 - edge detection')
    print('4 - noise filtering')
    filter_number = 0
    while(not (filter_number in ([1, 2, 3, 4]))):
        try:
            filter_number = int(input())
            if(not (filter_number in ([1, 2, 3, 4]))):
                raise Exception("You inserted a wrong number, try again!")
        except ValueError:
            print('Please enter an integer.')
        except:
            print('You inserted a wrong number, try again!')

    print('What version of the image you want to work with?')
    print('1 - Color(RGB)')
    print('2 - Greyscale')
    print('3 - Red')
    print('4 - Green')
    print('5 - Blue')
    color_number = 0
    while(not (color_number in ([1, 2, 3, 4, 5]))):
        try:
            color_number = int(input())
            if(not (color_number in ([1, 2, 3, 4, 5]))):
                raise Exception("You inserted a wrong number, try again!")
        except ValueError:
            print('Please enter an integer.')
        except:
            print('You inserted a wrong number, try again!')
    
    return filter_number, color_number 

def apply_filter(image, filter, color):
    if(filter == 1):
        image.blurring(color)
    elif(filter == 2):
        image.sharpening(color)
    elif(filter == 3):
        image.edge_detection(color)
    elif(filter == 4):
        image.noise_filtering(color)

    if(color == 2):
        show_images([[image.image_gray, 'gray', 'Original image grayscale'],[image.magnitude_spectrum_gray, 'gray', 'Magnitude spectrum grayscale'],
                    [image.filtered_image_gray, 'gray', 'Filtered image grayscale'],[image.filtered_magnitude_spectrum_gray, 'gray', 'Filtered magnitude spectrum grayscale']], 2)
    else:
        show_images([[image.image, 'viridis', 'Original RGB image'],[image.magnitude_spectrum_RGB[0], 'gray', 'Magnitude spectrum Red'],
                    [image.filtered_image_RGB, 'viridis', 'Filtered image'],[image.filtered_magnitude_spectrum_RGB[0], 'gray', 'Filtered magnitude spectrum Red']], 2)

def main():
    print('Enter the image name,')
    print('(if the image is not in the current folder indicate the relative path)')  
    file_exists = False
    while(not file_exists):
        path = input()
        file_exists = exists(path)
        if(not file_exists):
            print('The specified path does not exist, try again!')

    image = ImageProcessing(path)
    images_list = [[image.image, 'viridis', 'Original image'],[image.magnitude_spectrum_RGB[0], 'gray', 'Magnitude spectrum Red'],[image.magnitude_spectrum_RGB[1], 'gray', 'Magnitude spectrum Green'],[image.magnitude_spectrum_RGB[2], 'gray', 'Magnitude spectrum Blue'],
                    [image.image_gray, 'gray', 'Greyscale image'],[image.magnitude_spectrum_gray, 'gray', 'Magnitude spectrum Greyscale']]  
    show_images(images_list, 4)

    filter_number, color_number = user_filter_choice()
    apply_filter(image, filter_number, color_number)





if __name__ == '__main__':
    main()

# def show_images(images: list, col_n):
#     plt.figure(figsize=(20,20))
#     row_n = math.ceil(len(images)/col_n)
#     for i, image in enumerate(images):
#         plt.subplot(row_n, col_n, i+1)
#         plt.imshow(image[0])
#         plt.axis('off')
#         plt.title(image[1])
#     plt.show()

# # def main():
# print('Enter the image name,')
# print('(if the image is not in the current folder indicate the relative path)')
# path = input()
# image = ImageProcessing(path)
# show_images = [[image.image, 'Original image'],[image.magnitude_spectrum[0], 'Magnitude spectrum Red'],[image.magnitude_spectrum[1], 'Magnitude spectrum Green'],[image.magnitude_spectrum[2], 'Magnitude spectrum Blue'],
#                 [image.image_bw, 'Greyscale image'],[image.magnitude_spectrum_grayscale, 'Magnitude spectrum Greyscale']]  

# plt.figure(figsize=(20,20))
# row_n = math.ceil(len(show_images)/4)
# for i, image in enumerate(show_images):
#     plt.subplot(row_n, 4, i+1)
#     plt.imshow(image[0])
#     plt.axis('off')
#     plt.title(image[1])
# plt.show()



# if __name__ == '__main__':
#     main()
# im = ImageProcessing('image1.jpeg')
# # colors = ['Red', 'Green', 'Blue']

# # print(im.magnitude_spectrum[0])
# # print(im.magnitude_spectrum[0].shape)
# # im.alex_edge_detection()
# print(im.image_bw)
# print(im.image[:,:,0])
# print(im.image[:,:,1])
# print(im.image[:,:,2])
# im.alex_edge_detection()
#



# plt.subplot(121)
# plt.imshow(im.image)
# plt.title('Input Image')
# plt.xticks([]), plt.yticks([])
# plt.subplot(122)
# plt.imshow(im.frequency_image, cmap = 'gray')
# plt.title('Magnitude Spectrum')
# plt.xticks([]), plt.yticks([])
# plt.show()