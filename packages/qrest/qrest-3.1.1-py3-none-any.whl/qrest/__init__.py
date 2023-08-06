__version__ = "3.1.1"

from .resource import JSONResource  # noqa: F401
from .conf import APIConfig, ResourceConfig, BodyParameter, QueryParameter  # noqa: F401
from .exception import RestClientConfigurationError  # noqa: F401
from .resource import API  # noqa: F401
