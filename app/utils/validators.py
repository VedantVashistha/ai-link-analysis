import ipaddress
import socket
from urllib.parse import urlparse


class URLValidationError(ValueError):
    pass


def validate_public_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https"):
        raise URLValidationError("URL must start with http:// or https://")

    hostname = parsed.hostname
    if not hostname:
        raise URLValidationError("Invalid URL: missing hostname")

    if hostname.lower() in {"localhost", "127.0.0.1", "0.0.0.0", "::1"}:
        raise URLValidationError("Access to localhost or loopback addresses is forbidden.")

    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise URLValidationError(f"Could not resolve hostname: {hostname}") from exc

    for info in addr_info:
        ip_str = info[4][0]
        ip_obj = ipaddress.ip_address(ip_str)
        if (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_multicast
            or ip_obj.is_reserved
        ):
            raise URLValidationError("Access to private or internal network addresses is blocked (SSRF protection).")

    return url.strip()