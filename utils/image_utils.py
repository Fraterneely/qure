from PIL import Image
import os

def resize_image(image_path: str, output_size: tuple) -> str:
    """
    Resizes an image to the specified dimensions.

    Parameters:
        image_path (str): The path to the input image.
        output_size (tuple): The desired output size, e.g., (300, 300).

    Returns:
        str: Path to the resized image.
    """
    try:
        with Image.open(image_path) as img:
            img = img.resize(output_size, Image.LANCZOS)
            resized_path = os.path.splitext(image_path)[0] + "_resized.png"
            img.save(resized_path, "PNG")
        return resized_path
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None

def convert_image_format(image_path: str, target_format: str) -> str:
    """
    Converts an image to a specified format.

    Parameters:
        image_path (str): The path to the input image.
        target_format (str): The desired format (e.g., 'JPEG', 'PNG').

    Returns:
        str: Path to the converted image.
    """
    try:
        with Image.open(image_path) as img:
            converted_path = os.path.splitext(image_path)[0] + f".{target_format.lower()}"
            img.save(converted_path, target_format)
        return converted_path
    except Exception as e:
        print(f"Error converting image format: {e}")
        return None

def is_image_file(file_path: str) -> bool:
    """
    Checks if a given file is a valid image.

    Parameters:
        file_path (str): The path to the file to check.

    Returns:
        bool: True if the file is a valid image, False otherwise.
    """
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify if it's an image
        return True
    except (IOError, SyntaxError) as e:
        print(f"Invalid image file: {e}")
        return False
