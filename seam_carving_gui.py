import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from skimage.io import imread

def is_button_clicked():
    file_type = [('Image File','.jpg .png')]
    Dir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes=file_type, initialdir=Dir)
    image_path.set(filepath)
    
    img = imread(filepath)
    image_info.set('image_path (size {}x{}): '.format(img.shape[1], img.shape[0]))

def start_button_clicked():
    path = image_path.get()
    rwidth = rimage_width.get()
    rheight = rimage_height.get()
    if path == '':
        messagebox.showerror('Error', 'Please select an image file')
        return
    if rwidth == '' or rheight == '':
        messagebox.showerror('Error', 'Please enter resize value')
        return
    if not str.isdecimal(rwidth) or not str.isdecimal(rheight):
        messagebox.showerror('Error', 'Please enter numerical value in resizing parameter')
        return

    img = imread(path)    
    height, width, _ = img.shape
    rwidth = int(rwidth)
    rheight = int(rheight)
    if rwidth > width: rwidth = width
    if rheight > height: rheight = height
    os.system('python seam_carving.py {} {} {}'.format(path, rwidth, rheight))

    messagebox.showinfo('Completed', 'the selected image is resized!')
    exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    root.title('seam_carving')

    is_frame = tk.Frame(root)
    is_frame.grid()
    image_info = tk.StringVar()
    image_info.set('image_path: ')
    is_label = tk.Label(is_frame, textvariable=image_info)
    is_label.grid(row=0, column=0)
    image_path = tk.StringVar()
    file_entry = tk.Entry(is_frame, textvariable=image_path, width=50)
    file_entry.grid(row=0, column=1)
    is_button = tk.Button(is_frame, text='Browse', command=is_button_clicked)
    is_button.grid(row=0, column=2)
    
    resize_frame = tk.Frame(root)
    resize_frame.grid()
    rimage_label = tk.Label(resize_frame, text='resize: ')
    rimage_label.grid(row=1, column=0)
    rimage_width = tk.StringVar()
    rimage_width_entry = tk.Entry(resize_frame, textvariable=rimage_width, width=10)
    rimage_width_entry.grid(row=1, column=1)
    tk.Label(resize_frame, text='x').grid(row=1, column=2)
    rimage_height = tk.StringVar()
    rimage_height_entry = tk.Entry(resize_frame, textvariable=rimage_height, width=10)
    rimage_height_entry.grid(row=1, column=3)

    ok_frame = tk.Frame(root)
    ok_frame.grid()
    start_button = tk.Button(ok_frame, text='Start', command=start_button_clicked)
    start_button.grid(row=2, column=0)
    cancel_button = tk.Button(ok_frame, text='Cancel', command=quit)
    cancel_button.grid(row=2, column=1)

    root.mainloop()