DEFAULT_DIR = '.config/video_file_organizer/'

CONFIG_FILE_TEMPLATE = """
# This is the main config file for video_file_organizer

# The directory it will search for the videos to sort
# *REQUIRED
# Example
# input_dir: "path/to/input/dir"
input_dir:

# List of directories it will copy the series to
# *REQUIRED
# Example
# output_dirs:
#   - path/to/dir/1
series_dirs:

# List of files and folders to ignore from input_dir
# Example
# ignore:
#   - ".stversions"
ignore:

# Advanced Options

# list of scripts to run before starting.
# Especially useful if your folders are located on a network drive that you
# need to mount first
# Example
# before_scripts:
#   - "path/to/script"
before_scripts:


# list of scripts to run on_transfer.
# Example
# on_transfer:
#   - "path/to/script"
on_transfer:
"""

RULEBOOK_FILE_TEMPLATE = """
# series
# ---Pick 1 Only---
# season                     --> sets the transfer_to to the correct season
#                                folder
# parent-dir                 --> sets the transfer_to to the parent directory
# sub-dir "<subdir_name>"    --> sets the transfer_to to "<subdir_name>" in
#                                parent directory
# ------------------
# episode-only               --> Change season 1 episode 23 to episode 123
# format-title "<new_title>" --> Jinja formatting, variables are: episode,
#                                season, title, ...
#                                example: "One_Piece_{{ episode }}"
# alt-title                  --> Use the alternative title to search for file
#                                video

[series]
"""
