from typing import Annotated

from fastapi import Depends, APIRouter, Request
from fastapi_sso.sso.google import GoogleSSO
import structlog

from config import settings
from db.pg import get_session, Session
from db.services import UserSvc

logger = structlog.stdlib.get_logger()

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


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
async def google_callback(
    request: Request, session: SessionDep, google_sso: GoogleSSO = Depends(get_google_sso)
):
    """Allow a Google SSO user to login"""
    # TODO verify_and_process(request) can throw exceptions:
    # oauthlib.oauth2.rfc6749.errors.InvalidGrantError: (invalid_grant) Bad Request
    user = await google_sso.verify_and_process(request)
    user_rec = UserSvc.get_by_email(session, user.email)
    if user_rec is None:
        user_rec = UserSvc.insert_from_google_sso(session, user)

    # TODO Allow the user to continue where they left off
    return user_rec
