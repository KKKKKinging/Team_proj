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
    ### image file address should be English only
    global photo, displayed_path
    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    displayed_path = file_path

### Image Option ###
def cvt_gray():
    if displayed_path:
        original_image = cv2.imread(displayed_path)

        ### image successfully opened ###
        if original_image is not None: 
            gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        
            # OpenCV to PIL image
            converted_image = Image.fromarray(gray_image)
            
            # PIL to Tkinter PhotoImage
            converted_photo = ImageTk.PhotoImage(image=converted_image)
            
            # display converted image
            cvt_image_label.config(image=converted_photo)
            cvt_image_label.image = converted_photo
        else:
            print(f'Invalid Image: {displayed_path}')


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

change_img1 = tk.Button(win, text='Gray', command=cvt_gray)
change_img1.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

change_img2 = tk.Button(win, text='cvt') # modify, add command
change_img2.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

### Execution ###
win.mainloop()