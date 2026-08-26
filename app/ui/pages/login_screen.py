from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QThread, Signal

from services.auth_service import auth_service
from services.auth_exceptions import (
    EmptyFieldError,
    InvalidEmailFormatError,
    InvalidCredentialsError,
    EmailNotVerifiedError,
    ServerUnavailableError,
    NetworkError,
)

from components.auth_widgets import (
    AuthCard,
    wordmark,
    app_name,
    screen_title,
    screen_subtitle,
    GlobalBanner,
    IconField,
    PrimaryButton,
    link_label,
    simple_link,
)


class LoginWorker(QThread):
    success = Signal(object)
    failure = Signal(object)

    def __init__(self, email, password):
        super().__init__()
        self.email = email
        self.password = password

    def run(self):
        try:
            result = auth_service.login(
                self.email,
                self.password,
            )
        except Exception as error:
            self.failure.emit(error)
        else:
            self.success.emit(result)


class LoginScreen(QWidget):

    def __init__(self, on_success=None, on_navigate=None):
        super().__init__()

        self.on_success = on_success
        self.on_navigate = on_navigate
        self.worker = None

        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignCenter)

        card = AuthCard()
        body = card.body()

        body.addWidget(wordmark())
        body.addWidget(app_name())
        body.addSpacing(18)

        body.addWidget(
            screen_title("Welcome back")
        )

        body.addWidget(
            screen_subtitle("Sign in to your account")
        )

        body.addSpacing(16)

        self.banner = GlobalBanner()
        body.addWidget(self.banner)

        self.email_field = IconField(
            "Email",
            "your.email@example.com",
            "fa5s.envelope",
        )

        body.addWidget(self.email_field)
        body.addSpacing(8)

        self.password_field = IconField(
            "Password",
            "Enter your password",
            "fa5s.lock",
            is_password=True,
        )

        body.addWidget(self.password_field)

        forgot_row = QHBoxLayout()
        forgot_row.addStretch()

        forgot_link = simple_link(
            "Forgot your password?"
        )

        forgot_link.linkActivated.connect(
            lambda: self._navigate("forgot_password")
        )

        forgot_row.addWidget(forgot_link)
        body.addLayout(forgot_row)

        body.addSpacing(16)

        self.submit_btn = PrimaryButton("SIGN IN")
        self.submit_btn.clicked.connect(
            self.handle_login
        )

        body.addWidget(self.submit_btn)
        body.addSpacing(14)

        signup_link = link_label(
            "Don't have an account?",
            "Sign up",
        )

        signup_link.linkActivated.connect(
            lambda: self._navigate("signup")
        )

        body.addWidget(signup_link)

        outer.addWidget(card)
        self.setLayout(outer)

        self.email_field.input.returnPressed.connect(
            self.handle_login
        )

        self.password_field.input.returnPressed.connect(
            self.handle_login
        )

        self.email_field.input.setFocus()

    def _navigate(self, screen_name):
        if self.on_navigate:
            self.on_navigate(screen_name)

    def handle_login(self):
        if self.worker is not None and self.worker.isRunning():
            return

        email = self.email_field.text()
        password = self.password_field.text()

        self.banner.hide_banner()
        self.email_field.clear_error()
        self.password_field.clear_error()

        has_error = False

        if not email:
            self.email_field.set_error(
                "Please enter your email address."
            )
            has_error = True

        if not password:
            self.password_field.set_error(
                "Please enter your password."
            )
            has_error = True

        if has_error:
            return

        self._set_loading(True)

        self.worker = LoginWorker(
            email,
            password,
        )

        self.worker.success.connect(
            self._handle_success
        )

        self.worker.failure.connect(
            self._handle_failure
        )

        self.worker.finished.connect(
            self._cleanup_worker
        )

        self.worker.start()

    def _set_loading(self, is_loading):
        self.submit_btn.set_loading(
            is_loading,
            "Signing in...",
        )

        self.email_field.set_disabled(
            is_loading
        )

        self.password_field.set_disabled(
            is_loading
        )

    def _handle_success(self, result):
        self._set_loading(False)

        self.banner.show_success(
            "Login successful!"
        )

        if self.on_success:
            self.on_success(result)

    def _handle_failure(self, error):
        self._set_loading(False)

        self.email_field.clear_error()
        self.password_field.clear_error()

        if isinstance(error, EmptyFieldError):
            self.banner.show_error(
                str(error)
            )

        elif isinstance(error, InvalidEmailFormatError):
            self.email_field.set_error(
                str(error)
            )

        elif isinstance(error, InvalidCredentialsError):
            self.banner.show_error(
                "Incorrect email or password."
            )

        elif isinstance(error, EmailNotVerifiedError):
            self.banner.show_error(
                str(error)
            )

        elif isinstance(
            error,
            (
                ServerUnavailableError,
                NetworkError,
            ),
        ):
            self.banner.show_error(
                str(error)
            )

        else:
            self.banner.show_error(
                "Something went wrong. Please try again."
            )

    def _cleanup_worker(self):
        if self.worker is not None:
            self.worker.deleteLater()
            self.worker = None