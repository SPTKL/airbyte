#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from typing import Any, List, Mapping

import pendulum
from airbyte_cdk.sources.declarative.interpolation.interpolated_mapping import InterpolatedMapping
from airbyte_cdk.sources.declarative.interpolation.interpolated_string import InterpolatedString
from airbyte_cdk.sources.streams.http.requests_native_auth.abstract_oauth import AbstractOauth2Authenticator


class DeclarativeOauth2Authenticator(AbstractOauth2Authenticator):
    """
    Generates OAuth2.0 access tokens from an OAuth2.0 refresh token and client credentials based on
    a declarative connector configuration file. Credentials can be defined explicitly or via interpolation
    at runtime. The generated access token is attached to each request via the Authorization header.
    """

    def __init__(
        self,
        token_refresh_endpoint: str,
        client_id: str,
        client_secret: str,
        refresh_token: str,
        config: Mapping[str, Any],
        scopes: List[str] = None,
        token_expiry_date: str = None,
        access_token_name: str = "access_token",
        expires_in_name: str = "expires_in",
        refresh_request_body: Mapping[str, Any] = None,
    ):
        self.config = config
        self.token_refresh_endpoint = InterpolatedString(token_refresh_endpoint)
        self.client_secret = InterpolatedString(client_secret)
        self.client_id = InterpolatedString(client_id)
        self.refresh_token = InterpolatedString(refresh_token)
        self.scopes = scopes
        self.access_token_name = InterpolatedString(access_token_name)
        self.expires_in_name = InterpolatedString(expires_in_name)
        self.refresh_request_body = InterpolatedMapping(refresh_request_body)

        self.token_expiry_date = (
            pendulum.parse(InterpolatedString(token_expiry_date).eval(self.config))
            if token_expiry_date
            else pendulum.now().subtract(days=1)
        )
        self.access_token = None

    @property
    def config(self) -> Mapping[str, Any]:
        return self._config

    @config.setter
    def config(self, value: Mapping[str, Any]):
        self._config = value

    @property
    def token_refresh_endpoint(self) -> InterpolatedString:
        get_some = self._token_refresh_endpoint.eval(self.config)
        return get_some

    @token_refresh_endpoint.setter
    def token_refresh_endpoint(self, value: InterpolatedString):
        self._token_refresh_endpoint = value

    @property
    def client_id(self) -> InterpolatedString:
        return self._client_id.eval(self.config)

    @client_id.setter
    def client_id(self, value: InterpolatedString):
        self._client_id = value

    @property
    def client_secret(self) -> InterpolatedString:
        return self._client_secret.eval(self.config)

    @client_secret.setter
    def client_secret(self, value: InterpolatedString):
        self._client_secret = value

    @property
    def refresh_token(self) -> InterpolatedString:
        return self._refresh_token.eval(self.config)

    @refresh_token.setter
    def refresh_token(self, value: InterpolatedString):
        self._refresh_token = value

    @property
    def scopes(self) -> [str]:
        return self._scopes

    @scopes.setter
    def scopes(self, value: [str]):
        self._scopes = value

    @property
    def token_expiry_date(self) -> pendulum.DateTime:
        return self._token_expiry_date

    @token_expiry_date.setter
    def token_expiry_date(self, value: pendulum.DateTime):
        self._token_expiry_date = value

    @property
    def access_token_name(self) -> InterpolatedString:
        return self._access_token_name.eval(self.config)

    @access_token_name.setter
    def access_token_name(self, value: InterpolatedString):
        self._access_token_name = value

    @property
    def expires_in_name(self) -> InterpolatedString:
        return self._expires_in_name.eval(self.config)

    @expires_in_name.setter
    def expires_in_name(self, value: InterpolatedString):
        self._expires_in_name = value

    @property
    def refresh_request_body(self) -> InterpolatedMapping:
        return self._refresh_request_body.eval(self.config)

    @refresh_request_body.setter
    def refresh_request_body(self, value: InterpolatedMapping):
        self._refresh_request_body = value

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self, value: str):
        self._access_token = value
