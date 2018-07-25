from sympy import preview
import base64


def convert_latex_to_image(latex_string, output_path):
    '''
        This function takes in a LaTex string and saves it to [output_path]
    '''
    # Convert latex to image
    preview(latex_string, viewer='file', filename=output_path, euler=False)

    # Read image to base64 string
    with open(filename, 'rb') as f:
        str = base64.b64encode(f.read())
        return str


convert_latex_to_image(
    r'$\begin{matrix} 2 \\ \ 4, \\ \end{matrix}\begin{matrix} 3 \\ \ 4,\\ \end{matrix}\begin{matrix} 3 \\ \ 2, \\ \end{matrix}$',
    '../playground/test.png')
