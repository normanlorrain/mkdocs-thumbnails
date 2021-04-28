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


def createPdfThumb(inputPDFfile,outputThumbFile):        
    # Extract image
    doc = fitz.open(inputPDFfile)  # open document
    pix = doc.get_page_pixmap(0, alpha=False)  # render page to an image

    # Resize image
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    im = im.crop((72,72,im.width-72,im.height-72))  # left, upper, right, and lower 
    im.thumbnail((128, 128))

    # Create directory paths if necessary
    if not outputThumbFile.parent.exists():
        outputThumbFile.parent.mkdir(parents=True, exist_ok = True)

    # Save image to file
    im.save(str(outputThumbFile))

def createYouTubeThumb(id, outputThumbFile):
    # Get image from YouTube
    url = f'https://img.youtube.com/vi/{id}/default.jpg'
    thumbdata = urllib.request.urlopen(url)

    # Create directory paths if necessary
    if not outputThumbFile.parent.exists():
        outputThumbFile.parent.mkdir(parents=True, exist_ok = True)

    # Save image 
    with open(outputThumbFile,'wb') as outfile:
        outfile.write(thumbdata.read())
    



