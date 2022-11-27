import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from ImageProcessing import ImageProcessing 
import math
from os.path import exists

# #                                                           (pass the actual image, NOT the ImageProcessing instance)
# #                                                                             |                   (usually 'viridis' or 'gray')
# # Method to show images, accept the following parameters:                     V                           V
# # - images: list of list, a proper input format should be as follows [[1st_image_to_show: np.array, cmap_value: string, 1st_image_title_to_display: string], ... , [nth_image_to_show: np.array, cmap_value: string, nth_image_title_to_display: string]]
# # - col_n: integer, defines the numebr of column to be displayed                                                                                                        
# def show_images(images, col_n):
#     row_n = math.ceil(len(images)/col_n)
#     for i, curr_image in enumerate(images):
#         plt.subplot(row_n, col_n, i+1)
#         plt.imshow(curr_image[0], cmap=curr_image[1])
#         plt.title(curr_image[2])

#     plt.show()

# # Get info from user on which filter and color setting to apply
# # Filter choices:               Color choices:
# # 1 - blur (LPF)                1 - Color(RGB)
# # 2 - sharpening (HPF           2 - Greyscale
# # 3 - edge detection            3 - Red
# # 4 - noise filtering           4 - Green
# #                               5 - Blue
# def user_filter_choice():
#     print('What transformation do you want to apply? (1 to 4)')
#     print('1 - blur (LPF)')
#     print('2 - sharpening (HPF)')
#     print('3 - edge detection')
#     print('4 - noise filtering')
#     # Check that the user input is valid
#     while True:
#         try:
#             filter_number = int(input())
#             if(not (filter_number in ([1, 2, 3, 4]))):
#                 raise Exception("You inserted a wrong number, try again!")
#             break
#         except ValueError as ve:
#             print(ve)
#             continue
#         except Exception as e:
#             print(e)
#             continue

#     print('What version of the image you want to work with?')
#     print('1 - Color(RGB)')
#     print('2 - Greyscale')
#     print('3 - Red')
#     print('4 - Green')
#     print('5 - Blue')
#     # Check that the user input is valid
#     while True:
#         try:
#             color_number = int(input())
#             if(not (color_number in [1, 2, 3, 4, 5])):
#                 raise Exception("You inserted a wrong number, try again!")
#             break
#         except ValueError as ve:
#             print(ve)
#             continue
#         except Exception as e:
#             print(e)
#             continue
    
#     # generates a list of channels to be used for the transformations, empty list translate to grayscale
#     if color_number == 1:
#         color_channels = [0, 1, 2]
#     elif color_number == 2:
#         color_channels = []
#     elif color_number == 3:
#         color_channels = [0]
#     elif color_number == 4:
#         color_channels = [1]
#     elif color_number == 5:
#         color_channels = [2]
#     else:
#         color_channels = []

    
#     return filter_number, color_channels
 

# # Calls methods from ImageProcessing class coresponding to user choices
# def apply_filter(image, filter, color):
#     if(filter == 1):
#         image.blurring(color)
#     elif(filter == 2):
#         image.sharpening(color)
#     elif(filter == 3):
#         image.edge_detection(color)
#     elif(filter == 4):
#         image.noise_filtering(color)

#     if color:
#         show_images([[image.image, 'viridis', 'Original RGB image'],[image.magnitude_spectrum_RGB[0], 'gray', 'Magnitude spectrum Red'],
#                     [image.filtered_image_RGB, 'viridis', 'Filtered image'],[image.filtered_magnitude_spectrum_RGB[0], 'gray', 'Filtered magnitude spectrum Red']],2)
#     else:
#         show_images([[image.image_gray, 'gray', 'Original image grayscale'],[image.magnitude_spectrum_gray, 'gray', 'Magnitude spectrum grayscale'],
#                     [image.filtered_image_gray, 'gray', 'Filtered image grayscale'],[image.filtered_magnitude_spectrum_gray, 'gray', 'Filtered magnitude spectrum grayscale']], 2)

# def main():
#     while True:
#         print('Enter the image name,')
#         print('(if the image is not in the current folder indicate the relative path)')  
#         # Get image address and check file existence (keep iterating until a workable path is defined)
#         # Note: Only checks for file existance not the fact that the file is an actual image!!
#         while True:
#             try:
#                 path = input()
#                 file_exists = exists(path)
#                 if(not file_exists):
#                     raise Exception('The specified path does not exist, try again!')
#                 else:
#                     break
#             except Exception as e:
#                 print(e)
#         # Instantiate a variable of class ImageProcessing
#         image = ImageProcessing(path)
#         # generating list of images to output (show the user what image he/she selected)
#         images_list = [[image.image, 'viridis', 'Original image'],[image.magnitude_spectrum_RGB[0], 'gray', 'Magnitude spectrum Red'],[image.magnitude_spectrum_RGB[1], 'gray', 'Magnitude spectrum Green'],[image.magnitude_spectrum_RGB[2], 'gray', 'Magnitude spectrum Blue'],
#                         [image.image_gray, 'gray', 'Greyscale image'],[image.magnitude_spectrum_gray, 'gray', 'Magnitude spectrum Greyscale']]  
#         # Call show_image method defined above to ahowcase images
#         show_images(images_list, 4)
#         # Calling the user_filter_choice defined above to get information from the user on which filter to apply and color settings
#         filter_number, color_channels = user_filter_choice()
#         # Apply the selected filter
#         apply_filter(image, filter_number, color_channels)
#         # Requires user if a new run is needed or the program should terminate
#         while True:
#             try:
#                 print('Would you like to continue?(y/n)')
#                 keep_going = input()
#                 if keep_going.lower() == 'n':
#                     break
#                 elif keep_going.lower() == 'y':
#                     break
#                 else:
#                     raise Exception('Wrong input, try again!')
#             except Exception as e:
#                 print(e)
#         if keep_going.lower() == 'n':
#             break


def browseFiles():
    global filename
    filename = askopenfilename(title = "Select a File", filetypes = [("Images", "*.jpeg"), ("all files", "*.*")])
    if filename != '':
        label_file_explorer.config(text = f"Selected file: {filename}")
        label_file_explorer.update()


def main2():
    # Create the root window and set it's parameters
    global root
    root = Tk()
    root.title('Image processing')
    root.geometry("1000x800") 
    root.config(background = "white", padx=25, pady=25)
    
    global frame
    frame = Frame(root, bg='gray95', width=950, height=700)
    frame.grid(column=1, row=1, columnspan=7)

    # Create a File Explorer label and set it's parameters
    global label_file_explorer 
    label_file_explorer= Label(root, text = f"No file selected", height = 4, fg = "black", bg='white')
    label_file_explorer.grid(column = 2, row = 2, columnspan=5)
    
    # Create button for closing the program and to start the File Explorer
    button_explore = Button(root, text = "Open", command = lambda:browseFiles())  
    button_explore.grid(column = 1, row = 2)
    
    button_exit = Button(root, text = "Exit", command = exit)
    button_exit.grid(column = 7,row = 2)
    
    # Let the window wait for any events
    root.mainloop()

# check if the process running is the 'main', in that case start 
if __name__ == '__main__':
    main2()