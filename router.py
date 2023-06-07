# router.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from functions import send_email, ProfileHandler
from email_validator import validate_email
from models import EmailRequest
import os

profile_handler = ProfileHandler()
router = APIRouter()


@router.get("/profiles")
async def get_profiles():
    return profile_handler.get_profiles()

@router.get("/profiles/{profile_name:path}")
def check_profile(profile_name: str):
    # Step 1: Extract profile name
    if not profile_handler.profile_exists(profile_name):
        raise HTTPException(status_code=404, detail="Profile does not exist")
    if not profile_name:
        return {"message": "Please provide a profile name."}
    return profile_handler.check_profile(profile_name)


@router.post("/send-email")
async def handle_send_email(request_data: EmailRequest):
    subject = request_data.subject.strip()
    email_list = request_data.email_list
    body = request_data.body.strip()
    options = request_data.options
    selected_profiles = options.get("selected_profiles", [])

    errors = []

    if not subject:
        errors.append("Subject field is required.")
    if not email_list or all(email.strip() == '' for email in email_list):
        errors.append("Email list field is required.")
    elif not all(validate_email(email.strip()) for email in email_list):
        raise HTTPException(status_code=400, detail="Invalid email format in the email list.")
    if not body:
        errors.append("Body field is required.")
    if not selected_profiles or all(profile.strip() == '' for profile in selected_profiles):
        errors.append("Selected profiles field is required.")

    if errors:
        raise HTTPException(status_code=400, detail=errors[0])

    for email in email_list:
        for profile_path in selected_profiles:
            profile_name = os.path.basename(profile_path)
            if not profile_handler.profile_exists(profile_name):
                raise HTTPException(status_code=400, detail=f"Profile '{profile_name}' does not exist")
            try:
                send_email(email, subject, body, profile_path)
            except Exception as e:
                raise HTTPException(status_code=422, detail=str(e))

    return {"message": "Email sent successfully."}

