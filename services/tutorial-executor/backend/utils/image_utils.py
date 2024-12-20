# -*- coding: utf-8 -*-
"""
Image Utilities

This module contains utility functions for handling images, including processing, manipulation, and analysis.
It provides functionalities such as resizing, cropping, converting formats, extracting metadata, and more.
"""

import os
from PIL import Image, ImageOps
import io
import base64
from typing import Tuple, Optional, Dict


class ImageUtils:
    @staticmethod
    def open_image(image_path: str) -> Image.Image:
        """
        Opens an image file and returns it as a PIL Image object.

        Args:
            image_path (str): The path to the image file.

        Returns:
            Image.Image: A PIL Image object representing the opened image.
        """
        try:
            return Image.open(image_path)
        except IOError as e:
            raise Exception(f"Failed to open image at {image_path}: {e}")

    @staticmethod
    def save_image(image: Image.Image, output_path: str, format: Optional[str] = None) -> None:
        """
        Saves a PIL Image object to a specified location.

        Args:
            image (Image.Image): The PIL Image object to save.
            output_path (str): The path where the image will be saved.
            format (Optional[str]): The format to save the image in. If not provided, inferred from the filename extension.
        """
        try:
            image.save(output_path, format=format)
        except IOError as e:
            raise Exception(f"Failed to save image to {output_path}: {e}")

    @staticmethod
    def resize_image(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """
        Resizes an image to the specified dimensions.

        Args:
            image (Image.Image): The PIL Image object to resize.
            size (Tuple[int, int]): A tuple of (width, height) representing the new dimensions.

        Returns:
            Image.Image: A resized PIL Image object.
        """
        return image.resize(size, Image.ANTIALIAS)

    @staticmethod
    def crop_image(image: Image.Image, box: Tuple[int, int, int, int]) -> Image.Image:
        """
        Crops an image to the specified bounding box.

        Args:
            image (Image.Image): The PIL Image object to crop.
            box (Tuple[int, int, int, int]): A tuple of (left, upper, right, lower) defining the crop boundaries.

        Returns:
            Image.Image: A cropped PIL Image object.
        """
        return image.crop(box)

    @staticmethod
    def convert_image_format(image: Image.Image, format: str) -> Image.Image:
        """
        Converts an image to a specified format.

        Args:
            image (Image.Image): The PIL Image object to convert.
            format (str): The desired format of the output image (e.g., 'PNG', 'JPEG').

        Returns:
            Image.Image: A converted PIL Image object.
        """
        if format.lower() == 'jpeg' and image.mode != 'RGB':
            image = image.convert('RGB')
        return image

    @staticmethod
    def rotate_image(image: Image.Image, angle: float, expand: bool = False) -> Image.Image:
        """
        Rotates an image by a specified angle.

        Args:
            image (Image.Image): The PIL Image object to rotate.
            angle (float): The angle in degrees to rotate the image.
            expand (bool): If True, expands the output image to make it large enough to hold the entire rotated image.

        Returns:
            Image.Image: A rotated PIL Image object.
        """
        return image.rotate(angle, expand=expand)

    @staticmethod
    def flip_image(image: Image.Image, method: str) -> Image.Image:
        """
        Flips an image horizontally or vertically.

        Args:
            image (Image.Image): The PIL Image object to flip.
            method (str): The flipping method ('horizontal' or 'vertical').

        Returns:
            Image.Image: A flipped PIL Image object.
        """
        if method.lower() == 'horizontal':
            return image.transpose(Image.FLIP_LEFT_RIGHT)
        elif method.lower() == 'vertical':
            return image.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            raise ValueError("Invalid flip method. Use 'horizontal' or 'vertical'.")

    @staticmethod
    def image_to_base64(image: Image.Image, format: str = 'PNG') -> str:
        """
        Converts a PIL Image object to a base64 encoded string.

        Args:
            image (Image.Image): The PIL Image object to convert.
            format (str): The format of the image (e.g., 'PNG', 'JPEG').

        Returns:
            str: A base64 encoded string representation of the image.
        """
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_str

    @staticmethod
    def base64_to_image(base64_string: str) -> Image.Image:
        """
        Converts a base64 encoded string back into a PIL Image object.

        Args:
            base64_string (str): The base64 encoded string of the image.

        Returns:
            Image.Image: A PIL Image object.
        """
        try:
            img_data = base64.b64decode(base64_string)
            return Image.open(io.BytesIO(img_data))
        except Exception as e:
            raise Exception(f"Failed to decode base64 string to image: {e}")

    @staticmethod
    def get_image_metadata(image_path: str) -> Dict:
        """
        Extracts metadata from an image file.

        Args:
            image_path (str): The path to the image file.

        Returns:
            Dict: A dictionary containing the extracted metadata.
        """
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                if exif_data is not None:
                    return {
                        key: value for key, value in exif_data.items()
                        if key in Image.EXIF_TAGS
                    }
                else:
                    return {}
        except IOError as e:
            raise Exception(f"Failed to extract metadata from image at {image_path}: {e}")

    @staticmethod
    def compress_image(image: Image.Image, quality: int = 85) -> Image.Image:
        """
        Compresses an image while maintaining its dimensions.

        Args:
            image (Image.Image): The PIL Image object to compress.
            quality (int): The quality level for compression (0-100).

        Returns:
            Image.Image: A compressed PIL Image object.
        """
        output_io = io.BytesIO()
        image.save(output_io, format='JPEG', quality=quality, optimize=True)
        output_io.seek(0)
        return Image.open(output_io)

    @staticmethod
    def overlay_images(background: Image.Image, foreground: Image.Image, position: Tuple[int, int]) -> Image.Image:
        """
        Overlays one image on top of another.

        Args:
            background (Image.Image): The background image.
            foreground (Image.Image): The foreground image to overlay.
            position (Tuple[int, int]): The position (x, y) where the foreground will be placed on the background.

        Returns:
            Image.Image: The resulting combined image.
        """
        background.paste(foreground, position, foreground)
        return background