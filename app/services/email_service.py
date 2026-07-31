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