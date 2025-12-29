"""Check if a password has been compromised in a data breach."""

import hashlib

import requests
from fastapi import HTTPException, status


def request_api_data(query_char: str) -> requests.Response:
    """Fetch data from the Have I Been Pwned API.

    Args:
        query_char (str): The first 5 characters of the SHA-1 hashed
            password.

    Returns:
        HTTP Response: An object containing password hash suffixes (if
            any) returned by the API.

    Raises:
        HTTPException: Raised when the API request fails.
    """
    pwned_url = "https://api.pwnedpasswords.com/range/" + query_char
    try:
        response = requests.get(pwned_url)
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to check password safety right now.Please try again later.",
        )
    return response


def check_if_password_leaked(response, hash_to_check: str) -> bool:
    """Check whether the provided hash exists in the response data.

    Args:
        response: The API response containing hash leak data. Each line
            containing a hash and its count.
        hash_to_check (str): The rest of the SHA-1 hashed password to
            search for in the API response.

    Returns:
        bool: True if the hash exists in response, otherwise False.
    """
    api_hashes = (line.split(":") for line in response.text.splitlines())
    for api_hash, count in api_hashes:
        if api_hash == hash_to_check:
            return True
    return False


def password_breach_check(password: str) -> None:
    """Check if the given password has been compromised.

    Args:
        password (str): The password string to be checked for breaches.

    Returns:
        None.

    Raises:
        HTTPException: Raised if the password exists in the breach
            database.
    """
    sha1password: str = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5_chars, rest = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_chars)
    breached: bool = check_if_password_leaked(response, rest)
    if breached:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password found in a breach — try another.",
        )
