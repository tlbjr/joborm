from fastapi import Depends, APIRouter, Request
from fastapi_sso.sso.google import GoogleSSO
import structlog

from config import settings
from db.models import UserRecord
from db.services import UserSvc
from shared import UserFrom

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
    """Allow a Google SSO user to login

    user data available after verification:
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
    user = await google_sso.verify_and_process(request)
    logger.debug(user)
    user_rec = UserSvc.get_by_email(user.get("email"))
    if user_rec is None:
        user_new = UserRecord.model_validate(user)
        user_new.user_from = UserFrom.GOOGLE
        user_rec = UserSvc.insert_user_record(user_new)

    # TODO Allow the user to continue where they left off
    return user
