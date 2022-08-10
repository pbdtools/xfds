class ConfigNotFound(Exception):
    """Could not find the configuration file."""

    pass


class xFDSNotDefined(Exception):
    """xfds is not defined in the root of the config file."""

    pass


class RenderNotDefined(Exception):
    """render is not defined under xfds in the config file."""

    pass


class ModelNameNotDefiend(Exception):
    """Model specification does not have a name provided."""

    pass
