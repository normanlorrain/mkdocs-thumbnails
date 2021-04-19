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


# Regex: look for "thumbnail" in attribute of a link
regex=re.compile(r'<a.*?href=\"(.*?)\".*?id=\"THUMBNAIL\">(.*?)<\/a>')
# Substitution:  
sub = r'<a href="\1"><img src="\1-thumb.png" class="thumbnail" />\2</a>'


# Style for this class goes into CSS.  e.g. style="margin-top:5px;margin-bottom:5px;margin-right:25px"




class ThumbnailMaker(BasePlugin):

    def on_page_content(self, html, **kwargs):
        srcDir = Path(kwargs['page'].file.abs_src_path).parent
        tgtDir = Path(kwargs['page'].file.abs_dest_path).parent

        targets = regex.findall(html)
        for link, title in targets:
            thumbnail.create(srcDir/Path(link), tgtDir/Path(link+"-thumb.png"))
        html = regex.sub(sub, html)
        return html

