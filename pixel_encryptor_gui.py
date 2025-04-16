#!/usr/bin/env python3
"""
Pixel Manipulation Image Encryption Tool with GUI
Author: ProDigy Infotech
Description:
A simple GUI tool that encrypts and decrypts images by swapping and shifting pixel values.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def swap_pixels(img):
    pixels = img.load()
    width, height = img.size
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            try:
                p1 = pixels[x, y]
                p2 = pixels[x+1, y+1]
                pixels[x, y], pixels[x+1, y+1] = p2, p1
            except IndexError:
                continue
    return img

def shift_pixels(img, shift):
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            pixels[x, y] = ((r + shift) % 256,
                            (g + shift) % 256,
                            (b + shift) % 256)
    return img

def encrypt_image(img, shift):
    img = swap_pixels(img)
    img = shift_pixels(img, shift)
    return img

def decrypt_image(img, shift):
    img = shift_pixels(img, -shift)
    img = swap_pixels(img)
    return img

def open_image():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not path:
        return
    try:
        img = Image.open(path).convert("RGB")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open image: {e}")
        return
    app_state['img_path'] = path
    app_state['img'] = img
    display_image(img)

def display_image(img):
    img_thumb = img.copy()
    img_thumb.thumbnail((300, 300))
    tk_img = ImageTk.PhotoImage(img_thumb)
    image_label.config(image=tk_img)
    image_label.image = tk_img

def process_image():
    if 'img' not in app_state:
        messagebox.showwarning("Warning", "Please open an image first.")
        return
    try:
        shift = int(shift_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Shift must be an integer.")
        return
    img = app_state['img'].copy()
    if mode.get() == "Encrypt":
        result = encrypt_image(img, shift)
    else:
        result = decrypt_image(img, shift)
    app_state['result'] = result
    display_image(result)

def save_image():
    if 'result' not in app_state:
        messagebox.showwarning("Warning", "No processed image to save.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".png",
                                        filetypes=[("PNG files","*.png"),("JPEG files","*.jpg;*.jpeg")])
    if not path:
        return
    try:
        app_state['result'].save(path)
        messagebox.showinfo("Saved", f"Image saved to {path}")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot save image: {e}")

# GUI setup
root = tk.Tk()
root.title("Pixel Image Encryption Tool")
root.geometry("400x550")

app_state = {}

# Open button
tk.Button(root, text="Open Image", command=open_image).pack(pady=5)

# Image display
image_label = tk.Label(root)
image_label.pack(pady=5)

# Shift entry
tk.Label(root, text="Shift Value:").pack()
shift_entry = tk.Entry(root)
shift_entry.pack(pady=5)
shift_entry.insert(0, "30")

# Mode selection
mode = tk.StringVar(value="Encrypt")
tk.Radiobutton(root, text="Encrypt", variable=mode, value="Encrypt").pack()
tk.Radiobutton(root, text="Decrypt", variable=mode, value="Decrypt").pack()

# Process and Save buttons
tk.Button(root, text="Process Image", command=process_image).pack(pady=10)
tk.Button(root, text="Save Image", command=save_image).pack(pady=5)

root.mainloop()
