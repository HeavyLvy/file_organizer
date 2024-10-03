import json
import os
import tomllib
import pkg_resources
import jsonschema


def convert_dir_to_os_format(dir_path: str) -> str:
    """
    Converts the input directory path to the correct OS-specific format.
    :param dir_path: The input directory path.
    :return: The converted directory path.
    """

    # Normalize the path to handle forward and backward slashes consistently
    normalized_path = os.path.normpath(dir_path)

    return normalized_path


def get_package_version() -> str:
    """
    Gets the current version of the package.
    if its installed, it will return the installed version
    else its in development mode and it will return the version from `pyproject.toml`
    :return: The current version of the package.
    """
    try:
        # If the package is installed
        return pkg_resources.get_distribution("file_organizer").version
    except pkg_resources.DistributionNotFound:
        # If the package is in development
        with open("pyproject.toml", "r") as f:
            toml = tomllib.loads(f.read())
            return toml["project"]["version"]


def validate_config(configuration: dict):
    configuration_schema_path = os.path.join(
        os.path.dirname(__file__), "configuration_schema.json"
    )

    with open(configuration_schema_path, "r") as f:
        schema = json.load(f)

    jsonschema.validate(configuration, schema)

