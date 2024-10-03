"""
A different config version is never compatible with another config version.
"""

import json
import os
import tomllib
from logging import log
from pathlib import Path

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

        with open(os.path.join(data_path, "version.json"), "w") as f:
            base = {"file_organizer": current_version, "config": CONFIG_VERSION}
            f.write(json.dumps(base))
    else:
        check_config_version(logger)


PACKAGE_VERSION = get_package_version()
USER_DIR = Path.home()
DATA_PATH: str = os.path.join(USER_DIR, ".heavys_file_organizer")

config_logger = loguru.logger
config_logger.add("organize.log")
