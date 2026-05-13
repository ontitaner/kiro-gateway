# -*- coding: utf-8 -*-

# @AI_GENERATED
"""
SSL/TLS verification helper for httpx clients.

Provides a single source of truth for how the gateway should verify
upstream TLS certificates, based on SSL_VERIFY and SSL_CA_BUNDLE env vars.

Usage:
    from kiro.ssl_utils import get_httpx_verify

    client = httpx.AsyncClient(verify=get_httpx_verify(), timeout=30)
"""

from pathlib import Path
from typing import Union

from loguru import logger

from kiro.config import SSL_VERIFY, SSL_CA_BUNDLE

# Cache resolved value and whether we already warned, to avoid log spam
_resolved: Union[bool, str, None] = None
_warned: bool = False


def get_httpx_verify() -> Union[bool, str]:
    """
    Returns the value to pass to httpx's ``verify=`` parameter.

    Resolution order:
      1. If SSL_CA_BUNDLE is set and points to an existing file -> return that path
      2. Else if SSL_VERIFY is False -> return False (disable verification)
      3. Else -> return True (default strict verification via certifi)

    Falls back gracefully with warnings if the CA bundle path is invalid.
    """
    global _resolved, _warned

    if _resolved is not None:
        return _resolved

    if SSL_CA_BUNDLE:
        ca_path = Path(SSL_CA_BUNDLE).expanduser()
        if ca_path.is_file():
            logger.info(f"SSL: using custom CA bundle: {ca_path}")
            _resolved = str(ca_path)
            return _resolved
        else:
            if not _warned:
                logger.warning(
                    f"SSL_CA_BUNDLE is set but file not found: {ca_path}. "
                    "Falling back to SSL_VERIFY setting."
                )
                _warned = True

    if not SSL_VERIFY:
        if not _warned:
            logger.warning(
                "SSL: certificate verification is DISABLED (SSL_VERIFY=false). "
                "This is insecure and should only be used on trusted networks "
                "with corporate TLS inspection. Prefer setting SSL_CA_BUNDLE instead."
            )
            _warned = True
        _resolved = False
        return _resolved

    _resolved = True
    return _resolved


def reset_cache() -> None:
    """Reset internal cache. Intended for tests only."""
    global _resolved, _warned
    _resolved = None
    _warned = False
# @AI_GENERATED: end
