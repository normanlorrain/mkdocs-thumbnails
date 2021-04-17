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

class Handout:
    def __init__(self, filename):
        print(filename)
        self.filename = filename
        self.name, _ = os.path.splitext(os.path.basename(filename))
        self.thumb = f"{self.name}-thumb.png"

    def createTarget(self):
        print("createTarget", self.name)
        doc = fitz.open((self.filename))  # open document
        pix = doc.getPagePixmap(0, alpha=False)  # render page to an image

        # TODO - get in-memory conversion to work? png = pix.getPNGData() ; im = Image.fromarray(png)
        pix.writePNG(tmpThumb)  # store image as a PNG
        im = Image.open(tmpThumb)

        im.thumbnail((128, 128))
        im.save(str(self.thumb))
        os.remove(tmpThumb)

        pass

    def __repr__(self):
        return f"Handout:{self.name}"

    pass


if __name__ == "__main__":
    print(os.curdir)

    for i in glob.glob("*.pdf"):
        print(i)
        handout = Handout(i)
        handout.createTarget()
