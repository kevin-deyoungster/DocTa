'''
    This function takes in an html file path and pads it with a body tag (if needed)
'''
import glob
import os
from bs4 import BeautifulSoup


def _wrap_in(string, wrap_tag):
    '''
    Wraps [string] in html tag [wrap_tag]
    '''
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
        soup = BeautifulSoup(html,'html.parser')
        if soup:
            body = soup.find("body")
            if body:
                print("No need!")
            else:
                # The thing needs a body
                print("Need!")
                html = html.decode('utf-8', errors='ignore')

                html = _wrap_in(html,"body")
                # html.encode('utf-8')

                with open(html_path,"wb") as f2:
                    f2.write(html.encode('utf-8'))


walk("/home/kevin/Downloads/sd",".html",bodify)