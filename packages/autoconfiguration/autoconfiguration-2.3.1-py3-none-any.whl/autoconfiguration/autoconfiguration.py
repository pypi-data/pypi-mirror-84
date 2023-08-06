"""
Contains the initialization for the autoconfiguration package. It searches for the
config files and initializes the instance of a config class.
"""
import dataclasses
import logging
import os
from typing import Optional, Tuple, Type, Any

from autoconfiguration.create_config import create_config_instance
from autoconfiguration.exceptions.config_class_errors import (
    ConfigNotInitializedError,
    ConfigClassIsNotDataclassError,
)
from autoconfiguration.exceptions.config_dir_errors import ConfigDirNotFoundError
from autoconfiguration.exceptions.config_file_errors import NoConfigFilesFoundError
from autoconfiguration.helpers import instances

LOG = logging.getLogger(__name__)

CONFIG_EXTENSION = ".ini"
CONFIG_PREFIX = "config-"
GLOBAL_CONFIG = f"config{CONFIG_EXTENSION}"


def init(*args: str, config_class: Type[Any], config_dir: str = "config") -> Any:
    """
    Initializes the passed config class with the values of the *.ini files.

    Searches for the passed configuration files (args) automatically inside
    config_dir. The global config (config.ini) is always loaded by default. The order
    of the passed files matters because the files can depend on each other. Files at
    a higher indices in the list can depend on files with lower indices. Values are
    overwritten by files at a higher index.

    :param args: Environments that should be loaded. They should be inside config_dir.
    :param config_class: The class that should be initialized with the values of the
        *.ini files. This class and the types of its attributes have to be dataclasses.
    :param config_dir: Should be a path that is reachable from the directory where the
        application was executed. Default: config
    :returns: The initialized config class instance containing the values of the
        config files
    """
    if instances.has(config_class):
        LOG.debug("Config was already initialized. Returning existing instance.")
        return instances.get_by(config_class)

    if not dataclasses.is_dataclass(config_class) or not all(
        dataclasses.is_dataclass(field.type)
        for field in dataclasses.fields(config_class)
    ):
        raise ConfigClassIsNotDataclassError()

    if not os.path.exists(config_dir):
        raise ConfigDirNotFoundError(config_dir)
    if not os.path.exists(os.path.join(config_dir, GLOBAL_CONFIG)):
        raise NoConfigFilesFoundError()

    config_files = _validate_config_files(*args, config_dir=config_dir)
    LOG.info("The following config files were found: %s", config_files)

    instance = create_config_instance(config_class, config_files)
    return instance


def get(config_class: Optional[Type[Any]] = None) -> Any:
    """
    Returns the initialized instance of the passed config class.
    The first instance is always returned if no class was passed to this function!

    :param config_class: The class that was passed to `init` and initialized with the
        values of the *.ini files.
    :returns: The initialized instance of the config class
    :raises ConfigNotInitializedError: If the config class was not initialized
    """
    if config_class and not instances.has(config_class):
        raise ConfigNotInitializedError()

    if config_class:
        return instances.get_by(config_class)
    return instances.get_first()


def _validate_config_files(*args: str, config_dir: str) -> Tuple[str, ...]:
    """
    Checks if all passed config files exist in the passed config dir and returns a
    tuple containing the paths of the config files.

    :param args: The config files
    :param config_dir: The config dir
    :return: A tuple containing the paths of the config files
    """
    if not args:
        return (os.path.join(config_dir, GLOBAL_CONFIG),)

    not_existing_config_files = [
        config_file
        for config_file in args
        if not os.path.exists(
            os.path.join(config_dir, _get_correct_config_filename(config_file))
        )
    ]

    if len(not_existing_config_files) > 0:
        LOG.warning(
            "The following config files could not be found: %s",
            not_existing_config_files,
        )

    return (
        os.path.join(config_dir, GLOBAL_CONFIG),
        *(
            os.path.join(config_dir, _get_correct_config_filename(config_file))
            for config_file in args
            if config_file not in not_existing_config_files
        ),
    )


def _get_correct_config_filename(filename: str) -> str:
    """
    Returns the full filename of the config file. The full filename begins with
    'config-' and ends with '.ini'.

    :param filename: Part of a config filename
    :return: The full config filename
    """
    return (
        ("" if filename.startswith(CONFIG_PREFIX) else CONFIG_PREFIX)
        + filename
        + ("" if filename.endswith(CONFIG_EXTENSION) else CONFIG_EXTENSION)
    )


def reset() -> None:
    """
    Removes all cached instances of config classes. This should only be used in test
    setups because it should not be necessary to reinitialize instances.
    """
    instances.reset()
