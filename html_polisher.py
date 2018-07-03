# This module
# - changing list method from ol class to ol type
# - Removing blockquotes
# - Convert table border from 0 to 1

from bs4 import BeautifulSoup


def get_list_type(html_list):
    type_dict = {
        "lower-roman": "i",
        "upper-roman": "I",
        "decimal": "1",
        "lower-alpha": "a",
        "upper-alpha": "A"
    }
    if "style" in html_list:
        type = html_list["style"].split(':')[1].replace(" ", "")
        return(type_dict[type])
    else:
        return None


# Remove Blockquotes
# Convert list styles
from os import path


def polish(html_path):
    with open(html_path) as f:

        # Remove blockquotes
        feed = f.read()
        feed = feed.replace("<blockquote>", "").replace("</blockquote>", "")

        # Convert list styling
        html = BeautifulSoup(feed, "html.parser")
        ordered_lists = html.findAll("ol")
        for list in ordered_lists:
            list_type = get_list_type(list)
            if list_type is not None:
                del list["style"]
                list["type"] = str(list_type)

        # Add borders to table
        tables = html.findAll("table")
        for table in tables:
            table["border"] = "1"

        # Fix Image Paths
        images = html.find_all('img')
        for image in images:
            if image.get('height'):
                del image['height']

            if image.get('width'):
                del image['width']
            image['max-width'] = '100%'
            image['src'] = path.basename(image['src'])

        # Output new file
        fw = open(html_path, "w")
        fw.write(html.prettify())
        fw.close()
