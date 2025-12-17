import hashlib

import requests
from fastapi import HTTPException, status
from requests import RequestException


def request_api_data(query_char):
    pwned_url = "https://api.pwnedpasswords.com/range/" + query_char
    try:
        response = requests.get(pwned_url)
    except RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to check password safety right now",
        )
    return response


def get_password_leaks_count(response, hash_to_check):
    api_hashes = (line.split(":") for line in response.text.splitlines())
    for api_hash, count in api_hashes:
        if api_hash == hash_to_check:
            return True
    return False


def password_breach_check(password: str):
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5_chars, rest = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_chars)
    return get_password_leaks_count(response, rest)
