import torch
import torchvision.transforms as transforms
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from tkinter import ttk, colorchooser, Scale, messagebox, filedialog
import threading
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import colorsys
from scipy.ndimage import gaussian_filter

class ColorCelestialObjectGenerator:
    def __init__(self, image_size=(512, 512)):
        self.image_size = image_size
        self.celestial_objects = {
            'spiral galaxy': self.generate_galaxy,
            'elliptical galaxy': self.generate_elliptical_galaxy,
            'nebula': self.generate_nebula,
            'star cluster': self.generate_star_cluster,
            'planetary nebula': self.generate_planetary_nebula,
            'supernova remnant': self.generate_supernova_remnant,
            'binary star system': self.generate_binary_star,
            'globular cluster': self.generate_globular_cluster
        }
    def generate_base_noise(self, scale=100):
        x = np.linspace(0, scale, self.image_size[0])
        y = np.linspace(0, scale, self.image_size[1])
        x, y = np.meshgrid(x, y)
        noise = np.random.rand(*self.image_size)
        return gaussian_filter(noise, sigma=2)

    def apply_color(self, image, primary_color, secondary_color, blend_factor=0.7):
        image = (image - image.min()) / (image.max() - image.min())
        colored = np.zeros((*self.image_size, 3), dtype=np.float32)

        primary_color = np.array(primary_color) / 255
        secondary_color = np.array(secondary_color) / 255

        for i in range(3):
            colored[:,:,i] = image * (blend_factor * primary_color[i] +
                                    (1 - blend_factor) * secondary_color[i])

        return (colored * 255).astype(np.uint8)

    def add_stars(self, image, density=0.001):
        star_mask = np.random.random(self.image_size) < density
        star_brightness = np.random.randint(180, 256, size=self.image_size)
        for channel in range(3):
            image[:,:,channel][star_mask] = star_brightness[star_mask]
        return image

    def generate_galaxy(self):
        base = self.generate_base_noise()

        center = np.array(self.image_size) // 2
        y, x = np.ogrid[:self.image_size[0], :self.image_size[1]]
        r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
        theta = np.arctan2(y - center[1], x - center[0])

        spiral = np.sin(r/30 - theta*2) + 1

        galaxy = base * spiral * np.exp(-r/100)
        return gaussian_filter(galaxy, sigma=3)

    def generate_nebula(self):
        base = self.generate_base_noise(scale=50)

        layers = [
            gaussian_filter(self.generate_base_noise(scale=30), sigma=4),
            gaussian_filter(self.generate_base_noise(scale=20), sigma=2),
            gaussian_filter(self.generate_base_noise(scale=10), sigma=1)
        ]

        nebula = base
        for layer in layers:
            nebula = nebula * layer

        return nebula

    def generate_star_cluster(self):
        base = np.zeros(self.image_size)

        n_stars = np.random.randint(50, 200)
        for _ in range(n_stars):
            x = np.random.randint(0, self.image_size[0])
            y = np.random.randint(0, self.image_size[1])
            brightness = np.random.random() * 0.8 + 0.2
            sigma = np.random.random() * 2 + 1

            y_grid, x_grid = np.ogrid[:self.image_size[0], :self.image_size[1]]
            r2 = (x_grid - x)**2 + (y_grid - y)**2
            star = np.exp(-r2/(2*sigma**2)) * brightness
            base += star

        return gaussian_filter(base, sigma=0.5)

    def generate_elliptical_galaxy(self):
        base = self.generate_base_noise()

        center = np.array(self.image_size) // 2
        y, x = np.ogrid[:self.image_size[0], :self.image_size[1]]
        r = np.sqrt((x - center[0])**2 + (y - center[1])**2)

        galaxy = base * np.exp(-r/100)
        return gaussian_filter(galaxy, sigma=4)

    def generate_planetary_nebula(self):
        base = self.generate_base_noise()

        center = np.array(self.image_size) // 2
        y, x = np.ogrid[:self.image_size[0], :self.image_size[1]]
        r = np.sqrt((x - center[0])**2 + (y - center[1])**2)

        shell = np.sin(r/10)**2 * np.exp(-r/100)
        return base * shell

    def generate_supernova_remnant(self):
        base = self.generate_base_noise()

        center = np.array(self.image_size) // 2
        y, x = np.ogrid[:self.image_size[0], :self.image_size[1]]
        r = np.sqrt((x - center[0])**2 + (y - center[1])**2)

        shell = np.exp(-(r - 100)**2/1000) * np.random.rand(*self.image_size)
        return gaussian_filter(base * shell, sigma=2)

    def generate_binary_star(self):
        base = np.zeros(self.image_size)

        centers = [
            (self.image_size[0]//2 - 50, self.image_size[1]//2),
            (self.image_size[0]//2 + 50, self.image_size[1]//2)
        ]

        for center in centers:
            y, x = np.ogrid[:self.image_size[0], :self.image_size[1]]
            r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
            star = np.exp(-r/20)
            base += star

        return gaussian_filter(base, sigma=1)

    def generate_globular_cluster(self):
        base = np.zeros(self.image_size)

        center = np.array(self.image_size) // 2
        n_stars = 1000

        for _ in range(n_stars):
            r = np.random.rayleigh(50)
            theta = np.random.random() * 2 * np.pi
            x = int(center[0] + r * np.cos(theta))
            y = int(center[1] + r * np.sin(theta))

            if 0 <= x < self.image_size[0] and 0 <= y < self.image_size[1]:
                brightness = np.random.random() * 0.8 + 0.2
                sigma = np.random.random() + 0.5

                y_grid, x_grid = np.ogrid[:self.image_size[0], :self.image_size[1]]
                r2 = (x_grid - x)**2 + (y_grid - y)**2
                star = np.exp(-r2/(2*sigma**2)) * brightness
                base += star

        return gaussian_filter(base, sigma=0.5)

class CelestialObjectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Celestial Object Generator")
        self.generator = ColorCelestialObjectGenerator()

        self.root.geometry("1200x800")
        self.setup_gui()

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        object_label = ttk.Label(control_frame, text="Object Type:")
        object_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.object_var = tk.StringVar(value="spiral galaxy")
        object_menu = ttk.OptionMenu(control_frame, self.object_var, "spiral galaxy", *self.generator.celestial_objects.keys())
        object_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        size_label = ttk.Label(control_frame, text="Image Size:")
        size_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.size_var = tk.IntVar(value=512)
        size_slider = ttk.Scale(control_frame, from_=128, to=1024, variable=self.size_var, orient=tk.HORIZONTAL)
        size_slider.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        color_frame = ttk.LabelFrame(control_frame, text="Colors", padding="10")
        color_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        primary_color_button = ttk.Button(color_frame, text="Primary Color", command=self.choose_primary_color)
        primary_color_button.grid(row=0, column=0, padx=5, pady=5)
        self.primary_color = (255, 0, 0) 

        secondary_color_button = ttk.Button(color_frame, text="Secondary Color", command=self.choose_secondary_color)
        secondary_color_button.grid(row=0, column=1, padx=5, pady=5)
        self.secondary_color = (0, 0, 255)  

        blend_label = ttk.Label(control_frame, text="Blend Factor:")
        blend_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.blend_var = tk.DoubleVar(value=0.7)
        blend_slider = ttk.Scale(control_frame, from_=0.0, to=1.0, variable=self.blend_var, orient=tk.HORIZONTAL)
        blend_slider.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        effects_frame = ttk.LabelFrame(control_frame, text="Effects", padding="10")
        effects_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.stars_var = tk.BooleanVar(value=True)
        stars_check = ttk.Checkbutton(effects_frame, text="Add Stars", variable=self.stars_var)
        stars_check.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.noise_var = tk.BooleanVar(value=False)
        noise_check = ttk.Checkbutton(effects_frame, text="Add Noise", variable=self.noise_var)
        noise_check.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.blur_var = tk.BooleanVar(value=False)
        blur_check = ttk.Checkbutton(effects_frame, text="Add Blur", variable=self.blur_var)
        blur_check.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.glow_var = tk.BooleanVar(value=False)
        glow_check = ttk.Checkbutton(effects_frame, text="Add Glow", variable=self.glow_var)
        glow_check.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.disable_color_var = tk.BooleanVar(value=False)
        disable_color_check = ttk.Checkbutton(effects_frame, text="Disable Color", variable=self.disable_color_var)
        disable_color_check.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        intensity_frame = ttk.LabelFrame(control_frame, text="Intensities", padding="10")
        intensity_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        star_density_label = ttk.Label(intensity_frame, text="Star Density:")
        star_density_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.star_density = tk.DoubleVar(value=0.5)
        star_density_slider = ttk.Scale(intensity_frame, from_=0.0, to=1.0, variable=self.star_density, orient=tk.HORIZONTAL)
        star_density_slider.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        noise_intensity_label = ttk.Label(intensity_frame, text="Noise Intensity:")
        noise_intensity_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.noise_intensity = tk.DoubleVar(value=0.5)
        noise_intensity_slider = ttk.Scale(intensity_frame, from_=0.0, to=1.0, variable=self.noise_intensity, orient=tk.HORIZONTAL)
        noise_intensity_slider.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        blur_intensity_label = ttk.Label(intensity_frame, text="Blur Intensity:")
        blur_intensity_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.blur_intensity = tk.DoubleVar(value=0.5)
        blur_intensity_slider = ttk.Scale(intensity_frame, from_=0.0, to=1.0, variable=self.blur_intensity, orient=tk.HORIZONTAL)
        blur_intensity_slider.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        glow_intensity_label = ttk.Label(intensity_frame, text="Glow Intensity:")
        glow_intensity_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.glow_intensity = tk.DoubleVar(value=0.5)
        glow_intensity_slider = ttk.Scale(intensity_frame, from_=0.0, to=1.0, variable=self.glow_intensity, orient=tk.HORIZONTAL)
        glow_intensity_slider.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        generate_button = ttk.Button(control_frame, text="Generate Image", command=self.generate_image)
        generate_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.figure = Figure(figsize=(6, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)

    def choose_primary_color(self):
        color = colorchooser.askcolor(title="Choose Primary Color")
        if color[1]:
            self.primary_color = color[0]

    def choose_secondary_color(self):
        color = colorchooser.askcolor(title="Choose Secondary Color")
        if color[1]:
            self.secondary_color = color[0]

    def generate_image(self):
        image = self.generate_current_image()
        self.ax.imshow(image, cmap='gray' if self.disable_color_var.get() else None)
        self.canvas.draw()

    def generate_current_image(self, preview=True):
        obj_type = self.object_var.get()
        size = (self.size_var.get(), self.size_var.get())

        self.generator.image_size = size
        base_image = self.generator.celestial_objects[obj_type]()

        if not self.disable_color_var.get():
            image = self.generator.apply_color(
                base_image,
                self.primary_color,
                self.secondary_color,
                self.blend_var.get()
            )
        else:
            image = np.stack((base_image,)*3, axis=-1)  

        if self.stars_var.get():
            image = self.generator.add_stars(
                image,
                density=self.star_density.get() * 0.002
            )

        if self.noise_var.get():
            noise = np.random.normal(0, self.noise_intensity.get() * 20, image.shape)
            image = np.clip(image + noise, 0, 255).astype(np.uint8)

        if self.blur_var.get():
            sigma = self.blur_intensity.get() * 3
            image = cv2.GaussianBlur(image, (0, 0), sigma)

        if self.glow_var.get():
            glow = cv2.GaussianBlur(image, (0, 0), self.glow_intensity.get() * 10)
            image = cv2.addWeighted(image, 1, glow, 0.5, 0)

        return image

def main():
    root = tk.Tk()
    app = CelestialObjectApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
