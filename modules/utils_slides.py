from pathlib import Path
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE


EXTENSIONS_TO_IGNORE = [".html", ".py"]
SLIDE_EXPORTER = "modules/slides.exe"


def export_slides(slide_path, destination):
    process = Popen(
        [SLIDE_EXPORTER, str(slide_path), str(destination)], stdout=PIPE, bufsize=1
    )
    for line in iter(process.stdout.readline, b""):
        print(line.decode("utf-8").strip())
        process.stdout.close()
        return_code = process.wait()
        return return_code == 0


def knit_images_to_soup(image_dir):
    empty_html = "<html><body></body></html>"
    soup = BeautifulSoup(empty_html, "html.parser")
    body = soup.find("body")
    for file in image_dir.glob("**/*"):
        file = Path(file)
        if file.suffix not in EXTENSIONS_TO_IGNORE:
            p_tag = soup.new_tag("p")
            img_tag = soup.new_tag("img", src=file.name)
            p_tag.append(img_tag)
            body.append(p_tag)
    return soup
