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
import urllib.request



tmpThumb = str("tempfile.png")

def createPdfThumb(filename,thumb):        
    print(filename)

    # Extract image
    doc = fitz.open(filename)  # open document
    pix = doc.getPagePixmap(0, alpha=False)  # render page to an image

    # TODO - get in-memory conversion to work? png = pix.getPNGData() ; im = Image.fromarray(png)
    pix.writePNG(tmpThumb)  # store image as a PNG


    # Resize image
    im = Image.open(tmpThumb)

    im.thumbnail((128, 128))

    if not thumb.parent.exists():
        thumb.parent.mkdir(parents=True, exist_ok = True)

    im.save(str(thumb))
    os.remove(tmpThumb)

    pass



def createYouTubeThumb(id, target):
    url = f'https://img.youtube.com/vi/{id}/default.jpg'
    f = urllib.request.urlopen(url)
    thumbnail =open(target,'wb')
    thumbnail.write(f.read())
    thumbnail.close()






if __name__ == "__main__":
    print(os.curdir)

    for i in glob.glob("*.pdf"):
        print(i)
        create(i)
