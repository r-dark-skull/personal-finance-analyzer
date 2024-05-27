from fastapi import APIRouter, Request
from core import EmailManager


router = APIRouter()
email_manager = EmailManager()


@router.get("/save_emails_for/{sdate}", response_description="Triggers the Data Fetching endpoint")
@router.get("/save_emails_for/{sdate}/{edate}", response_description="Triggers the Data Fetching endpoint")
async def save_emails(sdate: str, edate: str = None, request: Request = None):
    status = await email_manager.fetch_and_save_emails(sdate, edate)
    return {"status": "success" if status else "fail"}


@router.get("/analyze_emails")
async def analyse_emails(request: Request):
    await email_manager.email_analyzer()
    return {"status": "done"}
