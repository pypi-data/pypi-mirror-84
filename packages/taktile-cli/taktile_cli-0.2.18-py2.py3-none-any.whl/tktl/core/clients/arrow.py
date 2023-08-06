from pyarrow.flight import (
    ClientAuthHandler,
    FlightClient,
    FlightDescriptor,
    FlightInfo,
    Ticket,
)

from tktl.core.clients import Client
from tktl.core.config import settings
from tktl.core.exceptions import AuthenticationError
from tktl.core.schemas.repository import _format_grpc_url
from tktl.core.serializers import deserialize_arrow, serialize_arrow
from tktl.core.t import ServiceT


class ApiKeyClientAuthHandler(ClientAuthHandler):
    """An example implementation of authentication via ApiKey."""

    def __init__(self, api_key: str):
        super(ApiKeyClientAuthHandler, self).__init__()
        self.api_key = api_key

    def authenticate(self, outgoing, incoming):
        outgoing.write(self.api_key)
        self.api_key = incoming.read()

    def get_token(self):
        return self.api_key


class ArrowFlightClient(Client):

    TRANSPORT = ServiceT.GRPC

    def __init__(
        self,
        api_key: str,
        repository_name: str,
        branch_name: str = None,
        local: bool = False,
    ):
        super().__init__(
            api_key=api_key,
            repository_name=repository_name,
            branch_name=branch_name,
            local=local,
        )

    @staticmethod
    def format_url(url: str) -> str:
        return _format_grpc_url(url)

    @property
    def local_endpoint(self):
        return settings.LOCAL_ARROW_ENDPOINT

    def list_deployments(self):
        pass

    def list_commands(self):
        return self.client.list_actions()

    def authenticate(self, endpoint_name: str):
        location = self.get_endpoint_and_location(endpoint_name)
        if not location:
            return
        self.location = location
        client = FlightClient(location=self.location)
        client.authenticate(
            ApiKeyClientAuthHandler(api_key=self.taktile_client.api_key)
        )
        self.client = client

    def predict(self, inputs):
        table = serialize_arrow(inputs)
        descriptor = self.get_flight_info(command_name=str.encode(self.endpoint))
        writer, reader = self.client.do_exchange(descriptor.descriptor)
        with writer:
            writer.begin(table.schema)
            writer.write_table(table)
            writer.done_writing()
            table = reader.read_all()
            return deserialize_arrow(table)

    def get_sample_data(self):
        if not self.endpoint:
            raise AuthenticationError(
                "Please authenticate against a specific endpoint first"
            )
        x_info = self.client.do_get(Ticket(ticket=str.encode(f"{self.endpoint}__X")))
        y_info = self.client.do_get(Ticket(ticket=str.encode(f"{self.endpoint}__y")))
        return (
            deserialize_arrow(x_info.read_all()),
            deserialize_arrow(y_info.read_all()),
        )

    def get_schema(self):
        if not self.endpoint:
            raise AuthenticationError(
                "Please authenticate against a specific endpoint first"
            )
        info = self.get_flight_info(str.encode(self.endpoint))
        return info.schema

    def get_flight_info(self, command_name: bytes) -> FlightInfo:
        descriptor = FlightDescriptor.for_command(command_name)
        return self.client.get_flight_info(descriptor)
