MathsJax dependency is too large to deal with this thing. Maybe I should use python plastex

Python plasTex is cool, works basically but doesn't fit the use case of this thing.

Sympy seems to be the best fit with least code:
    - Requires latex to be installed though, that's the only issue 
    - test by running 'latex' in the command line 
    - download from here: https://miktex.org/download

Approach:
- Use sympy to convert latex string to image in path name under [math_image_1.png]
- Make a reference to that image in the docs 
- That's that 


Later : Uniformity of Images
- Uniform image names because some images are named wrongly 
- Loop through all images in the html file 
    - For each image
        - Get src link
        - Rename the image in the src link it according to the counter 
        - Update the src link 
