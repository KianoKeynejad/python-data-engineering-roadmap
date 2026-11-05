import os
import secrets

from fastapi import Header, HTTPException, status


def verify_api_key(x_api_key: str = Header(...)):
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key is not configured",
        )

    if not secrets.compare_digest(x_api_key, api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )