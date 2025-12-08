# STYLE FX PROJECT

# IMPORTS
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# IMAGE I/O
def load_image(path):
    return Image.open(path).convert("RGB")
def save_image(img, path):
    img.save(path)