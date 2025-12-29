from fastapi import status
from fastapi.responses import RedirectResponse


def redirect_to_login():
    """Redirects user to the login page and clears access token.

    Returns:
        RedirectResponse: A response that redirects the client to the
            login page and clears the access token cookie.
    """
    redirect_response = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key="access_token")
    return redirect_response
