import os

def convert_dir_to_os_format(dir_path: str) -> str:
    """
    Converts the input directory path to the correct OS-specific format.
    :param dir_path: The input directory path.
    :return: The converted directory path.
    """

    # Normalize the path to handle forward and backward slashes consistently
    normalized_path = os.path.normpath(dir_path)

    return normalized_path
