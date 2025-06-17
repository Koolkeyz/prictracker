"""
Email service for the PriceTracker application.
Handles sending emails for price alerts, user registration, password resets etc.
"""

from typing import List, Optional, Dict, Any, Union
import os
from pathlib import Path
from datetime import datetime


from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from ..helpers.logger import get_logger
from ..helpers.settings import get_settings

# Define the directory for email templates
TEMPLATES_DIR = Path(__file__).parent / "templates"
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Initialize logger
logger = get_logger("pricetracker_mail")
settings = get_settings()

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USERNAME,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_FROM_NAME=settings.SMTP_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=TEMPLATES_DIR,
)


def create_email_message(subject: str, recipients: List[str], body: Dict[str, any]):
    """
    Create an email message with the given subject, recipients and body.

    Args:
        subject (str): Subject of the email.
        recipients (List[str]): List of recipient email addresses.
        body (Dict[str, Any]): Body of the email, can include HTML content.

    Returns:
        MessageSchema: Configured email message ready to be sent.
    """
    return MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=body,
        subtype=MessageType.html,
        headers={"X-Mailer": "PriceTracker Mailer"},
    )


mailer = FastMail(mail_config)
