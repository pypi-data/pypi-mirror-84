import logging
from os import listdir
from os.path import isfile, join, isdir, dirname
import os
import shutil
from tqdm import tqdm
from typing import Dict, List


class ManageDir:
    """Commonly used directory functions to manage a directory."""

    suffix = "_"

    @staticmethod
    def assert_file_exists(file_path: str) -> None:
        """Assert filepath exists. Give verbose error messages.

        Args:
            file_path (str): file path e.g. abc/xyz.csv or xyz.csv
        """
        dir = dirname(file_path)
        assert dir == "" or isdir(dir), f"{dir} directory doesn't exist.."
        assert isfile(
            file_path
        ), f"{file_path} is invalid. \nContents of {dir} are {[f for f in listdir(dir)]}"

    @staticmethod
    def assert_parent_dir_exists(file_path: str) -> None:
        """Assert parent directory of a file_path exists

        Args:
            file_path (str): file path e.g. abc/xyz.csv or xyz.csv
        """
        dir = dirname(file_path)
        assert dir == "" or isdir(dir), f"{dir} directory doesn't exist.."

    @staticmethod
    def assert_dir_exists(dir_path: str) -> None:
        """Assert directory exists

        Args:
            dir_path (str): dir path e.g. abc/ or abc/xyz/
        """
        dir = dirname(dir_path)
        assert dir == "" or isdir(dir), f"{dir} directory doesn't exist.."
        assert isdir(dir_path), f"{dir_path} directory doesn't exist.."

    @classmethod
    def list_empty_sub_dirs(cls, dir_path: str) -> List[str]:
        """Get empty dirs in given directory path.

        Args:
            dir_path (str): String directory path

        Returns:
            List[str]: List of sub directory path if those dirs are empty
        """

        cls.assert_dir_exists(dir_path)
        return [
            join(dir_path, f)
            for f in listdir(dir_path)
            if isdir(join(dir_path, f)) and not listdir(join(dir_path, f))
        ]

    @classmethod
    def remove_empty_sub_dirs(cls, dir_path: str, verbose: bool = False) -> None:
        """Removes empty directories from provided dir path.

        Args:
            dir_path (str): String directory path
            verbose (bool, optional): print out name of deleted dir. Defaults to False.
        """
        for dir in cls.list_empty_sub_dirs(dir_path):
            os.rmdir(dir)
            if verbose:
                logging.info(f"Deleted {dir}")

    @staticmethod
    def get_filetype(file_path: str) -> str:
        """Get fie type from extension.

        Args:
            file_path (str): filepath

        Returns:
            str: filetype, eg. for `abc.csv` return `csv`
        
        Examples:
            xy.jpg      -> jpg
            .gitignore  -> unk
        """
        _, filetype = os.path.splitext(file_path)

        if not filetype:
            filetype = "unk"

        filetype = filetype.replace(".", "")
        return filetype

    @classmethod
    def get_type_sub_dirs(cls, dir_path: str) -> Dict[str, str]:
        """Get sub dirs which are created by us

        Args:
            dir_path (str): dir to search into

        Returns: 
            Dict[str, str]: filetype to file type sub directory path
        """
        cls.assert_dir_exists(dir_path)

        return {
            f[:-1]: join(dir_path, f)
            for f in listdir(dir_path)
            if isdir(join(dir_path, f)) and str(f).endswith(cls.suffix)
        }

    @classmethod
    def create_type_sub_dirs(cls, dir_path: str) -> Dict[str, str]:
        """Creates type sub folders (if doesn't exist).

        Args:
            dir_path (str): directory path to create into

        Returns:
            Dict[str, str]: filetype to file type sub dirs path
        """

        # check if the directory to arrange exists
        cls.assert_dir_exists(dir_path)

        dir_path = os.path.abspath(dir_path)

        logging.info("Working on {}\n".format(dir_path))

        files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

        # previously created file_type folders
        filetype_folder_dict = cls.get_type_sub_dirs(dir_path)

        # creating directory
        for file in tqdm(files):
            filetype = cls.get_filetype(file)

            if filetype not in filetype_folder_dict:
                new_file_type_folder = join(
                    dir_path, "{}{}".format(filetype, cls.suffix)
                )

                # if folder doesn't exists -> create folder for file type
                if not isdir(new_file_type_folder):
                    os.mkdir(new_file_type_folder)
                    filetype_folder_dict[str(filetype)] = str(new_file_type_folder)

        return filetype_folder_dict

    @classmethod
    def move_files_to_type_sub_dirs(cls, dir_path: str, verbose: bool = False) -> None:
        """Creates type folders in a directory and moves files to respective type folders.

        Args:
            dir_path (str): Directory to work upon
            verbose (bool, optional): If true log INFO. Defaults to False.
        """
        cls.assert_dir_exists(dir_path)
        filetype_folder_dict = cls.create_type_sub_dirs(dir_path)
        dir_path = os.path.abspath(dir_path)
        logging.info("Working on {}\n".format(dir_path))
        files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
        # moving files
        for file in tqdm(files):
            src_path = os.path.join(dir_path, file)
            filetype = cls.get_filetype(file)
            if filetype in filetype_folder_dict.keys():
                dest_folder = filetype_folder_dict[str(filetype)]
                dest_path = os.path.join(dest_folder, file)
                shutil.move(src_path, dest_path)
                if verbose:
                    logging.info(f"{src_path} --to---> {dest_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OCD args")
    parser.add_argument(
        "-D", "--dir", type=str, required=True, nargs=1, help="directory to run on",
    )

    # example args
    # args = parser.parse_args("-D /Users/userx/Downloads".split())

    # args from cli
    args = parser.parse_args()

    path = args.dir[0]
    # print(f"Empty in {path}: {ManageDir.list_empty_sub_dirs(path)}")
    # ManageDir.remove_empty_sub_dirs(path)
    ManageDir.move_files_to_type_sub_dirs(path)
