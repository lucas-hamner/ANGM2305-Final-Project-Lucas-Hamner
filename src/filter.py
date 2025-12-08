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

# FILTERS
def apply_grayscale(img):
    return ImageOps.grayscale(img).convert("RGB")
def apply_sepia(img):
    w, h = img.size
    src = img.load()
    out = Image.new("RGB", (w, h))
    dst = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            tr = int(0.393*r + 0.769*g + 0.189*b)
            tg = int(0.349*r + 0.686*g + 0.168*b)
            tb = int(0.272*r + 0.534*g + 0.131*b)
            dst[x, y] = (min(255, tr), min(255, tg), min(255, tb))
    return out
def apply_invert(img):
    return ImageOps.invert(img)

def apply_blur(img, radius=2.0):
    return img.filter(ImageFilter.GaussianBlur(radius=radius))

def apply_sharpen(img):
    return img.filter(ImageFilter.SHARPEN)

def apply_edges(img):
    return img.filter(ImageFilter.FIND_EDGES)

def apply_pixelate(img, size=10):
    if size <= 1:
        return img
    w, h = img.size
    small_w = max(1, w // size)
    small_h = max(1, h // size)
    small = img.resize((small_w, small_h), Image.NEAREST)
    return small.resize((w, h), Image.NEAREST)

def adjust_brightness(img, factor=1.0):
    return ImageEnhance.Brightness(img).enhance(factor)

def adjust_contrast(img, factor=1.0):
    return ImageEnhance.Contrast(img).enhance(factor)

def adjust_saturation(img, factor=1.0):
    return ImageEnhance.Color(img).enhance(factor)

def apply_filter(img, name, radius=2.0, factor=1.0):
    n = name.lower()
    if n == "grayscale":
        return apply_grayscale(img)
    if n == "sepia":
        return apply_sepia(img)
    if n == "invert":
        return apply_invert(img)
    if n == "blur":
        return apply_blur(img, radius=radius)
    if n == "sharpen":
        return apply_sharpen(img)
    if n == "edges":
        return apply_edges(img)
    if n == "pixelate":
        size = max(1, int(round(factor)))
        return apply_pixelate(img, size=size)
    if n == "brighten":
        return adjust_brightness(img, factor)
    if n == "darken":
        return adjust_brightness(img, factor)
    if n == "contrast+":
        return adjust_contrast(img, factor)
    if n == "contrast-":
        return adjust_contrast(img, factor)
    if n == "saturate+":
        return adjust_saturation(img, factor)
    if n == "saturate-":
        return adjust_saturation(img, factor)
    return img