"""
Email service.

This module handles sending emails
for account verification and password reset.
"""



class EmailService:
    """
    Service responsible for email operations.
    """

    @staticmethod
    def send_verification_email(
        email: str,
        token: str
    ) -> None:
        """
        Send account verification email.

        For now, this method simulates
        sending an email by printing the link.
        """

        verification_link = (
            f"http://127.0.0.1:8000/auth/verify-email/{token}"
        )

        print("\n========== VERIFICATION EMAIL ==========")
        print(f"To: {email}")
        print("Subject: Verify your account")
        print()
        print(
            "Click this link to verify your account:"
        )
        print(verification_link)
        print("========================================\n")

    def send_reset_password_email(
        email: str,
        token: str
    ):
        link = (
            f"http://127.0.0.1:8000/auth/reset-password/{token}"
        )

        print("==============================")
        print("PASSWORD RESET EMAIL")
        print(f"To: {email}")
        print("")
        print("Click this link:")
        print(link)
        print("==============================")
=======
import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

SMTP_FROM = os.getenv("SMTP_FROM")

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:3000"
)


def send_email(
    recipient_email: str,
    subject: str,
    body: str
):
    """
    Send a generic email.

    Args:
        recipient_email: Email address of receiver.
        subject: Email subject.
        body: Email content.
    """

    message = MIMEMultipart()

    message["From"] = SMTP_FROM
    message["To"] = recipient_email
    message["Subject"] = subject


    message.attach(
        MIMEText(
            body,
            "plain"
        )
    )


    with smtplib.SMTP(
        SMTP_HOST,
        SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            SMTP_USERNAME,
            SMTP_PASSWORD
        )

        server.send_message(message)



def send_verification_email(
    email: str,
    token: str
):
    """
    Send account verification email.

    Args:
        email: User email.
        token: Verification JWT token.
    """

    verification_link = (
        f"{FRONTEND_URL}"
        f"/verify-email?token={token}"
    )


    body = f"""
Hello,

Thank you for creating an account.

Please verify your email address
by clicking the link below:

{verification_link}


This link will expire soon.

Regards,
Collaborative Platform Team
"""


    send_email(
        recipient_email=email,
        subject="Verify your account",
        body=body
    )



def send_password_reset_email(
    email: str,
    token: str
):
    """
    Send password reset email.

    Args:
        email: User email.
        token: Password reset JWT token.
    """

    reset_link = (
        f"{FRONTEND_URL}"
        f"/reset-password?token={token}"
    )


    body = f"""
Hello,

You requested a password reset.

Click the link below to create
a new password:

{reset_link}


If you did not request this,
ignore this email.

Regards,
Collaborative Platform Team
"""


    send_email(
        recipient_email=email,
        subject="Reset your password",
        body=body
    )
