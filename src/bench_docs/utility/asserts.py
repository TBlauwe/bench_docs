import os


def assert_file_exists(file_path: str, additional_message: str = ""):
    assert os.path.isfile(file_path), f"File \"{file_path}\" does not exist. {additional_message}"


def assert_directory_exists(dir_path: str, additional_message: str = ""):
    assert os.path.isdir(dir_path), (f"Directory \"{dir_path}\" does not exist. Please provide a valid file path. "
                                     f"{additional_message}")
