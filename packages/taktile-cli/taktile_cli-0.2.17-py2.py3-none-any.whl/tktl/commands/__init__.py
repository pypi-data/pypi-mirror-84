import abc

from tktl.core.clients import TaktileClient
from tktl.core.config import settings
from tktl.core.loggers import LOG


class CommandBase(object):
    def __init__(self, api=None):
        self.api = api


class BaseApiCommand:

    __metaclass__ = abc.ABCMeta

    def __init__(
        self, api_url=settings.DEPLOYMENT_API_URL,
    ):
        self.api_url = api_url
        self.client = self._get_client()

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def _get_client(self):
        return TaktileClient(api_url=self.api_url)


class BaseDeploymentApiCommand(BaseApiCommand):
    def __init__(self):
        super().__init__(api_url=settings.DEPLOYMENT_API_URL)

    def execute(self, *args, **kwargs):
        raise NotImplementedError


class BaseTaktileApiCommand(BaseApiCommand):
    def __init__(self):
        super().__init__(api_url=settings.TAKTILE_API_URL)

    def execute(self, *args, **kwargs):
        raise NotImplementedError
