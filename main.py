"""
main.py
"""

import json
import os
import shutil

import jsonschema
import loguru


def convert_dir_to_os_format(dir_path: str) -> str:
    """
    Converts the input directory path to the correct OS-specific format.
    :param dir_path: The input directory path.
    :return: The converted directory path.
    """

    # Normalize the path to handle forward and backward slashes consistently
    normalized_path = os.path.normpath(dir_path)

    return normalized_path


def organize(
    file_types: list[str], directories: list[str], folder: str, logger
) -> None:
    """
    Organizes files in a directory by file type and moves it into a folder.
    :param file_types: A list of strings containing the file extension to be moved.
    :param directories: Directories to be searched
    :param folder: Where to put the organized files.
    :param logger: The logger to be used.
    :return: None
    """

    # region Convert folder path and directory paths to OS-specific format
    folder = convert_dir_to_os_format(folder)
    directories = list(map(convert_dir_to_os_format, directories))
    # endregion

    if folder in directories:
        logger.error(
            f'Folder: "{folder}" was included in the directories to be searched'
        )
        return

    # region Check if the folders exist.
    folder_exists = os.path.exists(folder)
    if not folder_exists:
        logger.error(f'Folder: "{folder}" doesnt exist!')
        return
    for directory in directories:
        if not os.path.exists(directory):
            logger.error(f'Directory: "{directory}" doesnt exist!')
            return
    # endregion

    for directory in directories:
        for entry in os.listdir(directory):
            full_path: str = os.path.join(directory, entry)
            _, file_extension = os.path.splitext(full_path)

            in_supported_file_types = file_extension.lower() in file_types
            is_a_file = os.path.isfile(full_path)

            if is_a_file and in_supported_file_types:
                try:
                    shutil.move(full_path, folder)
                    logger.info(f'File: "{full_path}" has been moved to "{folder}"')
                except shutil.Error as e:
                    logger.error(
                        f'Failed to move "{full_path}" to "{folder}", reason:\n{e}'
                    )


def main(logger) -> None:
    """
    Main function to be run.
    :param logger: A logger to be used, designed to work with the logging module.
    :return: None
    """

    configuration_path = "my_configuration.json"

    logger.info("Organizing files!")

    # region Load configuration.
    try:
        with open(configuration_path, "r") as f:
            configuration: dict = json.load(f)
    except json.decoder.JSONDecodeError as e:
        logger.error(f"Failed to load json configuration because: {e}")
        return
    with open("configuration_schema.json", "r") as f:
        schema = json.load(f)
    try:
        jsonschema.validate(configuration, schema)
    except jsonschema.exceptions.ValidationError as e:  # type: ignore # | False Positive | "exceptions" is not a known attribute of module "jsonschema" - pyright
        logger.error(f"json configuration failed schema validation because: {e}")
        return
    # endregion

    for title, data in configuration.items():
        logger.info(f"Organizing {title}")
        organize(data["types"], data["directories"], data["folder"], logger=logger)


if __name__ == "__main__":
    my_logger = loguru.logger
    my_logger.add("organize.log")

    try:
        main(my_logger)
    except Exception as e:
        my_logger.error(f"Program crashed because: {e}")
        my_logger.info(f"GLOBALS: {globals()}")
