import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

### Load and display image on GUI ###
def open_image():
    global file_path
    file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
    if file_path:
        display_image(file_path)

def display_image(file_path):
    global photo, displayed_path
    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    displayed_path = file_path

### Image Option ###
def apply_filter(filter_function):
    if displayed_path:
        original_image = cv2.imread(displayed_path)

        if original_image is not None: 
            filtered_image = filter_function(original_image)

            converted_image = Image.fromarray(cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB))

            converted_photo = ImageTk.PhotoImage(image=converted_image)

            cvt_image_label.config(image=converted_photo)
            cvt_image_label.image = converted_photo
        else:
            print(f'Invalid Image: {displayed_path}')
            print('Invalid Image')

def cvt_gray(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def cvt_canny(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 50, 150)
    contour_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return contour_image

def apply_yellow_filter(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = (20, 100, 100)
    upper_yellow = (30, 255, 255)
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    yellow_filtered_image = cv2.bitwise_and(image, image, mask=yellow_mask)
    return yellow_filtered_image

def apply_blue_filter(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = (110, 50, 50)
    upper_blue = (130, 255, 255)
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    blue_filtered_image = cv2.bitwise_and(image, image, mask=blue_mask)
    return blue_filtered_image

def apply_blur(image):
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)
    return blurred_image

### cvt to contour ###
def cvt_canny():
    if displayed_path:
        original_image = cv2.imread(displayed_path)

        ### image successfully opened ###
        if original_image is not None:
            gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            
            # Canny edge detection
            edges = cv2.Canny(gray_image, 50, 150)
            contour_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            # OpenCV to PIL image
            converted_image = Image.fromarray(contour_image)
            
            # PIL to Tkinter PhotoImage
            converted_photo = ImageTk.PhotoImage(image=converted_image)
            
            # display converted image
            cvt_image_label.config(image=converted_photo)
            cvt_image_label.image = converted_photo
        else:
            print('Invalid Image')

### GUI design ###
win = tk.Tk()
win.title('Image Film')
win.geometry('800x550+100+100')
win.resizable(False, False)

### Labels ###
before_label = tk.Label(win, text='Before', font=('Helvetica', 16, 'bold'))
before_label.place(x=150, y=0)

after_label = tk.Label(win, text='After', font=('Helvetica', 16, 'bold'))
after_label.place(x=600, y=0)

image_label = tk.Label(win)
image_label.place(x=0, y=35)

cvt_image_label = tk.Label(win) # for converted image display
cvt_image_label.place(x=480, y=35)

### Buttons ###
select_img = tk.Button(win, text='Select Image', command=open_image)
select_img.place(relx=0.5, rely=0, anchor=tk.N)

change_img1 = tk.Button(win, text='Gray', command=lambda: apply_filter(cvt_gray))
change_img1.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

change_img2 = tk.Button(win, text='Contour', command=lambda: apply_filter(cvt_canny))
change_img2.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

apply_yellow_filter_button = tk.Button(win, text='Apply Yellow Filter', command=lambda: apply_filter(apply_yellow_filter))
apply_yellow_filter_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

apply_blue_filter_button = tk.Button(win, text='Apply Blue Filter', command=lambda: apply_filter(apply_blue_filter))
apply_blue_filter_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

apply_blur_button = tk.Button(win, text='Apply Blur', command=lambda: apply_filter(apply_blur))
apply_blur_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

### Execution ###
win.mainloop()
