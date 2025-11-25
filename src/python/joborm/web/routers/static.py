from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import structlog

logger = structlog.stdlib.get_logger()

router = APIRouter()


@router.get("/example/pages/opportunity", response_class=HTMLResponse)
async def ex_opportunity_page():
    return """<html>
    <head>
        <title>A Company hiring A Job</title>
    </head>
    <body>
        <h1>Look, ma! An opportunity page!</h1>
    </body>
</html>"""
