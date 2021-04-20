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

def createPdfThumb(filename,thumb):        
    # Extract image
    doc = fitz.open(filename)  # open document
    pix = doc.get_page_pixmap(0, alpha=False)  # render page to an image

    # Resize image
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    im = im.crop((72,72,im.width-72,im.height-72))  # left, upper, right, and lower 
    im.thumbnail((128, 128))

    if not thumb.parent.exists():
        thumb.parent.mkdir(parents=True, exist_ok = True)

    im.save(str(thumb))

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
