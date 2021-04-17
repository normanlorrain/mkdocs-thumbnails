import os
import sys
from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

class ThumbnailMaker(BasePlugin):

    def on_page_markdown(self, markdown, **kwargs):
        return markdown

