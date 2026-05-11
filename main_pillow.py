from PIL import Image


def main():

    # 1. Open the original image
    original = Image.open("data/input_file.png")

    # 2. Define the region to copy (left, upper, right, lower)
    # Example: a 400x400 square starting from the top-left
    box = (0, 200, 400, 400)

    # 3. Crop the image to that box
    cropped_image = original.crop(box)

    # 4. Save as a new PNG
    # PNGs support transparency, which crop() will preserve automatically
    cropped_image.save("data/extracted_part.png")

    print("New image saved successfully!")


if __name__ == "__main__":
    main()
