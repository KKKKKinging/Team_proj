### ImageFilterApp ###
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import random

### image filter application class using Tkinter ###
class ImageFilterApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Image Filter')
        self.master.geometry('800x550+100+100')
        self.master.resizable(False, False)

        self.file_path = None
        self.displayed_path = None
        self.photo = None

        self.create_widgets()

    ### Load and display image on GUI ###
    def open_image(self):
        self.file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if self.file_path:
            self.display_image()
        # The image file name and address should be in English

    def display_image(self):
        image = Image.open(self.file_path)

        max_width = 330
        max_height = 460

        # Resize the image if it exceeds the maximum size
        if image.width > max_width or image.height > max_height:
            image.thumbnail((max_width, max_height))

            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)
            self.displayed_path = self.file_path

    ### Image Option ###
    def apply_filter(self, filter_function):
        if self.displayed_path:
            original_image = cv2.imread(self.displayed_path)

            if original_image is not None:
                filtered_image = filter_function(original_image)
                converted_image = Image.fromarray(cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB))

                max_width = 330
                max_height = 460

                # Resize the converted image if it exceeds the maximum size
                if converted_image.width > max_width or converted_image.height > max_height:
                    converted_image.thumbnail((max_width, max_height))

                converted_photo = ImageTk.PhotoImage(image=converted_image)

                self.cvt_image_label.config(image=converted_photo)
                self.cvt_image_label.image = converted_photo
            else:
                print(f'Invalid Image: {self.displayed_path}')

    ### Filters ###

    def apply_filters(self, selected_filters):
        if self.displayed_path:
            original_image = cv2.imread(self.displayed_path)

            if original_image is not None:
                result_image = original_image.copy()
                for filter_function in selected_filters:
                    result_image = filter_function(result_image)

                converted_image = Image.fromarray(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
                max_width = 400
                max_height = 460

                if converted_image.width > max_width or converted_image.height > max_height:
                    converted_image.thumbnail((max_width, max_height))

                converted_photo = ImageTk.PhotoImage(image=converted_image)

                self.cvt_image_label.config(image=converted_photo)
                self.cvt_image_label.image = converted_photo
            else:
                print(f'Invalid Image: {self.displayed_path}')

    def cvt_gray(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def cvt_canny(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, 50, 150)
        contour_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return contour_image

    def apply_red_filter(self, image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
        red_filtered_image = cv2.bitwise_and(image, image, mask=red_mask)
        return red_filtered_image

    def apply_yellow_filter(self, image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_yellow = (20, 100, 100)
        upper_yellow = (30, 255, 255)
        yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        yellow_filtered_image = cv2.bitwise_and(image, image, mask=yellow_mask)
        return yellow_filtered_image

    def apply_blue_filter(self, image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_blue = (110, 50, 50)
        upper_blue = (130, 255, 255)
        blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
        blue_filtered_image = cv2.bitwise_and(image, image, mask=blue_mask)
        return blue_filtered_image

    def apply_blur(self, image):
        blurred_image = cv2.GaussianBlur(image, (15, 15), 0)
        return blurred_image

    def apply_invert(self, image):
        inverted_image = cv2.bitwise_not(image)
        return inverted_image

    def apply_random_filter(self, image):
        filter_functions = [self.cvt_gray, self.cvt_canny, self.apply_yellow_filter, self.apply_blue_filter, self.apply_blur, self.apply_invert, self.apply_red_filter]
        selected_filter = random.choice(filter_functions)
        result_image = selected_filter(image)
        return result_image

    ### Labels and GUI creation ###
    def create_widgets(self):
        before_label = tk.Label(self.master, text='Before', font=('Helvetica', 16, 'bold'))
        before_label.place(x=150, y=0)

        after_label = tk.Label(self.master, text='After', font=('Helvetica', 16, 'bold'))
        after_label.place(x=600, y=0)

        self.image_label = tk.Label(self.master)
        self.image_label.place(x=0, y=35)

        self.cvt_image_label = tk.Label(self.master)
        self.cvt_image_label.place(x=450, y=35)

        select_img = tk.Button(self.master, text='Select Image', command=self.open_image)
        select_img.place(relx=0.5, rely=0.1, anchor=tk.N)

        apply_gray_filters_button = tk.Button(self.master, text='Gray', command=lambda: self.apply_filter(self.cvt_gray))
        apply_gray_filters_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        apply_contour_filters_button = tk.Button(self.master, text='Contour', command=lambda: self.apply_filter(self.cvt_canny))
        apply_contour_filters_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        apply_invert_filter_button = tk.Button(self.master, text='Invert Filter', command=lambda: self.apply_filter(self.apply_invert))
        apply_invert_filter_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        apply_red_filter_button = tk.Button(self.master, text='Red Filter', command=lambda: self.apply_filter(self.apply_red_filter))
        apply_red_filter_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        apply_yellow_filter_button = tk.Button(self.master, text='Yellow Filter', command=lambda: self.apply_filter(self.apply_yellow_filter))
        apply_yellow_filter_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        apply_blue_filter_button = tk.Button(self.master, text='Blue Filter', command=lambda: self.apply_filter(self.apply_blue_filter))
        apply_blue_filter_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        apply_random_filter_button = tk.Button(self.master, text='Random Filter', command=lambda: self.apply_filter(self.apply_random_filter))
        apply_random_filter_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

### Execution ###
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()