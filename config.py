# -*- coding: utf-8 -*-
"""
Config file for the program. All constants should be stored here.
"""
import os
import datetime

# Retrieves the dropbox API oauth 2 access token saved as an environment variable.
TOKEN = os.environ.get("TOKEN")

# Sets the log file to the path provided or defaults to the tmp folder.
LOGFILE = os.environ.get("LOGFILE", "/tmp/dropsavelog")

# Constant to store the source directory. Must contain a leading "/" and no trailing "/".
SOURCE_DIR = "/dropsave"

# Constant to store the destination directory. Must contain a leading and trailing "/".
DEST_DIR = "/documents/"

# Set the base path dynamically using the current year.
BASE_DEST_PATH = f"{DEST_DIR}{datetime.datetime.now().year}"

# Category constants - used to define the overall types of files that will be dropsaved.
# These will also be the keywords we look for in the file names of the source files.
# Must be lowercase.
RECEIPTS = "receipts"
VIDEOS = "videos"

# Path associations - used to map categories to destination paths.
CATEGORY_TO_PATH_MAP = {
    RECEIPTS: f"{BASE_DEST_PATH} Receipts",
    VIDEOS: f"{BASE_DEST_PATH} Videos",
}
