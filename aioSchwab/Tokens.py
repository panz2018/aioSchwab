"""
Project: https://github.com/panz2018/aioSchwab
"""

from .BaseClient import BaseClient

BaseClient.base_url = r"https://api.schwabapi.com/"


class Tokens:
    def __init__(
        self,
        app_key: str,
        app_secret: str,
        callback_url: str,
    ):
        callback_url = callback_url.rstrip("/")
        self._validate_input(app_key, app_secret, callback_url)

        self._app_key = app_key  # app key credential
        self._app_secret = app_secret  # app secret credential
        self._callback_url = callback_url  # callback url to use

    @staticmethod
    def _validate_input(
        app_key: str,
        app_secret: str,
        callback_url: str,
    ) -> None:
        """
        Validates initialization parameters.

        Args:
            app_key (str): App key credentials.
            app_secret (str): App secret credentials.

        Raises:
            ValueError: If any validation checks fail.
        """
        if not app_key:
            raise ValueError("[aioSchwab] app_key cannot be None.")
        if len(app_key) not in (32, 48):
            raise ValueError("[aioSchwab] App key has invalid length.")

        if not app_secret:
            raise ValueError("[aioSchwab] app_secret cannot be None.")
        if len(app_secret) not in (16, 64):
            raise ValueError("[aioSchwab] App secret has invalid length.")

        if not callback_url:
            raise ValueError("[aioSchwab] Callback URL cannot be None.")
        if not callback_url.startswith("https"):
            raise ValueError("[aioSchwab] Callback URL must be https.")
        if callback_url.endswith("/"):
            raise Exception('[aioSchwab] Callback URL cannot be path (ends with "/").')

    def auth_url(self) -> str:
        # get and open the link that the user will authorize with.
        auth_url = (
            f"https://api.schwabapi.com/v1/oauth/authorize"
            f"?client_id={self._app_key}"
            f"&redirect_uri={self._callback_url}"
        )
        return auth_url
