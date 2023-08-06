"""Contains helper functions for config instances and the cache for the instances."""
from typing import Any, Generator, List, Type

from autoconfiguration.exceptions.config_class_errors import ConfigNotInitializedError


class Constants:
    """Used to save the instances of config classes."""

    config_instances: List[Any] = []


def reset() -> None:
    """Removes all cached instances."""
    Constants.config_instances = []


def append(instance: Any) -> None:
    """
    Adds a new instance to the cache.

    :param instance: The instance that should be added to the cache.
    """
    Constants.config_instances.append(instance)


def get_by(config_class: Type[Any]) -> Any:
    """
    Returns the cached config instance of the passed config class.

    :param config_class: The class of the instance that should be returned
    :return: The cached instance of the passed class or `None` if no instance could be
        found
    """
    return next(_find_instance(config_class), None)


def has_any() -> bool:
    """
    Checks if any instances are currently cached.

    :return: True if any instances are currently cached, False otherwise
    """
    return len(Constants.config_instances) > 0


def has(config_class: Type[Any]) -> bool:
    """
    Checks if an instance for the passed class currently is cached.

    :param config_class: The config class of an instance
    :return: True if an instance for the passed class currently is cached, False
        otherwise
    """
    return any(_find_instance(config_class))


def get_first() -> Any:
    """
    Returns the first cached instance if any instances are currently cached.

    :raises ConfigNotInitializedError: If no instances are currently cached
    :return: The first cached instance
    """
    if not has_any():
        raise ConfigNotInitializedError()
    return Constants.config_instances[0]


def _find_instance(config_class: Type[Any]) -> Generator[Any, None, None]:
    """
    Searches for a cached instance of the passed config class.

    :param config_class: The config class of an instance
    :return: A generator that searches for a cached instance of the passed class
    :yield: An instance of the passed class
    """
    return (
        instance
        for instance in Constants.config_instances
        if isinstance(instance, config_class)
    )
