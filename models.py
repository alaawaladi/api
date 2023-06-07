from pydantic import BaseModel, EmailStr, Field, validator
from email_validator import validate_email, EmailNotValidError

class EmailRequest(BaseModel):
    subject: str = Field(..., title="Subject", description="Email subject", max_length=100)
    email_list: list[EmailStr] = Field(..., title="Email List", description="List of recipient emails")
    body: str = Field(..., title="Body", description="Email body", max_length=1000)
    options: dict = Field({}, title="Options", description="Additional options for sending the email")

    @validator('email_list')
    def validate_email_list(cls, email_list):
        validated_emails = []
        for email in email_list:
            try:
                validated_email = validate_email(email)
                validated_emails.append(validated_email.email)
            except EmailNotValidError:
                raise ValueError(f"Invalid email format: {email}")
        return validated_emails
