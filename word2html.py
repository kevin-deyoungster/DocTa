import os
import pypandoc
from tidylib import tidy_document


def convert_to_html(filename):

    directory = os.path.dirname(filename).encode('unicode_escape').decode()
    # Do the conversion with pandoc
    output = pypandoc.convert(
        filename, 'html', extra_args=[r'--extract-media=' + directory, "-M2GB"])

    # Clean up with tidy...
    output, errors = tidy_document(output,  options={
        'numeric-entities': 1,
        'tidy-mark': 0,
        'wrap': 80,
    })

    # replace smart quotes.
    output = output.replace(u"\u2018", '&lsquo;').replace(
        u"\u2019", '&rsquo;')
    output = output.replace(u"\u201c", "&ldquo;").replace(
        u"\u201d", "&rdquo;")

    # write the output and errors
    filename, ext = os.path.splitext(filename)
    directory = os.path.dirname(filename)

    error_filename = "{0}.txt".format(filename)
    with open(error_filename, 'w') as err:
        if(errors):
            err.write(errors)

    filename = "{0}".format(os.path.join(directory, "index.html"))
    with open(filename, 'w') as f:
        # Python 2 "fix". If this isn't a string, encode it.
        if type(output) is not str:
            output = output.encode('utf-8')
        f.write(output)

    return filename
