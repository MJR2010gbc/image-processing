import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from ImageProcessing import ImageProcessing 
import math
from PIL import Image, ImageTk
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
drag_id = ''
placeholder = True
root_w = 0
root_h = 0
def stop_drag():
    global drag_id, first_time
    root.state('zoomed')

    # maximum desirable width and height (over this the images would not fit the frame)
    global max_h
    global max_w
    if placeholder:
        max_w = int(root.winfo_width()*.045)
        max_h = int(root.winfo_height()*.025)
        og_img_label.configure(width=max_w, height=max_h)
        og_img_spec_label.configure(width=max_w, height=max_h)
        mod_img_label.configure(width=max_w, height=max_h)
        mod_img_spec_label.configure(width=max_w, height=max_h)
    else:
        max_w = int(root.winfo_width()*.313)
        max_h = int(root.winfo_height()*.373)
        display_images(image)

    # reset drag_id to be able to detect the start of next dragging
    drag_id = ''

def dragging(event):
    global drag_id
    if event.widget is root:  # do nothing if the event is triggered by one of root's children
        if drag_id != '':
            # cancel scheduled call to stop_drag
            root.after_cancel(drag_id)
        # schedule stop_drag
        drag_id = root.after(100, stop_drag)

def resize_image_to_display(img):
    
    # gain current image dimension
    img_w, img_h = img.size
    # calculate current image aspect ratio
    aspect_ratio = img_w/img_h
    # evaluate which dimension to take for max dimension defined above so that the other does 
    # not exceed maximum size limit 
    if max_h*aspect_ratio <= max_w:
        # (max_h*aspect_ratio) = resized width mantaining the aspect ratio, 
        # if that does not exceed the width limit means our image optimal dimension is
        # (max_h*aspect_ratio), max_h) 
        new_size = (int(max_h*aspect_ratio), max_h)
    else:
        # if max_h*aspect_ratio > max_w means that using max_h for our image dimension will cause
        # the width to be too large, as consequence we should take max width and elaborate height 
        # as follows: max_w/aspect_ratio
        new_size = (max_w, int(max_w/aspect_ratio))
    
    res_img = img.resize(new_size)
    return res_img

def display_images(image):
    og_img = resize_image_to_display(Image.fromarray(image.image))
    tk_og_img = ImageTk.PhotoImage(image = og_img)
    sp_og_img = resize_image_to_display(Image.fromarray(image.magnitude_spectrum_RGB[0]))
    tk_sp_og_img = ImageTk.PhotoImage(image = sp_og_img)
    filtered_img = resize_image_to_display(Image.fromarray(image.filtered_image_RGB))
    tk_filtered_img = ImageTk.PhotoImage(image = filtered_img)
    sp_filtered_img = resize_image_to_display(Image.fromarray(image.filtered_magnitude_spectrum_RGB[0]))
    tk_sp_filtered_img = ImageTk.PhotoImage(image = sp_filtered_img)

    og_img_label.image = tk_og_img
    og_img_label.configure(image = tk_og_img, width=max_w, height=max_h)
    og_img_spec_label.image = tk_sp_og_img
    og_img_spec_label.configure(image = tk_sp_og_img, width=max_w, height=max_h)
    mod_img_label.image = tk_filtered_img
    mod_img_label.configure(image = tk_filtered_img, width=max_w, height=max_h)
    mod_img_spec_label.image = tk_sp_filtered_img
    mod_img_spec_label.configure(image = tk_sp_filtered_img, width=max_w, height=max_h)

def load_image(file_path):
    global image
    image = ImageProcessing(file_path)
    
    global max_h, max_w, placeholder
    placeholder = False
    max_w = int(root.winfo_width()*.313)
    max_h = int(root.winfo_height()*.373)

    display_images(image)
    
    if file_path != '':
        label_file_explorer.config(text = f"Selected file: {file_path}")
        label_file_explorer.update()


def browseFiles():
    global file_path
    file_path = askopenfilename(title = "Select a File", filetypes = [("Images", "*.jpeg"), ("all files", "*.*")])
    load_image(file_path)
    
def apply_filter():
    
    if selected.get() == 'RGB':
        channels = [0,1,2]
    else:
        channels = []
    direction = var_filter.get()
    radius = sli_radius.get()
    intensity = sli_intensity.get()
    image.custom_filter(channels, radius, intensity, direction)
    display_images(image)

def main2():
    # Create the root window and set it's parameters
    global root
    root = tk.Tk()
    root.title('Image processing')
    root.state('zoomed')
    root.resizable(width=False, height=False)
    root.bind('<Configure>', dragging)
    root.config(background = "white", padx=25, pady=25)

    global frame
    frame = tk.Frame(root, bg='gray95')
    frame.config(highlightcolor='black', highlightbackground='black', highlightthickness=1)
    frame.pack(expand=True, side='top', fill="both")

    global images_area
    images_area = tk.Frame(frame, bg='gray95')
    images_area.config(highlightcolor='black', highlightbackground='black', highlightthickness=1)
    images_area.pack(side='left', expand=True, fill="both", ipadx=15)
    images_area.columnconfigure(1, weight=2)
    images_area.columnconfigure(2, weight=1)
    images_area.columnconfigure(3, weight=2)
    images_area.rowconfigure(1, weight=2)
    images_area.rowconfigure(2, weight=1)
    images_area.rowconfigure(3, weight=2)

    global og_img_label
    og_img_label = tk.Label(images_area, bg='gray95', text='Original image will appear here', borderwidth=1, relief='solid')
    og_img_label.grid(row=1, column=1, sticky=tk.NW, padx=25, pady=15)

    arrow1 = tk.Canvas(images_area, bg='gray95', width=200, border=0)
    arrow1.grid(row=1, column=2, sticky=tk.N, pady=75)
    arrow1.create_line(0, 150, 200, 150, fill='black', width=5, arrow=tk.LAST)

    global og_img_spec_label
    og_img_spec_label = tk.Label(images_area, bg='gray95', text='Original image spectrum will appear here', borderwidth=1, relief='solid')
    og_img_spec_label.grid(row=1, column=3, sticky=tk.NE, padx=25, pady=15)
    
    arrow2 = tk.Canvas(images_area, bg='gray95', width=40, height=60, border=0)
    arrow2.grid(row=2, column=3, sticky=tk.E, padx=260)
    arrow2.create_line(20, 0, 20, 60, fill='black', width=5, arrow=tk.LAST)

    global mod_img_label
    mod_img_label = tk.Label(images_area, bg='gray95', text='Modified image will appear here', borderwidth=1, relief='solid')
    mod_img_label.grid(row=3, column=1, sticky=tk.SW, padx=25, pady=15)

    arrow3 = tk.Canvas(images_area, bg='gray95', width=200, border=0)
    arrow3.grid(row=3, column=2, sticky=tk.S, pady=75)
    arrow3.create_line(200, 150, 0, 150, fill='black', width=5, arrow=tk.LAST)
    
    global mod_img_spec_label
    mod_img_spec_label = tk.Label(images_area, bg='gray95', text='Modified image spectrum will appear here', borderwidth=1, relief='solid')
    mod_img_spec_label.grid(row=3, column=3, sticky=tk.SE, padx=25, pady=15)
    
    global controls_area
    controls_area = tk.Frame(frame, bg='gray95', width=200)
    controls_area.config(highlightcolor='black', highlightbackground='black', highlightthickness=1)
    # controls_area.grid(column=6, row=1, columnspan=2)
    controls_area.pack(side='right', expand=False, fill='y', ipadx=25, ipady=25)

    global color_options
    color_options = ['RGB', 'Grayscale']
    global selected 
    selected = tk.StringVar()
    selected.set(color_options[0]) 
    # Dropdown
    global dropdown
    dropdown = tk.OptionMenu(controls_area, selected, *color_options)
    dropdown.config(width=25)
    dropdown.pack(side='top', fill='x', padx=15, pady=50)
    # Radio buttons
    global var_filter
    var_filter = tk.IntVar()
    R1 = tk.Radiobutton(controls_area, text="HPF", variable=var_filter, value=0)
    R1.pack(side='top', fill='x', padx=15, pady=(50,10))
    R2 = tk.Radiobutton(controls_area, text="LPF", variable=var_filter, value=1)
    R2.pack(side='top', fill='x', padx=15, pady=(10,50))
    # Slider radius
    global sli_radius, sli_intensity
    sli_radius = tk.Scale(controls_area, from_=0, to=100, orient=tk.HORIZONTAL, label='Radius of filter', tickinterval=10)
    sli_radius.pack(side='top', fill='x', padx=15, pady=50)
    # Slider intensity
    sli_intensity = tk.Scale(controls_area, from_=0, to=100, orient=tk.HORIZONTAL, label='Dampening intensity', tickinterval=10)
    sli_intensity.pack(side='top', fill='x', padx=15, pady=50)
    # Button to apply filter
    button_filter = tk.Button(controls_area, text = "Filter", height=2, width=15, command = apply_filter)  
    button_filter.pack(side='bottom', fill='x', padx=15, pady=50)

    # Create button for closing the program and to start the File Explorer
    button_explore = tk.Button(root, text = "Select image...", height=2, width=15, command = browseFiles)  
    button_explore.pack(side='left', fill='none', expand=False)

    # Create a File Explorer label and set it's parameters
    global label_file_explorer 
    label_file_explorer= tk.Label(root, text = f"No file selected", height = 5, fg = "black", bg='white')
    label_file_explorer.pack(side='left', fill='x', pady=5, padx=2)
    
    button_exit = tk.Button(root, text = "Exit", height=2, width=10, command = exit)
    button_exit.pack(side='right', fill='none', expand=False)

    # Let the window wait for any events
    root.mainloop()

# check if the process running is the 'main', in that case start 
if __name__ == '__main__':
    main2()