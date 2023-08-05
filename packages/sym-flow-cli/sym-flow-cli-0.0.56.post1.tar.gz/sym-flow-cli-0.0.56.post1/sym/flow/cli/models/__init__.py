from dataclasses import dataclass
from typing import TypedDict

from sym.flow.cli.errors import InvalidTokenError


@dataclass
class Organization(TypedDict):
    slug: str
    client_id: str


SymOrganization = Organization(slug="sym", client_id="P5juMqe7UUpKo6634ZeuUgZF3QTXyIfj")
HealthyHealthOrganization = Organization(
    slug="healthy-health", client_id="Y4dnvjDlRibbKqSXA57hFnvZKyINHyJW"
)


@dataclass
class UserCredentials:
    username: str
    password: str


@dataclass
class AuthToken(TypedDict):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    scope: str


def parse_auth_token(json_response: dict) -> AuthToken:
    try:
        return AuthToken(
            access_token=json_response["access_token"],
            refresh_token=json_response["refresh_token"],
            token_type=json_response["token_type"],
            expires_in=json_response["expires_in"],
            scope=json_response["scope"],
        )
    except KeyError:
        raise InvalidTokenError(str(json_response))
