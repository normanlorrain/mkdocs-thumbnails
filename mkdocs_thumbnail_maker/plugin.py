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

# Goal: have an "extension" to markdown to precede a link to PDF with a thumbnail image of the PDF.
# Method: wrap any link that needs a thumbnail with "*".  This will show up as italic without this (backward compatible)
# when extension is enabled, this regex will catch it, allowing for a proper substitition
# 
#

# Regex: \*\[(.*?)\]\((.*?)\)\*
# Substitution: ![thumbnail:\1](\1-thumb.jpg)  [\1](\2)  
# 
# eg:
#  *[foo](bar.pdf)*
# becomes
# ![thumbnail:foo](bar-thumb.png)  [foo](bar.pdf)  
# 
# now the downstream markdown conversion will do what we want




exp = re.compile(r'\*\[(.*?)\]\((.*?)\)\*')


class ThumbnailMaker(BasePlugin):

    def on_page_markdown(self, markdown, **kwargs):
        srcDir = Path(kwargs['page'].file.abs_src_path).parent
        tgtDir = Path(kwargs['page'].file.abs_dest_path).parent

        targets = exp.findall(markdown)
        for title, link in targets:
            thumbnail.create(srcDir/Path(link), tgtDir/Path(link+"-thumb.png"))
        markdown2 = exp.sub( r'![thumbnail:\1](\2-thumb.png)  [\1](\2)', markdown)
        return markdown2

