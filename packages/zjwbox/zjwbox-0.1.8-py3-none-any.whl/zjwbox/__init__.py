from __future__ import absolute_import
from .zjwbox import *
from .auto_req import *
from .comm_req import *
import os
from pyppeteer import chromium_downloader


name = "zjwbox"
version = "0.1.8"


pyppeteer_version_win32 = chromium_downloader.downloadURLs.get("win32")
pyppeteer_version_win64 = chromium_downloader.downloadURLs.get("win64")


