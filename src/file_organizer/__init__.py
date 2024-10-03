"""
Organize your files into folders on Windows, Linux and Mac.
Create a JSON configuration and run the command
`fo add configuration.json name_of_the_config`
`fo use name_of_the_config`
`fo organize`
"""

from . import organizer
from . import config as __config

import loguru

CONFIG_VERSION = 0

logger = loguru.logger

# Create config dir and config file
__config.create_config_dirs(__config.CONFIG_VERSION, __config.DATA_PATH, logger)
