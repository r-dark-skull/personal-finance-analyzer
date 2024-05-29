from fastapi import APIRouter, Request
from core import EmailManager
from logging import getLogger


logger = getLogger(__name__)
router = APIRouter()
email_manager = EmailManager()


@router.get("/save_emails_for/{sdate}",
            response_description="Triggers the Data Fetching endpoint")
@router.get("/save_emails_for/{sdate}/{edate}",
            response_description="Triggers the Data Fetching endpoint")
async def save_emails(sdate: str, edate: str = None, request: Request = None):
    logger.info(f"Save Email Request : {sdate} - {edate}")

    status = await email_manager.fetch_and_save_emails(sdate, edate)

    logger.info(f"Request Status : {status}")
    return {"status": "success" if status else "fail"}


@router.get("/analyze_emails")
async def analyse_emails(request: Request):
    logger.info(f"Analyze Email Request")

    await email_manager.email_analyzer()
    return {"status": "done"}
