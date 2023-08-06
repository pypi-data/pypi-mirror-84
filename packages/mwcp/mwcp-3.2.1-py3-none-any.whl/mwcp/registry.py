"""
Interface for registering and accessing parsers.
"""
import imp
from collections import namedtuple
import hashlib
import importlib
import importlib.machinery
import importlib.util
import logging
import os
import pkgutil
from typing import Optional, Tuple

import pkg_resources

from ruamel.yaml import YAML

yaml = YAML()

from mwcp.parser import Parser
from mwcp.dispatcher import Dispatcher

logger = logging.getLogger(__name__)

ParserInfo = namedtuple("ParserInfo", ("name", "source", "author", "description"))


class Source:
    """Represents a source of parsers."""

    def __init__(self, name, path, config, is_pkg):
        self.name = name
        self.path = path
        self.config = config
        self.is_pkg = is_pkg
        self._package = None

    def __getstate__(self):
        # Modifying __getstate__ in order to null out _package, since that is not picklable.
        _dict = self.__dict__
        _dict["_package"] = None
        return _dict

    @property
    def package(self):
        """Imports and returns the Python package for the source."""
        if not self._package:
            # Import source on first call.
            if self.is_pkg:
                try:
                    self._package = importlib.import_module(self.path)
                except ImportError:
                    raise ValueError("Could not import source: {}".format(self.path))
            else:
                self._package = _create_package(self.path)
        return self._package


class ParserNotFoundError(Exception):
    """This exception gets thrown if a parser can't be found."""


# Set of parser sources mapped to configuration files.
# Sources can be a file path or import path to a python package containing parsers.
# Maps source -> Source object
_sources = {}

_default_source = None


def set_default_source(source_name):
    """
    Sets a default parser source to use if not explicitly defined.
    If this is not set, all sources will be considered.

    :param source_name: The name of the source to set.
    """
    global _default_source
    _default_source = source_name


def clear_default_source():
    """
    Clears a previously set default source.
    """
    global _default_source
    _default_source = None


def clear():
    """
    Removes all registered parsers.
    """
    global _sources
    global _default_source
    _sources = {}
    _default_source = None


def register_entry_points():
    """
    Registers parsers found in entry_point: "mwcp.parsers"
    :return:
    """
    for entry in pkg_resources.iter_entry_points("mwcp.parsers"):
        package = entry.load()
        register_parser_package(package, source_name=entry.name)


def _load_config(config_file_path):
    """
    Loads and validates given parser config file path.

    :raises ValueError: If loaded config file is invalid.
    """
    with open(config_file_path, "r") as fp:
        config = yaml.load(fp)

    logger.debug("Validating parser config: {}".format(config_file_path))
    if not isinstance(config, dict):
        raise ValueError("Parser config is not a dictionary: {}".format(config_file_path))
    config = {str(key): value for key, value in config.items()}  # Force keys to be strings.
    for key, value in config.items():
        if "." in key:
            raise ValueError('"." in group name is not allowed: {}'.format(key))
        if "description" not in value:
            raise ValueError('Missing "description" field in group: {}'.format(key))
        if "parsers" not in value:
            raise ValueError('Missing "parsers" field in group: {}'.format(key))
        if not isinstance(value["parsers"], list):
            raise ValueError('"parsers" field is not a list in group: {}'.format(key))
    return config


def register_parser_directory(directory, config_file_path=None, source_name=None):
    """
    Registers parsers found in parser_dir. This function allows you to register one-off parsers
    that are not part of an installed python package.

    :param str directory: An extra directory to look for one-off parsers.
    :param config_file_path: Optional path to a parser configuration file used to define parser groups.
            If not provided, it will attempt to pull from the "config" attribute of the __init__ module.
    :param source_name: Unique name to give to the source. (uses directory path otherwise)

    :raises ValueError: If loaded config file is invalid.
    """
    global _sources

    if not os.path.isdir(directory):
        raise ValueError(u"Parser directory not found or not a directory: {}".format(directory))

    # Ensure this directory can be converted to a package and pull config_file_path if available.
    package = _create_package(directory)
    if not config_file_path:
        config_file_path = getattr(package, "config", None)
    config = _load_config(config_file_path) if config_file_path else {}

    if not source_name:
        source_name = directory

    # NOTE: _sources must be discoverable without modification, so we can't register the package.
    _sources[source_name] = Source(source_name, directory, config, False)


def register_parser_package(package, config_file_path=None, source_name=None):
    """
    Registers Python package containing MWCP parsers.

    :param package: An Python package containing submodules that contain MWCP parsers.
        NOTE: Package must be discoverable in subprocesses without modifying the python path.
              Please use register_parser_directory() instead if that is not possible.
    :param config_file_path: Path to parser configuration file used to define parser groups.
        If not provided, it will attempt to pull from the "config" attribute of the __init__ module.
    :param source_name: Unique name to give to the source. (uses package name otherwise)

    :raises AttributeError: If config_file_path is not provided and package doesn't have a "config" attribute.
    :raises ValueError: If loaded config file is invalid.
    """
    global _sources

    if not hasattr(package, "__path__"):
        raise ValueError("{!r} is not a Python package".format(package))

    if not config_file_path:
        config_file_path = getattr(package, "config", None)
    config = _load_config(config_file_path) if config_file_path else {}

    if not source_name:
        source_name = package.__name__.lower()

    _sources[source_name] = Source(source_name, package.__name__, config, True)


def _create_package(directory):
    """Creates a Python package object from given directory."""
    # Create a dummy package for the directory.
    package_name = hashlib.md5(directory.encode("utf8")).hexdigest()
    package_init = os.path.join(directory, "__init__.py")
    # Create __init__.py if it doesn't exist.
    if not os.path.exists(package_init):
        logger.info("Creating required __init__ module: {}".format(package_init))
        with open(package_init, "a"):
            pass
    try:
        package = imp.load_source(package_name, package_init)
        package.__path__ = [directory]
    except IOError as e:
        raise ValueError("Could not create package from {} with error: {}".format(directory, e))
    return package


def _is_module_available(module_name):
    """Determines whether given module name is available without importing."""
    try:
        return bool(importlib.util.find_spec(module_name))
    except ModuleNotFoundError:
        # If we get this error, that means an intermediate package couldn't be found.
        return False


def _generate_parser_aux(parser_name, group_name, source, _visiting):
    """
    Auxiliary function used by _generate_parser() to format the parser_name
    before running _generate_parser()
    """
    orig_parser_name = parser_name

    if parser_name.startswith("."):
        parser_name = group_name + parser_name

    # Pull out imported source.
    if ":" in parser_name:
        source_name, _, parser_name = parser_name.partition(":")
        if source_name not in _sources:
            raise RuntimeError(f"Unable to find source: {source_name}")
        source = _sources[source_name]

    if (parser_name, source.name) in _visiting:
        raise RuntimeError(f"Detected recursive loop: {group_name} -> {orig_parser_name}")

    try:
        return _generate_parser(parser_name, source, _visiting=_visiting)
    except ParserNotFoundError as e:
        raise RuntimeError(f"Unable to find {parser_name} with error: {e}")


def _generate_parser(name: str, source: Source, recursive=True, _visiting=None):
    """
    Generates parser for given name.

    :param str name: Name of parser or parser group.
    :param Source source: Source object containing parser.
    :param bool recursive: Recursively generate listed sub parsers.
        (otherwise only top level parsers will be produced)
    :param _visiting: Used internally for recursive loop detection.

    :returns: Either a Dispatcher object for a group of parsers or a Parser class.

    :raises ParserNotFound: If parser could not be found.
    """
    if _visiting is None:
        _visiting = set()

    _visiting.add((name, source.name))

    try:
        # First check if parser name is a parser group.
        options = dict(source.config[name])
    except KeyError:
        logger.debug("Generating parser: {}".format(name))
        if "." not in name:
            raise ParserNotFoundError("Invalid name {}".format(name))
        # If not, find and import the referenced mwcp.Parser class.
        module_name, _, class_name = name.rpartition(".")
        module_fullname = source.package.__name__ + "." + module_name

        logger.debug("Checking existence of {}".format(module_fullname))
        if not _is_module_available(module_fullname):
            raise ParserNotFoundError("{} module does not exist".format(module_fullname))

        logger.debug("Importing: {}".format(module_fullname))
        module = importlib.import_module(module_fullname)

        if not hasattr(module, class_name):
            raise ParserNotFoundError("{} is not in {}".format(class_name, module_fullname))

        klass = getattr(module, class_name)

        if not issubclass(klass, Parser):
            raise ParserNotFoundError("{}.{} is not a mwcp.Parser class".format(module_fullname, class_name))

        klass.name = name
        klass.source = source.name
        logger.debug("Created parser: {!r}".format(klass))
        _visiting.remove((name, source.name))
        return klass

    # Otherwise, instantiate a mwcp.Dispatcher class for the parser group.
    group_name = name
    parser_names = options.pop("parsers")
    sub_parsers = []
    if recursive:
        for parser_name in parser_names:
            sub_parsers.append(_generate_parser_aux(parser_name, group_name, source, _visiting))

    # Dereference default parser.
    default = options.pop("default", None)
    if default and recursive:
        options["default"] = _generate_parser_aux(default, group_name, source, _visiting)

    parser = Dispatcher(group_name, source.name, parsers=sub_parsers, **options)
    logger.debug("Created parser group: {!r}".format(parser))
    _visiting.remove((name, source.name))
    return parser


def _import_all_modules(package):
    """Recursively imports all modules from a given python package or directory."""
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = "{}.{}".format(package.__name__, name)
        module = importlib.import_module(full_name)
        if is_pkg:
            _import_all_modules(module)


def iter_parsers(name: str = None, source: str = None, config_only=True, _recursive=True):
    """
    Iterates all registered parsers.

    :param str name: Filters parser based on a particular name. (":" notation is also supported)
    :param str source: Filters parser based on a particular source.
                       (source is either the name of a python package or path to local directory)
    :param bool config_only: Whether to only include parsers listed in the parser configuration file.
                             (ie. ignore component parsers like "Foo.Implant")
    :param bool _recursive: Whether to generate sub parsers.
        (This is used internally, don't change it unless you know what you are doing)

    :yields: tuple containing: (Source tuple, parser)

    :raises ValueError: If a parser name or source could not be found.
    """
    global _sources

    if name and not source:
        # If name is using ":" notation, assume it is being organized by "source_name:parser_name"
        # (os.path.basename is necessary in-case source is a file path containing ":"'s)
        orig_name = name
        _, _, name = os.path.basename(name).rpartition(":")
        source = orig_name[: -(len(name) + 1)]

    # Use default source if one is not provided.
    source = source or _default_source or None

    sources = []
    if source:
        if source in _sources:
            sources.append((source, _sources[source]))
    else:
        sources += _sources.items()

    for source_name, source in sources:
        # Find list of parser names to generate
        if name:
            try:
                parser = _generate_parser(name, source, recursive=_recursive)
                yield source, parser
            except ParserNotFoundError as e:
                logger.debug("[{}] {}".format(source_name, e))
                # Parser couldn't be found for this source.
                continue
        else:
            # If parser name is not provided provide all parsers from the given source.
            for parser_name in source.config.keys():
                parser = _generate_parser(parser_name, source, recursive=_recursive)
                yield source, parser

            # Also list all the component parsers if requested.
            if not config_only:
                _import_all_modules(source.package)
                package_prefix = source.package.__name__ + "."
                for klass in set(Parser.iter_subclasses()):
                    # Ignore classes without DESCRIPTIONS since they are usually base classes.
                    if klass.DESCRIPTION and klass.__module__.startswith(package_prefix):
                        parser_name = "{}.{}".format(klass.__module__[len(package_prefix):], klass.__name__)
                        klass.name = parser_name
                        yield source, klass


def get_parser_descriptions(name=None, source=None, config_only=True):
    """
    Retrieve list of parser descriptions

    :param str name: Filters parser based on a particular name. (":" notation is also supported)
    :param str source: Filters parser based on a particular source.
                       (source is either the name of a python package or path to local directory)
    :param bool config_only: Whether to only include parsers listed in the parser configuration file.
                             (ie. ignore component parsers like "Foo.Implant")

    Returns list of tuples per parser. Tuple contains parser name, author, and description.
    """
    descriptions = []
    for _source, parser in iter_parsers(name=name, source=source, config_only=config_only, _recursive=False):
        descriptions.append(ParserInfo(parser.name, _source.name, parser.AUTHOR, parser.DESCRIPTION))
    return sorted(descriptions, key=lambda e: tuple(sub.lower() for sub in e))  # Case-insensitive sorting.
