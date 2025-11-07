from fastapi import Depends, APIRouter, Request
from fastapi_sso.sso.google import GoogleSSO
import structlog

from config import settings

logger = structlog.stdlib.get_logger()

router = APIRouter()


def get_google_sso() -> GoogleSSO:
    return GoogleSSO(
        settings.GOOGLE_CLIENT_ID,
        settings.GOOGLE_CLIENT_SECRET,
        redirect_uri="http://localhost:8000/google/callback",
        allow_insecure_http=settings.GOOGLE_CLIENT_HTTP,
    )


@router.get("/google/login")
async def google_login(google_sso: GoogleSSO = Depends(get_google_sso)):
    return await google_sso.get_login_redirect()


@router.get("/google/callback")
async def google_callback(request: Request, google_sso: GoogleSSO = Depends(get_google_sso)):
    user = await google_sso.verify_and_process(request)
    logger.info(user)
    """ Format:
        {
            "id":"<number>",
            "email":"<email>",
            "first_name":"<first>",
            "last_name":"<last>",
            "display_name":"<display name>",
            "picture":"https://<host>/<path>",
            "provider":"google"
        }
    """
    return user
