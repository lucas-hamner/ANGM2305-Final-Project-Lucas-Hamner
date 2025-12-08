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

# GUI
class StyleFXApp:
    def __init__(self, root):
        self.root = root
        root.title("Style FX")
        self.img_orig: Optional[Image.Image] = None
        self.img_preview: Optional[Image.Image] = None
        self.preview_tk = None
        self.preview_w, self.preview_h = 640, 480
        blank = Image.new("RGB", (self.preview_w, self.preview_h), (34, 34, 34))
        self.preview_tk = ImageTk.PhotoImage(blank)
        self.preview_label = tk.Label(root, image=self.preview_tk, bg="#222")
        self.preview_label.grid(row=0, column=0, rowspan=9, padx=8, pady=8)
        tk.Button(root, text="Load Image", command=self.on_load).grid(row=0, column=1, sticky="ew", padx=8, pady=4)
        tk.Button(root, text="Save Image", command=self.on_save).grid(row=1, column=1, sticky="ew", padx=8, pady=4)
        tk.Label(root, text="Filter:").grid(row=2, column=1, sticky="w", padx=8)
        self.filter_var = tk.StringVar(value="grayscale")
        self.filter_menu = ttk.Combobox(root,
            values=[
                "grayscale", "sepia", "invert", "blur", "sharpen", "edges", "pixelate",
                "brighten", "darken", "contrast+", "contrast-", "saturate+", "saturate-"
            ],
            textvariable=self.filter_var, state="readonly")
        self.filter_menu.grid(row=3, column=1, padx=8, pady=4, sticky="ew")
        tk.Label(root, text="Blur radius:").grid(row=4, column=1, sticky="w", padx=8)
        self.blur_var = tk.DoubleVar(value=2.0)
        self.blur_slider = tk.Scale(root, from_=0.0, to=10.0, resolution=0.5,
                                    orient="horizontal", variable=self.blur_var, length=180)
        self.blur_slider.grid(row=5, column=1, padx=8, pady=4)
        tk.Label(root, text="Factor (brightness/contrast/sat/pixel-size):").grid(row=6, column=1, sticky="w", padx=8)
        self.factor_var = tk.DoubleVar(value=1.0)
        self.factor_slider = tk.Scale(root, from_=0.2, to=10.0, resolution=0.1,
                                      orient="horizontal", variable=self.factor_var, length=180)
        self.factor_slider.grid(row=7, column=1, padx=8, pady=4)
        tk.Button(root, text="Apply Filter", command=self.on_apply).grid(row=8, column=1, sticky="ew", padx=8, pady=6)
    def on_load(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not path:
            return
        try:
            self.img_orig = load_image(path)
        except Exception as e:
            messagebox.showerror("Load error", f"Could not load image: {e}")
            return
        self.img_preview = self.img_orig.copy()
        self.show_preview(self.img_preview)
    def on_apply(self):
        if self.img_orig is None:
            messagebox.showinfo("No image", "Please load an image first.")
            return
        name = self.filter_var.get()
        radius = float(self.blur_var.get())
        factor = float(self.factor_var.get())
        try:
            out = apply_filter(self.img_orig, name, radius=radius, factor=factor)
        except Exception as e:
            messagebox.showerror("Filter error", str(e))
            return
        self.img_preview = out
        self.show_preview(self.img_preview)
    def on_save(self):
        if self.img_preview is None:
            messagebox.showinfo("Nothing to save", "Apply a filter first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg")])
        if not path:
            return
        try:
            save_image(self.img_preview, path)
            messagebox.showinfo("Saved", f"Saved to {path}")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

    def show_preview(self, img):
        thumb = img.copy()
        max_w, max_h = self.preview_w, self.preview_h
        w, h = thumb.size
        scale = min(max_w / w, max_h / h, 1.0)
        new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        out_thumb = thumb.resize(new_size, Image.LANCZOS)
        bg = Image.new("RGB", (max_w, max_h), (34, 34, 34))
        x = (max_w - out_thumb.width) // 2
        y = (max_h - out_thumb.height) // 2
        bg.paste(out_thumb, (x, y))
        self.preview_tk = ImageTk.PhotoImage(bg)
        self.preview_label.configure(image=self.preview_tk)

# MAIN
def main():
    root = tk.Tk()
    app = StyleFXApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()