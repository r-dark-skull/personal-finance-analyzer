from fastapi import APIRouter, Request
from core import EmailManager


router = APIRouter()
email_manager = EmailManager()


@router.get("/save_emails_for/{date}", response_description="Triggers the Data Fetching endpoint")
async def save_emails(date: str, request: Request):
    status = await email_manager.fetch_and_save_emails(date)
    return {"status": "success" if status else "fail"}


@router.get("/analyze_emails")
async def analyse_emails(request: Request):
    await email_manager.email_analyzer()
    return {"status": "done"}
