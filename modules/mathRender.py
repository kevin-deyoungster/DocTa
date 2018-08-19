from sympy import preview
import time
import base64
import os


def convert_latex_to_image(latex_string):
    """
        This function takes in a LaTex string and saves it to [output_path]
    """
    output_filename = str(time.time()) + ".png"
    try:
        preview(latex_string, viewer="file", filename=output_filename, euler=False)

        # Read image to base64 string
        f = open(output_filename, "rb")
        image_base64_string = base64.b64encode(f.read())
        # print(f'Could Render Image: {latex_string}')
        f.close()
        os.remove(output_filename)
        return image_base64_string
    except Exception as e:
        # print(f'Could not render: {latex_string}')
        return None


# print(convert_latex_to_image(
#     r'$\begin{matrix} 2 \\ \ 4, \\ \end{matrix}\begin{matrix} 3 \\ \ 4,\\ \end{matrix}\begin{matrix} 3 \\ \ 2, \\ \end{matrix}$',))
