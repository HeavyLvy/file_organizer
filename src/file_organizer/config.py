"""
A different config version is never compatible with another config version.
"""

import json
import os
import tomllib
from logging import log
from pathlib import Path

import jsonschema.exceptions

from . import common
import shutil

import loguru
import pkg_resources

CONFIG_VERSION = 0


def upgrade_config(logger):
    """
    Upgrades config by going through each version above it one by one
    changing it to its format till it reaches the most recent version.
    """
    logger.warn("Not yet implemented (No other config versions)")


def check_config_version(logger):
    logger.info("Checking config version")
    with open(os.path.join(DATA_PATH, "version.json"), "r") as f:
        versions = json.load(f)
        found_config_version = versions["config"]
    if found_config_version != CONFIG_VERSION:
        logger.info("Updating config version")
        with open(os.path.join(DATA_PATH, "configs.json"), "w") as f:
            versions["config"] = CONFIG_VERSION
            upgrade_config(logger)
            logger.info(
                f"Upgrading config version from {found_config_version} to {CONFIG_VERSION}"
            )


def get_package_version():
    try:
        # If the package is installed
        return pkg_resources.get_distribution("file_organizer").version
    except pkg_resources.DistributionNotFound:
        # If the package is in development
        with open("pyproject.toml", "r") as f:
            toml = tomllib.loads(f.read())
            return toml["project"]["version"]


def create_config_dirs(current_version, data_path, logger):
    if not os.path.exists(data_path):
        logger.info(f"Created '{data_path}'")
        os.mkdir(data_path)
        os.mkdir(os.path.join(data_path, "configs"))

        with open(os.path.join(data_path, "current_config.json"), 'w') as f:
            f.write('{}')

        with open(os.path.join(data_path, "version.json"), "w") as f:
            base = {"file_organizer": current_version, "config": CONFIG_VERSION}
            f.write(json.dumps(base))
    else:
        check_config_version(logger)


def save_config(config_file_path: str, config_name: str) -> None:
    """
    Reads the config and saves it into a 'configs' dir
    and gives it the name as '{config_name}.json'

    :param config_file_path: The path to read the config from.
    :param config_name: The name of the config to be saved.
    :return None:
    """
    # Open the config
    with open(config_file_path, 'r') as f:
        configuration = json.load(f)

    # Validate the config
    common.validate_config(configuration)

    if os.path.exists(os.path.join(CONFIGS_DIR, config_name)):
        raise FileExistsError(f"'{config_name}' already exists.")
    shutil.copy(config_file_path, os.path.join(CONFIGS_DIR, config_name))


def load_config(config_name: str) -> dict:
    """
    Loads the config called 'config_name' from the 'configs' dir

    :param config_name: The name of the config to be loaded.
    :return dict: The configuration
    """

    try:
        with open(os.path.join(CONFIGS_DIR, config_name), 'r') as f:
            configuration = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find configuration: '{config_name}'")

    with open(os.path.join(DATA_PATH, 'current_config.json'), 'w') as f:
        f.write(json.dumps(configuration))


PACKAGE_VERSION = get_package_version()
USER_DIR = Path.home()
DATA_PATH: str = os.path.join(USER_DIR, ".heavys_file_organizer")
CONFIGS_DIR = os.path.join(DATA_PATH, "configs")

config_logger = loguru.logger
config_logger.add("organize.log")
