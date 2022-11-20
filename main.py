import numpy as np
import matplotlib.pyplot as plt
from ImageProcessing import ImageProcessing 
import math
from os.path import exists
#                                                           (pass the actual image, NOT the ImageProcessing instance)
#                                                                             |                   (usually 'viridis' or 'gray')
# Method to show images, accept the following parameters:                     V                           V
# - images: list of list, a proper input format should be as follows [[1st_image_to_show: np.array, cmap_value: string, 1st_image_title_to_display: string], ... , [nth_image_to_show: np.array, cmap_value: string, nth_image_title_to_display: string]]
# - col_n: integer, defines the numebr of column to be displayed                                                                                                        
def show_images(images, col_n):
    row_n = math.ceil(len(images)/col_n)
    for i, curr_image in enumerate(images):
        plt.subplot(row_n, col_n, i+1)
        plt.imshow(curr_image[0], cmap=curr_image[1])
        plt.title(curr_image[2])

    plt.show()

# Get info from user on which filter and color setting to apply
# Filter choices:               Color choices:
# 1 - blur (LPF)                1 - Color(RGB)
# 2 - sharpening (HPF           2 - Greyscale
# 3 - edge detection            3 - Red
# 4 - noise filtering           4 - Green
#                               5 - Blue
def user_filter_choice():
    print('What transformation do you want to apply? (1 to 4)')
    print('1 - blur (LPF)')
    print('2 - sharpening (HPF)')
    print('3 - edge detection')
    print('4 - noise filtering')
    # Check that the user input is valid
    while True:
        try:
            filter_number = int(input())
            if(not (filter_number in ([1, 2, 3, 4]))):
                raise Exception("You inserted a wrong number, try again!")
            break
        except ValueError as ve:
            print(ve)
            continue
        except Exception as e:
            print(e)
            continue

    print('What version of the image you want to work with?')
    print('1 - Color(RGB)')
    print('2 - Greyscale')
    print('3 - Red')
    print('4 - Green')
    print('5 - Blue')
    # Check that the user input is valid
    while True:
        try:
            color_number = int(input())
            if(not (color_number in [1, 2, 3, 4, 5])):
                raise Exception("You inserted a wrong number, try again!")
            break
        except ValueError as ve:
            print(ve)
            continue
        except Exception as e:
            print(e)
            continue
    
    # generates a list of channels to be used for the transformations, empty list translate to grayscale
    if color_number == 1:
        color_channels = [0, 1, 2]
    elif color_number == 2:
        color_channels = []
    elif color_number == 3:
        color_channels = [0]
    elif color_number == 4:
        color_channels = [1]
    elif color_number == 5:
        color_channels = [2]
    else:
        color_channels = []

    
    return filter_number, color_channels
 

# Calls methods from ImageProcessing class coresponding to user choices
def apply_filter(image, filter, color):
    if(filter == 1):
        image.blurring(color)
    elif(filter == 2):
        image.sharpening(color)
    elif(filter == 3):
        image.edge_detection(color)
    elif(filter == 4):
        image.noise_filtering(color)

    if color:
        show_images([[image.image, 'viridis', 'Original RGB image'],[image.magnitude_spectrum_RGB[0], 'gray', 'Magnitude spectrum Red'],
                    [image.filtered_image_RGB, 'viridis', 'Filtered image'],[image.filtered_magnitude_spectrum_RGB[0], 'gray', 'Filtered magnitude spectrum Red']],2)
    else:
        show_images([[image.image_gray, 'gray', 'Original image grayscale'],[image.magnitude_spectrum_gray, 'gray', 'Magnitude spectrum grayscale'],
                    [image.filtered_image_gray, 'gray', 'Filtered image grayscale'],[image.filtered_magnitude_spectrum_gray, 'gray', 'Filtered magnitude spectrum grayscale']], 2)

def main():
    while True:
        print('Enter the image name,')
        print('(if the image is not in the current folder indicate the relative path)')  
        # Get image address and check file existence (keep iterating until a workable path is defined)
        # Note: Only checks for file existance not the fact that the file is an actual image!!
        while True:
            try:
                path = input()
                file_exists = exists(path)
                if(not file_exists):
                    raise Exception('The specified path does not exist, try again!')
                else:
                    break
            except Exception as e:
                print(e)
        # Instantiate a variable of class ImageProcessing
        image = ImageProcessing(path)
        # generating list of images to output (show the user what image he/she selected)
        images_list = [[image.image, 'viridis', 'Original image'],[image.magnitude_spectrum_RGB[0], 'gray', 'Magnitude spectrum Red'],[image.magnitude_spectrum_RGB[1], 'gray', 'Magnitude spectrum Green'],[image.magnitude_spectrum_RGB[2], 'gray', 'Magnitude spectrum Blue'],
                        [image.image_gray, 'gray', 'Greyscale image'],[image.magnitude_spectrum_gray, 'gray', 'Magnitude spectrum Greyscale']]  
        # Call show_image method defined above to ahowcase images
        show_images(images_list, 4)
        # Calling the user_filter_choice defined above to get information from the user on which filter to apply and color settings
        filter_number, color_channels = user_filter_choice()
        # Apply the selected filter
        apply_filter(image, filter_number, color_channels)
        # Requires user if a new run is needed or the program should terminate
        while True:
            try:
                print('Would you like to continue?(y/n)')
                keep_going = input()
                if keep_going.lower() == 'n':
                    break
                elif keep_going.lower() == 'y':
                    break
                else:
                    raise Exception('Wrong input, try again!')
            except Exception as e:
                print(e)
        if keep_going.lower() == 'n':
            break
        

# check if the process running is the 'main', in that case start 
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