"""
Project: https://github.com/panz2018/aioSchwab

aioSchwab Base Client
---------------------
This module defines the `Base` class, a reusable asynchronous HTTP client
that provides shared networking logic for higher-level clients such as
`Tokens` and `AuthorizedClient`.

It wraps an internal `httpx.AsyncClient` for efficient connection pooling,
and exposes thread-safe methods for sending requests and updating headers.
"""

import asyncio
import httpx
from typing import Any


class Base:
    """
    A base asynchronous HTTP client providing common request utilities.

    This class manages a shared `httpx.AsyncClient` session, which should
    be explicitly closed using `await aclose()` when the client is no longer needed.

    Attributes:
        base_url (str): The base API URL for all requests.
        timeout (float): Request timeout in seconds.
    """

    def __init__(self, base_url: str = "", timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._lock = asyncio.Lock()

        # Underlying reusable HTTP client
        self._client: httpx.AsyncClient = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
        )

    # -------------------------------------------------------------------------
    # Lifecycle management
    # -------------------------------------------------------------------------
    async def aclose(self) -> None:
        """
        Gracefully close the internal HTTP session.

        Should be awaited before program exit or when cleaning up resources.
        """
        await self._client.aclose()

    # -------------------------------------------------------------------------
    # Core request logic
    # -------------------------------------------------------------------------
    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Send a raw HTTP request using the internal AsyncClient.

        Args:
            method: The HTTP method (e.g., "GET", "POST", "PUT", "DELETE").
            endpoint: The API endpoint path, with or without leading slash.
            **kwargs: Optional keyword arguments passed directly to
                      `httpx.AsyncClient.request()`.

        Returns:
            httpx.Response: The raw HTTP response.
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return await self._client.request(method, url, **kwargs)

    # -------------------------------------------------------------------------
    # Common HTTP methods
    # -------------------------------------------------------------------------
    async def get(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Perform an HTTP GET request."""
        return await self._request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Perform an HTTP POST request."""
        return await self._request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Perform an HTTP PUT request."""
        return await self._request("PUT", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Perform an HTTP DELETE request."""
        return await self._request("DELETE", endpoint, **kwargs)

    # -------------------------------------------------------------------------
    # Header management
    # -------------------------------------------------------------------------
    async def update_headers(self, **headers: str) -> None:
        """
        Safely update the default headers for all future requests.

        This method acquires a lock to ensure thread-safety when
        modifying the internal header dictionary.

        Example:
            >>> await client.update_headers(Authorization="Bearer token")
        """
        async with self._lock:
            self._client.headers.update(headers)
