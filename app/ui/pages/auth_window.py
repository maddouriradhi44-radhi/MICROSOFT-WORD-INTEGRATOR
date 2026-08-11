from PySide6.QtWidgets import QMainWindow, QStackedWidget

from app.ui.components.auth_widgets import BG_WINDOW
from app.ui.pages.login_screen import LoginScreen
from app.ui.pages.signup_screen import SignUpScreen
from app.ui.pages.email_verification_screen import EmailVerificationScreen
from app.ui.pages.forget_password_screen import ForgotPasswordScreen
from app.ui.pages.reset_password_screen import ResetPasswordScreen


class AuthWindow(QMainWindow):

    def __init__(self, on_authenticated=None):
        super().__init__()

        self.on_authenticated = on_authenticated

        self.setWindowTitle("Microsoft Word Integrator")
        self.setFixedSize(480, 640)
        self.setStyleSheet(
            f"QMainWindow {{ background-color: {BG_WINDOW}; }}"
        )

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_screen = LoginScreen(
            on_success=self._handle_authenticated,
            on_navigate=self.navigate_to,
        )

        self.stack.addWidget(self.login_screen)

        self.signup_screen = None
        self.email_verification_screen = None
        self.forgot_password_screen = None
        self.reset_password_screen = None

        self.stack.setCurrentWidget(self.login_screen)

    def _handle_authenticated(self, auth_result):
        if self.on_authenticated:
            self.on_authenticated(auth_result)

    def navigate_to(self, screen_name, **kwargs):

        if screen_name == "login":
            self.stack.setCurrentWidget(self.login_screen)

        elif screen_name == "signup":
            if self.signup_screen is None:
                self.signup_screen = SignUpScreen(
                    on_success=self._go_to_email_verification,
                    on_navigate=self.navigate_to,
                )
                self.stack.addWidget(self.signup_screen)

            self.stack.setCurrentWidget(self.signup_screen)

        elif screen_name == "email_verification":
            email = kwargs.get("email", "")

            if self.email_verification_screen is not None:
                self.stack.removeWidget(
                    self.email_verification_screen
                )
                self.email_verification_screen.deleteLater()

            self.email_verification_screen = EmailVerificationScreen(
                email=email,
                on_resend=self._handle_resend_verification,
                on_navigate=self.navigate_to,
            )

            self.stack.addWidget(
                self.email_verification_screen
            )

            self.stack.setCurrentWidget(
                self.email_verification_screen
            )

        elif screen_name == "forgot_password":
            if self.forgot_password_screen is not None:
                self.stack.removeWidget(
                    self.forgot_password_screen
                )
                self.forgot_password_screen.deleteLater()

            self.forgot_password_screen = ForgotPasswordScreen(
                on_navigate=self.navigate_to
            )

            self.stack.addWidget(
                self.forgot_password_screen
            )

            self.stack.setCurrentWidget(
                self.forgot_password_screen
            )

        elif screen_name == "reset_password":
            token = kwargs.get("token", "")

            if self.reset_password_screen is not None:
                self.stack.removeWidget(
                    self.reset_password_screen
                )
                self.reset_password_screen.deleteLater()

            self.reset_password_screen = ResetPasswordScreen(
                token=token,
                on_navigate=self.navigate_to,
            )

            self.stack.addWidget(
                self.reset_password_screen
            )

            self.stack.setCurrentWidget(
                self.reset_password_screen
            )

    def _go_to_email_verification(self, email):
        self.navigate_to(
            "email_verification",
            email=email,
        )

    def _handle_resend_verification(self, email):
        pass