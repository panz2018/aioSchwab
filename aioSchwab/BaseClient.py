"""
Project: https://github.com/panz2018/aioSchwab

aioSchwab Base Client
This module defines the BaseClient class, providing shared async HTTP functionality
used by higher-level API clients (e.g., AuthorizedClient, TokenManager).
"""

import asyncio
import httpx
from typing import Any, Optional


class BaseClient:
    """A base asynchronous HTTP client providing common request methods."""

    base_url: str = ""
    timeout: float = 10.0

    _client: Optional[httpx.AsyncClient] = None
    _init_lock = asyncio.Lock()
    _header_lock = asyncio.Lock()

    # -------------------------------------------------------------------------
    # Client management
    # -------------------------------------------------------------------------
    @classmethod
    async def _get_client(cls) -> httpx.AsyncClient:
        """
        Lazily initialize a global AsyncClient instance.
        Thread-safe with an async lock.
        """
        if cls._client is None:
            async with cls._init_lock:
                if cls._client is None:
                    cls._client = httpx.AsyncClient(
                        base_url=cls.base_url.rstrip("/"),
                        timeout=cls.timeout,
                    )
        return cls._client

    @classmethod
    async def close(cls) -> None:
        """
        Close the AsyncClient session and reset the internal reference.
        Should be called during shutdown.
        """
        if cls._client is not None:
            await cls._client.aclose()
            cls._client = None

    # -------------------------------------------------------------------------
    # Core request logic
    # -------------------------------------------------------------------------
    @classmethod
    async def _request(
        cls, method: str, endpoint: str, **kwargs: Any
    ) -> httpx.Response:
        """
        Perform an HTTP request using the global AsyncClient.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path, with or without leading slash.
            **kwargs: Additional arguments passed to httpx.request().

        Returns:
            httpx.Response: The HTTP response object.
        """
        client = await cls._get_client()
        url = f"{cls.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return await client.request(method, url, **kwargs)

    # -------------------------------------------------------------------------
    # Common HTTP methods
    # -------------------------------------------------------------------------
    @classmethod
    async def get(cls, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Perform an HTTP GET request."""
        return await cls._request("GET", endpoint, **kwargs)

    @classmethod
    async def post(cls, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Perform an HTTP POST request."""
        return await cls._request("POST", endpoint, **kwargs)

    @classmethod
    async def put(cls, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Perform an HTTP PUT request."""
        return await cls._request("PUT", endpoint, **kwargs)

    @classmethod
    async def delete(cls, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Perform an HTTP DELETE request."""
        return await cls._request("DELETE", endpoint, **kwargs)

    # -------------------------------------------------------------------------
    # Header management
    # -------------------------------------------------------------------------
    @classmethod
    async def update_headers(cls, **headers: str) -> None:
        """
        Safely update the default headers of the shared AsyncClient.

        Args:
            **headers: Key-value pairs to update in the request headers.
        """
        client = await cls._get_client()
        async with cls._header_lock:
            client.headers.update(headers)
