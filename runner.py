#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main script that executes the dropsave program.
"""
import logging
import config
import dropbox
import destination_factory 
import dropbox_helper

# Set up logging.
logging.basicConfig(filename=config.LOGFILE, level=logging.INFO)


def main(dbx):
    """Main function to run the program. Requires an auth'd dropbox client."""
    # Retrieve contents of the source directory.
    source_files = dropbox_helper.get_directory_contents(config.SOURCE_DIR, dbx)
    logging.info(f"Retrieved {len(source_files)} files.")

    # Ensure all the destination directories exist - create them if they do not.
    for dest_dir in config.CATEGORY_TO_PATH_MAP.values():
        if not dropbox_helper.dropbox_path_exists(dest_dir, dbx):
            logging.info(f"The directory \"{dest_dir}\" does not exist.")
            dropbox_helper.create_directory_at_path(dest_dir, dbx)
    
    # Generate a mapping of each source file to its proper destination path.
    source_to_dest_map = destination_factory.DestinationFactory(
        source_files, config.CATEGORY_TO_PATH_MAP).generate_destination_paths()

    # Move files to their specified destinations using the map created above.
    moved_files = []
    for source, dest in source_to_dest_map.items():
        moved_files.append((dropbox_helper.move_dropbox_file(source, dest, dbx), source, dest))

    # Log final file names.
    logging.info(f"Execution complete. The following {len(moved_files)} files were moved:")
    for f in moved_files:
        logging.info(f"\tMoved {f[0]} from \"{f[1]}\" to \"{f[2]}\"")


if __name__ == "__main__":
    # Create the dropbox client and pass it to main.
    with dropbox.Dropbox(oauth2_access_token=config.TOKEN) as dbx:
        main(dbx)
