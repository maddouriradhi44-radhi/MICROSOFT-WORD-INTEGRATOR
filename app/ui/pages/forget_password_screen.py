from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QThread, Signal

from services.auth_service import auth_service
from services.auth_exceptions import (
    EmptyFieldError,
    InvalidEmailFormatError,
    NetworkError,
    ServerUnavailableError,
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
    simple_link,
    TEXT_SECONDARY,
    SUCCESS,
)


class ForgotPasswordWorker(QThread):
    success = Signal()
    failure = Signal(object)

    def __init__(self, email):
        super().__init__()
        self.email = email

    def run(self):
        try:
            auth_service.forgot_password(self.email)
        except Exception as error:
            self.failure.emit(error)
        else:
            self.success.emit()


class ForgotPasswordScreen(QWidget):

    def __init__(self, on_navigate=None):
        super().__init__()

        self.on_navigate = on_navigate
        self.worker = None

        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignCenter)

        self.card = AuthCard()
        self.body = self.card.body()

        self._build_request_form()

        outer.addWidget(self.card)
        self.setLayout(outer)

    def _build_request_form(self):
        self.body.addWidget(wordmark())
        self.body.addWidget(app_name())
        self.body.addSpacing(18)

        self.body.addWidget(
            screen_title("Forgot your password?")
        )

        self.body.addWidget(
            screen_subtitle(
                "No worries. Enter your email address and "
                "we'll send you a password reset link."
            )
        )

        self.body.addSpacing(16)

        self.banner = GlobalBanner()
        self.body.addWidget(self.banner)

        self.email_field = IconField(
            "Email",
            "your.email@example.com",
            "fa5s.envelope",
        )
        self.body.addWidget(self.email_field)

        self.body.addSpacing(16)

        self.submit_btn = PrimaryButton("SEND RESET LINK")
        self.submit_btn.clicked.connect(self.handle_submit)
        self.body.addWidget(self.submit_btn)

        self.body.addSpacing(14)

        self.back_link = simple_link("Back to sign in")
        self.back_link.linkActivated.connect(
            lambda: self._navigate("login")
        )
        self.body.addWidget(self.back_link)

        self.email_field.input.returnPressed.connect(
            self.handle_submit
        )

        self.email_field.input.setFocus()

    def _navigate(self, screen_name):
        if self.on_navigate:
            self.on_navigate(screen_name)

    def handle_submit(self):
        if self.worker is not None and self.worker.isRunning():
            return

        email = self.email_field.text()

        self.banner.hide_banner()
        self.email_field.clear_error()

        if not email:
            self.email_field.set_error(
                "Please enter your email address."
            )
            return

        self._set_loading(True)

        self.worker = ForgotPasswordWorker(email)

        self.worker.success.connect(
            self._handle_success
        )

        self.worker.failure.connect(
            self._handle_failure
        )

        self.worker.start()

    def _set_loading(self, is_loading):
        self.submit_btn.set_loading(
            is_loading,
            "Sending...",
        )

        self.email_field.set_disabled(
            is_loading
        )

    def _handle_failure(self, error):
        self._set_loading(False)

        if isinstance(error, InvalidEmailFormatError):
            self.email_field.set_error(
                str(error)
            )

        elif isinstance(error, EmptyFieldError):
            self.email_field.set_error(
                str(error)
            )

        elif isinstance(
            error,
            (NetworkError, ServerUnavailableError),
        ):
            self.banner.show_error(
                "Unable to contact the server. "
                "Please try again."
            )

        else:
            self.banner.show_error(
                "Something went wrong. "
                "Please try again."
            )

    def _handle_success(self):
        self._set_loading(False)
        self._show_success_state()

    def _show_success_state(self):
        while self.body.count():
            item = self.body.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.body.addWidget(wordmark())
        self.body.addWidget(app_name())
        self.body.addSpacing(20)

        icon_label = QLabel("✓")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(
            f"font-size: 36px;"
            f"color: {SUCCESS};"
            f"font-weight: 700;"
        )

        self.body.addWidget(icon_label)
        self.body.addSpacing(6)

        self.body.addWidget(
            screen_title("Check your email")
        )

        self.body.addWidget(
            screen_subtitle(
                "If an account exists with this email address, "
                "we've sent you a password reset link."
            )
        )

        self.body.addSpacing(6)

        secondary_message = QLabel(
            "Please check your inbox and follow the "
            "instructions to reset your password."
        )

        secondary_message.setWordWrap(True)
        secondary_message.setAlignment(Qt.AlignCenter)
        secondary_message.setStyleSheet(
            f"color: {TEXT_SECONDARY};"
            f"font-size: 12px;"
        )

        self.body.addWidget(
            secondary_message
        )

        self.body.addSpacing(16)

        back_btn = PrimaryButton("BACK TO SIGN IN")
        back_btn.clicked.connect(
            lambda: self._navigate("login")
        )

        self.body.addWidget(back_btn)

    def closeEvent(self, event):
        if self.worker is not None and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()

        super().closeEvent(event)