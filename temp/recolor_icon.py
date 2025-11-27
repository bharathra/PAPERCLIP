
import os
import sys

# Add local libs to path
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))
from PyQt6.QtGui import QImage, QColor


def recolor_icon():
    input_path = "icons/paper_clip.png"
    output_path = "icons/paper_clip_grey.png"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found")
        return

    image = QImage(input_path)
    if image.isNull():
        print("Error: Failed to load image")
        return

    # Create a new image with the same dimensions
    new_image = QImage(image.size(), QImage.Format.Format_ARGB32)
    new_image.fill(QColor(0, 0, 0, 0))

    # Dark grey color (standard material grey)
    grey = QColor("#777777")

    for x in range(image.width()):
        for y in range(image.height()):
            pixel_color = image.pixelColor(x, y)
            # If pixel is not transparent, make it grey while preserving alpha
            if pixel_color.alpha() > 0:
                new_color = QColor(grey)
                new_color.setAlpha(pixel_color.alpha())
                new_image.setPixelColor(x, y, new_color)

    new_image.save(output_path)
    print(f"Created {output_path}")


if __name__ == "__main__":
    recolor_icon()
