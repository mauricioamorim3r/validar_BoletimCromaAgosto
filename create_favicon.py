from PIL import Image, ImageDraw
import os

# Create a simple 16x16 favicon


def create_favicon():
    # Create a new image with RGBA mode for transparency
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a simple "B" for BRAVA
    # Blue background circle
    draw.ellipse([1, 1, 14, 14], fill=(0, 102, 204, 255))  # BRAVA blue

    # White "B" letter (simplified)
    draw.rectangle([4, 3, 6, 12], fill=(255, 255, 255, 255))  # Vertical line
    draw.rectangle([4, 3, 10, 5], fill=(255, 255, 255, 255))   # Top horizontal
    draw.rectangle([4, 7, 9, 8], fill=(255, 255, 255, 255))    # Middle horizontal
    draw.rectangle([4, 11, 10, 12], fill=(255, 255, 255, 255))  # Bottom horizontal

    return img


# Create and save favicon
try:
    favicon = create_favicon()
    favicon.save('static/favicon.ico', 'ICO')
    print("Favicon created successfully!")
except Exception as e:
    print(f"Error creating favicon with PIL: {e}")
    # Create a minimal HTML approach instead
    print("Creating simple favicon route...")
