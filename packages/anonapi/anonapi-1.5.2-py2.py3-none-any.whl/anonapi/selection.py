"""Functions to filter and select files from folders.
Useful for example for selecting only DICOM files in a folder.
"""
import logging
import re
from fnmatch import fnmatch
from pathlib import Path

import pydicom

from tqdm import tqdm

from fileselection.fileselection import FileSelectionFile, FileSelectionFolder
from pydicom.errors import InvalidDicomError

logger = logging.getLogger(__name__)


class FileFolder:
    """A folder that might contain some files. Makes it easy to iterate
    over these files in different ways
    """

    def __init__(self, path):
        self.path = Path(path)

    def iterate(
        self, pattern="*", recurse=True, exclude_patterns=None, ignore_dotfiles=True
    ):
        """Iterator that yields subpaths. Makes it easy to use progress bar

        Parameters
        ----------
        pattern: str, optional
            Glob file pattern. Default is '*' (match all)
        recurse: bool, optional
            Search for paths in all underlying directories. Default is True
        exclude_patterns: List[str], optional
            Exclude any root_path that matches_header any of these patterns.
            Patterns are unix-style: * as wildcard. See fnmatch function.
            Defaults to emtpy list meaning no exclusions
        ignore_dotfiles: bool, optional
            Ignore any filename starting with '.'

        Returns
        -------
        generator
            Yields Path if the root_path is a file, None otherwise

        """
        if not exclude_patterns:
            exclude_patterns = []

        if recurse:
            glob_pattern = f"**/{pattern}"
        else:
            glob_pattern = f"{pattern}"

        all_paths_iter = self.path.glob(glob_pattern)
        for x in all_paths_iter:
            # sleep(0.2)
            exclude = any(
                [fnmatch(x.relative_to(self.path), y) for y in exclude_patterns]
            )
            ignore = x.name.startswith(".") and ignore_dotfiles
            if x.is_file() and not exclude and not ignore:
                yield x
            else:
                continue


def open_as_dicom(path, read_pixel_data: bool = True):
    """Tries to open root_path as dicom

    Parameters
    ----------
    path: Pathlike
        Path a to a file
    read_pixel_data: Bool, optional
        Whether to read pixel data when opening this file.
        Defaults to True, meaning all pixel data will be read and returned

    Returns
    -------
    pydicom.dataset
        If root_path can be opened as dicom
    None
        If root_path cannot be opened
    """
    try:
        return pydicom.filereader.dcmread(
            str(path), stop_before_pixels=not read_pixel_data
        )
    except InvalidDicomError:
        return None


def create_dicom_selection(path, check_dicom=True) -> FileSelectionFile:
    """Find all DICOM files path (recursive) and save them as a FileSelectionFile.

    Parameters
    ----------
    path: PathLike
        Search for DICOM files in the path, recursively
    check_dicom: bool, optional
        If True, open each file to see whether it is valid DICOM (thorough).
        If False, will only select based on filename (fast). Defaults to True

    Returns
    -------
    FileSelectionFile
        The created file selection that has been saved to disk
    """
    # Find all dicom files in this folder
    folder = FileFolder(path)
    logger.info(f"Finding all files in {path}")
    files = [x for x in tqdm(folder.iterate()) if x is not None]
    if check_dicom:
        logger.info(f"Found {len(files)} files. Finding out which ones are DICOM")
        dicom_files = [
            x for x in tqdm(files) if open_as_dicom(x, read_pixel_data=False)
        ]
    else:
        logger.info(f"Found {len(files)} files. Adding all that look like DICOM")
        dicom_files = [x for x in files if looks_like_dicom_file(x)]

    logger.info(f"Found {len(dicom_files)} DICOM files")
    # record dicom files as fileselection
    selection_folder = FileSelectionFolder(path=path.absolute())
    selection = FileSelectionFile(
        data_file_path=selection_folder.get_data_file_path(),
        description=Path(path).name + " auto-generated by anonapi",
        selected_paths=[x.relative_to(folder.path) for x in dicom_files],
    )
    selection_folder.save_file_selection(selection)
    return selection


def looks_like_dicom_file(path) -> bool:
    """Does this file path look like a DICOM file?

    For doing a first quick selection of which files to include for deidentification
    """

    if Path(path).suffix.lower() in (".dicom", ".dcm"):
        return True
    elif re.match(r"^(\.[0-9]*)*$", Path(path).suffix):
        # there are only numbers in the extension. This might be a DICOM file
        return True
    else:
        return False
