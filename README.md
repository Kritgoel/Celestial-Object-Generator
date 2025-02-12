# Celestial Object Generator

A Python-based application that generates realistic-looking celestial objects using procedural generation techniques. This interactive tool allows users to create various astronomical objects with customizable properties and effects.

## Features

- Generate multiple types of celestial objects:
  - Spiral galaxies
  - Elliptical galaxies
  - Nebulae
  - Star clusters
  - Planetary nebulae
  - Supernova remnants
  - Binary star systems
  - Globular clusters

- Customizable parameters:
  - Image size (128px to 1024px)
  - Primary and secondary colors
  - Color blend factor
  - Star density
  - Noise intensity
  - Blur effects
  - Glow effects

## Installation

1. Clone this repository or download the source code.

2. Install the required dependencies:
```bash
pip install torch torchvision numpy opencv-python matplotlib Pillow scipy
```

## Usage

1. Run the application:
```bash
python celestial_generator.py
```

2. Use the GUI controls to:
   - Select the type of celestial object
   - Adjust the image size
   - Choose primary and secondary colors
   - Modify the blend factor
   - Toggle and adjust various effects

3. Click "Generate Image" to create a new celestial object with the current settings.

## Controls

### Basic Settings
- **Object Type**: Choose from various celestial objects
- **Image Size**: Adjust the output image dimensions (128px to 1024px)
- **Colors**:
  - Primary Color: Main color of the object
  - Secondary Color: Accent color for blending
  - Blend Factor: Controls the mix between primary and secondary colors
  - Disable Color: Generate monochrome images

### Effects
- **Stars**: Add background stars with adjustable density
- **Noise**: Add noise texture with controllable intensity
- **Blur**: Apply Gaussian blur with adjustable strength
- **Glow**: Add atmospheric glow effect with adjustable intensity

### Intensity Controls
- Star Density: Control the number of background stars
- Noise Intensity: Adjust the strength of the noise effect
- Blur Intensity: Control the amount of blur
- Glow Intensity: Adjust the strength of the glow effect

## Requirements

- Python 3.6+
- PyTorch
- torchvision
- NumPy
- OpenCV (cv2)
- Matplotlib
- Pillow
- SciPy
- tkinter (usually comes with Python)

## Technical Details

The application uses various mathematical techniques to generate celestial objects:
- Perlin noise for base texture generation
- Gaussian filters for smooth gradients
- Procedural algorithms for specific object characteristics
- Color blending using RGB space
- Post-processing effects using OpenCV

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
