from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List
import asyncio
from imap_tools import MailBox, AND
import logging
import os

from classifier import IssueClassifier
from service_handler import ServiceRequestHandler
from config import settings

app = FastAPI()
classifier = IssueClassifier()
service_handler = ServiceRequestHandler()

# Set up templates
templates = Jinja2Templates(directory="templates")

class IssueRequest(BaseModel):
    text: str
    source: str
    contact_email: Optional[str] = None
    priority: Optional[str] = "medium"

# Web routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/submit", response_class=HTMLResponse)
async def submit_form(request: Request):
    return templates.TemplateResponse("submit.html", {"request": request})

# API routes
@app.post("/api/process-issue")
async def process_issue(issue: IssueRequest):
    try:
        classification = classifier.classify_issue(issue.text)
        request = service_handler.create_request(issue.text, classification, issue.source)
        return request.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recent-requests")
async def get_recent_requests():
    # Get the 10 most recent requests
    requests = list(service_handler.requests.values())
    requests.sort(key=lambda x: x.timestamp, reverse=True)
    return [request.to_dict() for request in requests[:10]]

@app.get("/api/request/{request_id}")
async def get_request(request_id: str):
    request = service_handler.get_request(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request.to_dict()

# Email processing
async def process_email():
    while True:
        try:
            with MailBox(settings.EMAIL_SERVER).login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD) as mailbox:
                for msg in mailbox.fetch(AND(seen=False)):
                    classification = classifier.classify_issue(msg.text)
                    service_handler.create_request(msg.text, classification, "email")
                    # Mark email as read
                    mailbox.flag(msg.uid, 'SEEN', True)
        except Exception as e:
            logging.error(f"Error processing email: {e}")
        await asyncio.sleep(60)  # Check every minute

@app.on_event("startup")
async def startup_event():
    try:
        # Start email processing in background
        asyncio.create_task(process_email())
        logging.info("Email processing started successfully")
    except Exception as e:
        logging.error(f"Error during startup: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 