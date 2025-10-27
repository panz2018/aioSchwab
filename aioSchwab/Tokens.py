"""
Project: https://github.com/panz2018/aioSchwab

aioSchwab Tokens
----------------
Handles OAuth authorization and token retrieval using the Base HTTP client.
"""

from .Base import Base


class Tokens:
    def __init__(
        self,
        app_key: str,
        app_secret: str,
        callback_url: str,
    ):
        """
        Initialize the token manager.

        Args:
            app_key: Schwab app key credential.
            app_secret: Schwab app secret credential.
            callback_url: Redirect URI registered with Schwab API.
            base: Optional shared `Base` client instance.
        """
        self._app_key = app_key  # app key credential
        self._app_secret = app_secret  # app secret credential
        self._callback_url = callback_url.rstrip("/")  # callback url to use

        self._validate_input(self._app_key, self._app_secret, self._callback_url)

        self.client = Base("https://api.schwabapi.com/")

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------
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
            callback_url (str): Callback URL registered with Schwab API.

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

    # -------------------------------------------------------------------------
    # Authorization
    # -------------------------------------------------------------------------
    def auth_url(self) -> str:
        """
        Generate the authorization URL that the user must visit to grant access.

        Returns:
            The OAuth2 authorization URL.
        """
        # get and open the link that the user will authorize with.
        return (
            f"https://api.schwabapi.com/v1/oauth/authorize"
            f"?client_id={self._app_key}"
            f"&redirect_uri={self._callback_url}"
        )
