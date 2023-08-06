from typing import Tuple

from auth0.v3.authentication import GetToken


def get_access_token(
    key: str,
    secret: str,
    auth0_domain: str = None,
    audience: str = "https://api.mondobrain.com/",
) -> Tuple[str, str]:
    """Get an access token from Auth0 using the Client Credentials Exchange method
    Return is a tuple of two tokens (access, refresh). Refresh may be none
    """
    if auth0_domain is None:
        auth0_domain = "mb-production.us.auth0.com"

    gt = GetToken(auth0_domain)
    resp = gt.client_credentials(key, secret, audience)
    access = resp.get("access_token")
    refresh = resp.get("refresh_token", None)

    return (access, refresh)
