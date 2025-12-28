from fastapi import status
from fastapi.responses import RedirectResponse


def redirect_to_login():
    redirect_response = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key="access_token")
    return redirect_response
