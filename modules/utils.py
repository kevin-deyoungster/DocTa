import os
import pypandoc
import shutil
import base64
from PIL import Image
from bs4 import BeautifulSoup
from pathlib import Path
from modules import math_renderer
from tidylib import tidy_document

"""
    This module contains functions that are used for the basic operations such as conversion with pandoc
    and tidylib, moving files about, saving files to storage, etc. 
"""


def move_files(source, destination):
    """
        Move files from source to destination
    """
    images_moved_count = 0
    if source.exists():
        for file in [file for file in source.glob("**/*") if file.is_file()]:
            shutil.move(str(file), str(destination))
            images_moved_count += 1
        shutil.rmtree(source)
    print(f"\t[Image-Mover]: Moved {images_moved_count} images to job folder")


EXTENSIONS_TO_IGNORE = [".jpg", ".png", ".jpeg", ".html", ".py", ".gif"]
TARGET_IMAGE_EXTENSION = ".jpg"


def convert_invalid_images_in(root):
    """
    Converted all unsupported images to supported format
    """
    converted_images_count = 0
    for file in root.glob("**/*"):
        file = Path(file)
        if file.suffix not in EXTENSIONS_TO_IGNORE:
            destination_file = file.with_suffix(TARGET_IMAGE_EXTENSION)
            try:
                Image.open(file).convert("RGB").save(destination_file)
                file.unlink()
                converted_images_count += 1
            except Exception as e:
                print(e)
    print(f"\t[Image-Converter]: Converted {converted_images_count} invalid images")


def rename_image_files_in(root):
    """
        Renames all image files in order
    """
    img_count = 0
    index_file = root / "index.html"
    html_soup = BeautifulSoup(open(index_file, "rb"), "html.parser")
    images = html_soup.findAll("img")
    for image in images:
        old_image = root / image["src"]
        if old_image.exists():
            image_extension = old_image.suffix
            new_image = old_image.with_name(
                "image" + str(img_count + 1).rjust(3, "0")
            ).with_suffix(image_extension)
            old_image.rename(new_image)
            image["src"] = new_image.stem + new_image.suffix
            img_count += 1
    with open(index_file, "wb") as f:
        f.write(html_soup.prettify().encode("utf-8"))
    print(f"\t[Image-Renamer]: Renamed {img_count} images")


def render_maths(html, destination):
    """
        Renders formulas and LaTex stuff to images 
    """
    html_soup = BeautifulSoup(html, "html.parser")
    math_spans = html_soup.findAll("span", {"class": ["math inline", "math display"]})
    formula_count = 1
    for math_span in math_spans:
        latex_string = math_span.text.strip().replace("\n", "")
        try:
            image_base64_string = math_renderer.convert_latex_to_image(latex_string)
            if image_base64_string:
                print(f"\t[Math-Render]: Rendered {latex_string[:20]}")
                image_name = destination / f"math-image{formula_count}.png"
                __save_BASE64_to_file(image_name, image_base64_string)
                img_tag = html_soup.new_tag("img", src=image_name)
                math_span.replaceWith(img_tag)
                formula_count += 1
        except Exception as e:
            print(f"\t[Math-Render]: No Render {latex_string[:20]}")
            print(f"\t{e}")
    return html_soup


def convert_HTML(data_string, media_destination):
    """
        Converts docx data to html, puts the images extracted in media_destination
    """
    output_html = pypandoc.convert_text(
        data_string,
        format="docx",
        to="html",
        extra_args=[r"--extract-media=" + media_destination],
    )
    return output_html


def tidy_HTML(html_content):
    """
        Tidies html_content with TidyLib
    """
    output, _ = tidy_document(
        html_content, options={"numeric-entities": 1, "tidy-mark": 0, "wrap": 80}
    )

    # Replace smart quotes with normal quotes and em dashes to avoid char encoding errors
    output = (
        output.replace("\u2018", "&lsquo;")
        .replace("\u2019", "&rsquo;")
        .replace("\u201c", "&ldquo;")
        .replace("\u201d", "&rdquo;")
    )

    return output


def save_HTML(html_output, destination, filename):
    """
        Saves raw html output to destination + filename
    """
    output_file = destination / filename
    with open(output_file, "wb") as f:
        f.write(html_output)
        return output_file


def __save_BASE64_to_file(filepath, base64_string):
    """
        Saves base64 strings to file
    """
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(base64_string))
    return True


def delete_directory(directory):
    """
        Clears directory from existence
    """
    shutil.rmtree(directory)


def zip_up(archive_name, directory):
    """
        Compresses directory into a zip file
    """
    return shutil.make_archive(archive_name, "zip", directory)
