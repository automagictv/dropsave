# -*- coding: utf-8 -*-
"""
Helpers to deal with dropbox actions.
"""
import dropbox
import config
import re
import logging


def dropbox_path_exists(path, dbx):
    """Checks if a given dropbox path exists.

    Args:
        path: string representation of the objects path.
        dbx: A dropbox api connection object.
    
    Returns True if the path exists else False.
    """
    try:
        return dbx.files_get_metadata(path) is not None
    except dropbox.exceptions.ApiError as e:
        error_object = e.error
        if isinstance(error_object, dropbox.files.GetMetadataError) and error_object.is_path():
            base_error = error_object.get_path()
            if isinstance(base_error, dropbox.files.LookupError) and base_error.is_not_found():
                return False
            else:
                raise base_error
        else:
            raise error_object


def create_directory_at_path(path, dbx):
    """Creates a directory at the path. Expects that this does not point to a file.

    Args:
        path: string representation of the objects path with a leading "/".
        dbx: A dropbox api connection object.
    """
    # Check that the path does not end with a file extension.
    if re.search(r"\.[^.]*$", path) is not None:
        raise ValueError("The path needs to be a directory path and not a file path. "
                         "{path} appears to be a file path.")
    # Create folder and disregard the dropbox.files.FolderMetadata object that's returned.
    _ = dbx.files_create_folder(path)
    logging.info(f"Created directory at path: \"{path}\"")


def get_directory_contents(directory, dbx):
    """Calls dropbox to retrieve contents of a directory.

    Args:
        directory: string value representing the dir path.
    
    Returns:
        A list of strings representing the file names in the directory path.
    """
    content_to_return = []
    try:
        folder_contents = dbx.files_list_folder(directory)
    except dropbox.exceptions.ApiError as e:
        error_object = e.error
        if isinstance(error_object, dropbox.files.ListFolderError):
            base_error = error_object.get_path()
            if isinstance(base_error, dropbox.files.LookupError) and base_error.is_not_found():
                raise Exception(f"Dropbox cannot locate the object at path \"{directory}\".")
            else:
                raise base_error
        else:
            raise error_object

    # Get the dropbox objects contained within the folder
    directory_contents = folder_contents.entries
    while folder_contents.has_more:
        cursor = folder_contents.cursor
        folder_contents = dropbox.dropbox.Dropbox.files_list_folder_continue(cursor)
        directory_contents += folder_contents.entries

    # Save contents to file lists
    for fobj in directory_contents:
        if isinstance(fobj, dropbox.files.FileMetadata):
            content_to_return.append(fobj.name)
        else:
            logging.warn(f"The object type for \"{fobj.name}\" is not currently supported. "
                         "The object was not moved to a destination directory.")

    return content_to_return


def move_dropbox_file(source_path, destination_path, dbx):
    """Moves a file from the source path to the destination path.

    Args:
        source_path: String representation of the source file path.
        destination_path: String representation of the target destination path.

    Returns:
        The final file name for use in logging (in the runner.py script).
    """
    dbx.files_move(source_path, destination_path)
    return dbx.files_get_metadata(destination_path).name
