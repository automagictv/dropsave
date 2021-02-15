# -*- coding: utf-8 -*-
import datetime
import re
import logging
import config


class DestinationFactory(object):
    """
    Used to parse source file names and generate destination paths using
    the CATEGORY_TO_PATH_MAP passed in from the configuration file.
    """

    def __init__(self, files, category_to_path_map):
        """
        files: A list of file name strings (currently in the source dropbox folder).
        category_to_path_map: A dict that maps string args to string representations of the dest path.
        """
        self.category_to_path_map = category_to_path_map
        self.files = files
        self.source_to_dest_map = {}

        # Make file_date yesterday as cron runs at 12am every night. Format is "YYMMDD".
        self.file_date = (datetime.datetime.today() -
            datetime.timedelta(1)).strftime("%Y%m%d")[2:]

    def _get_destination_path_elements(self, file_name):
        """
        Parses the file path and returns the file extension, the destination
        directory, and the final file name.

        file_name: String of the source file name.
        """
        # Parse original name to determine destination path
        rxp = re.search(r"\.[^.]*$", file_name) # Searches for a file extension
        if rxp:
            ext = rxp.group(0)
            output_file_name = file_name[:file_name.rfind(ext)].split(" ")
        else:
            ext = ""
            output_file_name = file_name.split(" ")

        # Remove the first element of the source file name which will be used
        # as the key in the category_to_path_map
        destination = output_file_name.pop(0).lower()

        # Look up the destination path
        dest_directory_str = self.category_to_path_map.get(destination)
        if dest_directory_str is None:
            raise PathKeyDoesNotExist(destination)

        name = "-".join(output_file_name)
        return dest_directory_str, name, ext

    def generate_destination_paths(self):
        """Generates destination files paths for all source files in self.files.
        
        Destination paths are generated using the format YYMMDD_[file-name].[ext]

        Returns:
            A dictionary mapping full source file paths (str) to full destination file paths (str).
        """
        if not self.source_to_dest_map:
            logging.info("Generating destination paths...")

            # Generate destination paths for all file objects
            for file in self.files:
                try:
                    directory, name, ext = self._get_destination_path_elements(file)
                    full_source_path = f"{config.SOURCE_DIR}/{file}"
                    self.source_to_dest_map[full_source_path] = f"{directory}/{self.file_date}_{name}{ext}"
                except PathKeyDoesNotExist as e:
                    logging.warn(e.error)
                    continue

            logging.info(f"{len(self.files)} paths generated.")

        return self.source_to_dest_map


class PathKeyDoesNotExist(Exception):
    """Exception to handle files that don't match categories from config.CATEGORY_TO_PATH_MAP."""

    def __init__(self, _key=None, error=None):
        if not error:
            error = f"The key, \"{_key}\", for the specified file does not exist. " \
                "define this key and destination in the config file."
        self.error = error
