import glob
import shutil
import tempfile
from pathlib import Path
import os
from urllib.request import pathname2url
import sys
import json
import fitz
from PIL import Image
from jinja2 import Environment, FileSystemLoader, select_autoescape




tmpThumb = str("tempfile.png")

def create(filename,target):        
    print(filename)
    filename = filename
    name, _ = os.path.splitext(os.path.basename(filename))
    thumb = target


    # Extract image
    doc = fitz.open((filename))  # open document
    pix = doc.getPagePixmap(0, alpha=False)  # render page to an image

    # TODO - get in-memory conversion to work? png = pix.getPNGData() ; im = Image.fromarray(png)
    pix.writePNG(tmpThumb)  # store image as a PNG


    # Resize image
    im = Image.open(tmpThumb)

    im.thumbnail((128, 128))
    im.save(str(thumb))
    os.remove(tmpThumb)

    pass


if __name__ == "__main__":
    print(os.curdir)

    for i in glob.glob("*.pdf"):
        print(i)
        create(i)
