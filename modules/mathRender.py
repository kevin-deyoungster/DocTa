from sympy import preview
import time
import base64
import os


def convert_latex_to_image(latex_string):
    """
        This function takes in a LaTex string and saves it as an image in [output_path]
    """
    output_filename = str(time.time()) + ".png"
    try:
        preview(latex_string, viewer="file", filename=output_filename, euler=False)
        f = open(output_filename, "rb")
        image_base64_string = base64.b64encode(f.read())
        f.close()
        os.remove(output_filename)
        return image_base64_string
    except Exception as e:
        return None
