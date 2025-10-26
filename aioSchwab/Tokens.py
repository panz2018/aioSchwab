"""
Project: https://github.com/panz2018/aioSchwab
"""

from .BaseClient import BaseClient

BaseClient.base_url = r"https://api.schwabapi.com/trader/v1"


class Tokens:
    def __init__(
        self,
        app_key: str,
        app_secret: str,
    ):
        self._validate_input(app_key=app_key, app_secret=app_secret)

        self._app_key = app_key  # app key credential
        self._app_secret = app_secret  # app secret credential

    @staticmethod
    def _validate_input(
        app_key: str,
        app_secret: str,
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
