# This module
# - changing list method from ol class to ol type
# - Removing blockquotes

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


def polish(html_path):
    with open(html_path) as f:
        feed = f.read()
        feed = feed.replace("<blockquote>", "").replace("</blockquote>", "")
        html = BeautifulSoup(feed, "html.parser")
        ordered_lists = html.findAll("ol")
        for list in ordered_lists:
            list_type = get_list_type(list)
            if list_type is not None:
                del list["style"]
                list["type"] = str(list_type)

        tables = html.findAll("table")
        for table in tables:
            table["border"] = "1"

        fw = open(html_path, "w")
        fw.write(html.prettify())
        fw.close()


polish(
    "/home/kevin/Desktop/DocTa Web/jobs/07-03-2018.20-08-23/BOOK-Y_1.DOC/index.html")
