import os
import sys
from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File

import re
from pathlib import Path
import urllib

from . import thumbnail

# Goal: have a means in our markdown to indicate the desire for PDF links 
# to have a thumbnail, automatically generated.
#
# Method: use a special attribute (supported by Python's Attribute Lists) 
# https://python-markdown.github.io/extensions/attr_list/
# 
# eg [foo](bar.pdf){#THUMBNAIL}   (Markdown)
#    becomes
#    <a href="bar.pdf" id="THUMBNAIL">foo</a>   (HTML)
# in the on_page_content() below, we can search the HTML for this pattern and 
# modify the HTML before it's written to disk, AND, generate the required thumbnail
# eg:
#  <a href="bar.pdf" id="THUMBNAIL">foo</a>
# becomes
# <a href="bar.pdf"><img src="bar.pdf-thumb.png" />foo</a> 





class ThumbnailMaker(BasePlugin):

    # style is added to the image tag.  e.g. margin-right:10px; 
    config_scheme = ( ('style', config_options.Type(str, default="")), )

    # build our regex for future on_page events
    # At this point the user configuration is loaded and validated
    def on_config( self, config, **kwargs):
        # Regex: look for "thumbnail" in attribute of a link
        self.regexPDF=re.compile(r'<a.*?class=\"pdf\".*?href=\"(.*?)\".*?>(.*?)<\/a>')
        # Substitution:  
        self.subPDF = r'<a href="\1"><img src="\1-thumb.png" class="pdf" style="{}" />\2</a>'.format(self.config['style'])

        self.regexYT = re.compile(r'<a.*?class=\"youtube\".*?href=\"(.*?\/(\w+))\".*?>(.*?)<\/a>')
        self.subYT = r'<a href="\1"><img src="\2-thumb.png" class="youtube" style="{}" />\3</a>'.format(self.config['style'])
        # Style for this class goes into CSS.  e.g. style="margin-top:5px;margin-bottom:5px;margin-right:25px"

        return config

    # This is done for each page.  The markdown conversion has been done at this point.
    # Modify the HTML to have the thumbnail when the relevant attribute is found
    def on_page_content(self, html, **kwargs):


        srcDir = Path(kwargs['page'].file.abs_src_path).parent
        tgtDir = Path(kwargs['page'].file.abs_dest_path).parent

        targets = self.regexPDF.findall(html)
        for link, title in targets:
            filename = urllib.parse.unquote(link)
            thumbnail.createPdfThumb(srcDir/Path(filename), tgtDir/Path(filename+"-thumb.png"))
        html = self.regexPDF.sub(self.subPDF, html)

        targets = self.regexYT.findall(html)
        for link, id, title in targets:
            thumbnail.createYouTubeThumb(id, tgtDir/Path(id+"-thumb.png"))
        html = self.regexYT.sub(self.subYT, html)


        return html

