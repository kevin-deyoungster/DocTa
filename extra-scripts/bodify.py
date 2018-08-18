"""
    This function takes in an html file path and pads it with a body tag (if needed)
"""
import glob
import os
from bs4 import BeautifulSoup


def _wrap_in(string, wrap_tag):
    """
    Wraps [string] in html tag [wrap_tag]
    """
    open = f"<{wrap_tag}>"
    close = f"</{wrap_tag}>"
    return f"{open}{string}{close}"


def walk(folder, target_extension, function):
    files = []
    for filename in glob.iglob(f"{folder}/**/*.html", recursive=True):
        file = os.path.join(folder, filename)
        function(file)
    return True


def bodify(html_path):
    with open(html_path, "rb") as f:
        html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        if soup:
            body = soup.find("body")
            if body:
                # print("No need body!")
                soup_html = soup.find("html")
                if not soup_html:
                    html_tag = "<!DOCTYPE html PUBLIC '-//W3C//DTD HTML 4.01//EN'>"
                    open_tag = "<html>"
                    closing_tag = "</html>"
                    try:
                        new_html = (
                            html_tag + open_tag + html.decode("utf-8") + closing_tag
                        )
                        # print(new_html)
                        f = open(html_path, "wb")
                        f.write(new_html.encode("utf-8"))
                    except Exception as e:
                        print(f"Error handling {html_path}")
            else:
                html_tag = "<!DOCTYPE html PUBLIC '-//W3C//DTD HTML 4.01//EN'>"
                open_tag = "<html><body>"
                closing_tag = "</body></html>"
                try:
                    new_html = html_tag + open_tag + html.decode("utf-8") + closing_tag
                    # print(new_html)
                    f = open(html_path, "wb")
                    f.write(new_html.encode("utf-8"))
                except Exception as e:
                    print(f"Error handling {html_path}")
            # print("Need a body!")


walk(".", ".html", bodify)

