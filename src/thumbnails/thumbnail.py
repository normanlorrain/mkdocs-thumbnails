import glob
import shutil
import tempfile
from pathlib import Path
import os
import requests_cache
import sys
import json
import fitz
from PIL import Image
from jinja2 import Environment, FileSystemLoader, select_autoescape
from requests.exceptions import *
_session = requests_cache.CachedSession()


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
    # Create directory paths if necessary
    if not outputThumbFile.parent.exists():
        outputThumbFile.parent.mkdir(parents=True, exist_ok = True)

    # Save image 
    with open(outputThumbFile,'wb') as outfile:
         # Get image from YouTube
        url = f'https://img.youtube.com/vi/{id}/default.jpg'
        response = _session.get(url)
        response.raise_for_status()
        imageBytes = response.content
        outfile.write(imageBytes)
        
    
# Playlists are a little harder; need to get the thumbnail via the oembed api
def createYouTubePlaylistThumb(playlistUrl, outputThumbFile):
    # Create directory paths if necessary
    if not outputThumbFile.parent.exists():
        outputThumbFile.parent.mkdir(parents=True, exist_ok = True)

    # Save image 
    with open(outputThumbFile,'wb') as outfile:
        # Get URL of thumbnail from playlist url 
        response = _session.get(f'https://youtube.com/oembed?url={playlistUrl}&format=json')
        response.raise_for_status()
        playlistData = response.json()
        
        # Get thumbnail 
        response = _session.get(playlistData['thumbnail_url'])
        response.raise_for_status()

        outfile.write(response.content)
    



