import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageEnhance
import os

def fuzzy_adjust(value, param_name):
    if param_name == 'focus':
        return min(100, max(0, value * 1.2))
    elif param_name == 'brightness':
        return min(100, max(0, value * 0.8))
    elif param_name == 'stabilization':
        return min(100, max(0, value * 1.1))
    elif param_name == 'iso':
        return min(100, max(0, value * 1.3))

def adjust_image(auto_mode=False):
    global img_display, adjusted_img
    img = original_img.copy()

    # Adjust sharpness
    sharpness = sharpness_slider.get() if not auto_mode else fuzzy_adjust(sharpness_slider.get(), 'focus')
    sharpness_label_value.config(text=f"{int(sharpness)}%")  # Update sharpness label
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpness / 50)

    # Adjust brightness
    brightness = brightness_slider.get() if not auto_mode else fuzzy_adjust(brightness_slider.get(), 'brightness')
    brightness_label_value.config(text=f"{int(brightness)}%")  # Update brightness label
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness / 50)

    # Adjust ISO
    iso = iso_slider.get() if not auto_mode else fuzzy_adjust(iso_slider.get(), 'iso')
    iso_label_value.config(text=f"{int(iso)}%")  # Update ISO label
    enhancer = ImageEnhance.Brightness(img)  # ISO affects brightness
    img = enhancer.enhance(iso / 50)

    # Adjust stabilization
    stabilization = stabilization_slider.get() if not auto_mode else fuzzy_adjust(stabilization_slider.get(), 'stabilization')
    stabilization_label_value.config(text=f"{int(stabilization)}%")  # Update stabilization label
    img = img.rotate(stabilization / 50 - 1)

    # Update canvas with the adjusted image
    img_display = ImageTk.PhotoImage(img)
    adjusted_img = img
    canvas.create_image(160, 120, image=img_display)

def toggle_auto_mode():
    auto_mode.set(not auto_mode.get())
    auto_button.config(text="Auto Mode: ON" if auto_mode.get() else "Auto Mode: OFF")
    adjust_image(auto_mode.get())

def save_image():
    global adjusted_img
    if adjusted_img:
        directory = filedialog.askdirectory()
        if directory:
            file_path = os.path.join(directory, "captured_image.jpg")
            adjusted_img.save(file_path)
            print(f"Image saved to {file_path}")

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Camera Settings")
    settings_window.geometry("300x200")

    tk.Label(settings_window, text=f"Sharpness: {sharpness_slider.get()}").pack()
    tk.Label(settings_window, text=f"Brightness: {brightness_slider.get()}").pack()
    tk.Label(settings_window, text=f"ISO: {iso_slider.get()}").pack()
    tk.Label(settings_window, text=f"Stabilization: {stabilization_slider.get()}").pack()

def open_gallery():
    os.system("explorer .")

root = tk.Tk()
root.title("Digital Camera Viewer")

original_img = Image.open("KamenRiderDecade.png")
original_img = original_img.resize((250, 250), Image.Resampling.LANCZOS)
img_display = ImageTk.PhotoImage(original_img)
adjusted_img = None

viewer_frame = tk.Frame(root, width=320, height=240, bg='black', relief=tk.SUNKEN, bd=10)
viewer_frame.grid(row=0, column=0, columnspan=3, pady=20)

canvas = tk.Canvas(viewer_frame, width=320, height=240, bg="grey")
canvas.pack()

ttk.Label(root, text="Autofocus (Sharpness)").grid(row=1, column=0)
sharpness_slider = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda val: adjust_image())
sharpness_slider.grid(row=1, column=1, columnspan=2)
sharpness_label_value = ttk.Label(root, text="50%") 
sharpness_label_value.grid(row=1, column=3)


ttk.Label(root, text="Exposure (Brightness)").grid(row=2, column=0)
brightness_slider = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda val: adjust_image())
brightness_slider.grid(row=2, column=1, columnspan=2)
brightness_label_value = ttk.Label(root, text="50%") 
brightness_label_value.grid(row=2, column=3)


ttk.Label(root, text="ISO").grid(row=3, column=0)
iso_slider = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda val: adjust_image())
iso_slider.grid(row=3, column=1, columnspan=2)
iso_label_value = ttk.Label(root, text="50%")
iso_label_value.grid(row=3, column=3)

ttk.Label(root, text="Stabilization (Motion)").grid(row=4, column=0)
stabilization_slider = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda val: adjust_image())
stabilization_slider.grid(row=4, column=1, columnspan=2)
stabilization_label_value = ttk.Label(root, text="50%")
stabilization_label_value.grid(row=4, column=3)

auto_mode = tk.BooleanVar(value=False)
auto_button = ttk.Button(root, text="Auto Mode: OFF", command=toggle_auto_mode)
auto_button.grid(row=5, column=0, columnspan=3)


tk.Button(root, text="Capture", width=10, command=save_image).grid(row=6, column=0, pady=10)
tk.Button(root, text="Settings", width=10, command=open_settings).grid(row=6, column=1, pady=10)
tk.Button(root, text="Gallery", width=10, command=open_gallery).grid(row=6, column=2, pady=10)

root.mainloop()
