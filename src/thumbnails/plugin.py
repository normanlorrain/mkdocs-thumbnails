import sys
import urllib
import re
import itertools
import logging
from pathlib import Path
import urllib
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from bs4 import BeautifulSoup

from . import thumbnail


# Goal: have a means in our markdown to indicate the desire for PDF links 
# to have a thumbnail, automatically generated.
#
# Method: use a special attribute (supported by Python's Attribute Lists) 
# https://python-markdown.github.io/extensions/attr_list/
# 
# eg 
#    [foo](bar.pdf){.pdf}   (Markdown)
# becomes
#    <a href="bar.pdf" class="pdf">foo</a>   (HTML)
# in the on_page_content() below, we can search the HTML for this pattern and 
# modify the HTML before it's written to disk, AND, generate the required thumbnail
# eg:
#    <a href="bar.pdf" class="pdf">foo</a>
# becomes
#    <a href="bar.pdf"><img src="bar.pdf-thumb.png" />foo</a> 

log = logging.getLogger('mkdocs')

class ThumbnailMaker(BasePlugin):
    # style is added to the image tag.  e.g. margin-right:10px; 
    config_scheme = ( ('style', config_options.Type(str, default="")), )

    def on_pre_build(self, **kwargs):
        self.pdf_count = 0
        self.yt_count = 0

    # This is done for each page.  The markdown conversion has been done at this point.
    # Modify the HTML to have the thumbnail when the relevant attribute is found
    def on_page_content(self, html, **kwargs):
        sys.stdout.write('.')
        sys.stdout.flush()                # flush stdout buffer (actual character display)
    
        pageFile = kwargs['page'].file
        srcDir = Path(pageFile.abs_src_path).parent
        tgtDir = Path(pageFile.abs_dest_path).parent

        soup = BeautifulSoup(html, "html.parser")


        # PDF links
        links = soup.find_all("a", class_="pdf")
        self.pdf_count+=len(links)
        for link in links:
            href = link.get('href')
            filename = urllib.parse.unquote(href)     # removes %20's typically
            if not (srcDir/Path(filename)).exists():
                continue # Skip this file; mkdocs detects these already, so no need to log again.
            thumbnail.createPdfThumb(srcDir/Path(filename), tgtDir/Path(filename+"-thumb.png"))
            img = soup.new_tag('img')
            img['src'] = f"{href}-thumb.png"
            img['style'] = self.config["style"]
            img['class'] = "pdf"
            del link['class']  
            link.contents.insert(0,img)

        # YouTube links
        # See https://webapps.stackexchange.com/questions/54443/format-for-id-of-youtube-video
        #
        links = soup.find_all("a", class_="youtube")
        self.yt_count+=len(links)
        for link in links:
            href = link.get('href')
            try:
                if 'playlist' in href:
                    id = re.search( r'.*playlist\?list=([0-9A-Za-z_-]+).*', href).group(1)
                    thumbnail.createYouTubePlaylistThumb(href,tgtDir/Path(id+"-thumb.png"))
                else:
                    id = re.search( r'.*youtu.be\/([0-9A-Za-z_-]+).*', href).group(1)
                    thumbnail.createYouTubeThumb(id, tgtDir/Path(id+"-thumb.png"))
            except thumbnail.HTTPError as e:
                    log.warn(f'Bad Youtube link: {href} in {pageFile.abs_src_path} ')
                    continue
            img = soup.new_tag('img')
            img['src'] = f"{id}-thumb.png"
            img['style'] = self.config["style"]
            img['class'] = "youtube"
            del link['class']
            link.contents.insert(0,img)

        return str(soup)

    def on_post_build(self, **kwargs):
        sys.stdout.write('\b')            # erase the last written char
        sys.stdout.flush()                # flush stdout buffer (actual character display)

        log.info(f"YouTube count: {self.yt_count}")
        log.info(f"PDF count: { self.pdf_count}")

