from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QThread, Signal

from services.auth_service import auth_service
from services.auth_exceptions import (
    EmptyFieldError,
    PasswordMismatchError,
    WeakPasswordError,
    InvalidTokenError,
    ExpiredTokenError,
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
    PasswordRequirementsList,
    simple_link,
    TEXT_SECONDARY,
    SUCCESS,
)


class TokenCheckWorker(QThread):
    valid = Signal()
    invalid = Signal(object)

    def __init__(self, token):
        super().__init__()
        self.token = token

    def run(self):
        try:
            auth_service.check_reset_token(self.token)
        except Exception as error:
            self.invalid.emit(error)
        else:
            self.valid.emit()


class ResetSubmitWorker(QThread):
    success = Signal()
    failure = Signal(object)

    def __init__(self, token, new_password, confirm_password):
        super().__init__()
        self.token = token
        self.new_password = new_password
        self.confirm_password = confirm_password

    def run(self):
        try:
            auth_service.reset_password(
                self.token,
                self.new_password,
                self.confirm_password,
            )
        except Exception as error:
            self.failure.emit(error)
        else:
            self.success.emit()


class ResetPasswordScreen(QWidget):

    def __init__(self, token="", on_navigate=None):
        super().__init__()

        self.token = token
        self.on_navigate = on_navigate
        self.token_worker = None
        self.submit_worker = None

        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignCenter)

        self.card = AuthCard()
        self.body = self.card.body()

        outer.addWidget(self.card)
        self.setLayout(outer)

        self._check_token()

    def _navigate(self, screen_name):
        if self.on_navigate:
            self.on_navigate(screen_name)

    def _clear_body(self):
        while self.body.count():
            item = self.body.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

    def _check_token(self):
        self._clear_body()

        self.body.addWidget(wordmark())
        self.body.addWidget(app_name())
        self.body.addSpacing(20)

        loading_label = QLabel(
            "Checking your reset link..."
        )
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet(
            f"color: {TEXT_SECONDARY};"
            f"font-size: 12px;"
        )

        self.body.addWidget(loading_label)

        self.token_worker = TokenCheckWorker(self.token)
        self.token_worker.valid.connect(
            self._show_reset_form
        )
        self.token_worker.invalid.connect(
            self._show_token_error
        )
        self.token_worker.start()

    def _show_token_error(self, error):
        self._clear_body()

        self.body.addWidget(wordmark())
        self.body.addWidget(app_name())
        self.body.addSpacing(20)

        if isinstance(error, ExpiredTokenError):
            title = "Reset link expired"
            message = (
                "This password reset link has expired. "
                "Please request a new one."
            )
        else:
            title = "Invalid reset link"
            message = (
                "This password reset link is invalid "
                "or no longer available."
            )

        self.body.addWidget(
            screen_title(title)
        )

        self.body.addWidget(
            screen_subtitle(message)
        )

        self.body.addSpacing(16)

        request_btn = PrimaryButton(
            "REQUEST A NEW LINK"
        )
        request_btn.clicked.connect(
            lambda: self._navigate("forgot_password")
        )

        self.body.addWidget(request_btn)
        self.body.addSpacing(14)

        back_link = simple_link(
            "Back to sign in"
        )
        back_link.linkActivated.connect(
            lambda: self._navigate("login")
        )

        self.body.addWidget(back_link)

    def _show_reset_form(self):
        self._clear_body()

        self.body.addWidget(wordmark())
        self.body.addWidget(app_name())
        self.body.addSpacing(16)

        self.body.addWidget(
            screen_title("Create a new password")
        )

        self.body.addWidget(
            screen_subtitle(
                "Choose a strong password for your account."
            )
        )

        self.body.addSpacing(14)

        self.banner = GlobalBanner()
        self.body.addWidget(self.banner)

        self.password_field = IconField(
            "New password",
            "Enter your new password",
            "fa5s.lock",
            is_password=True,
        )

        self.body.addWidget(
            self.password_field
        )

        self.body.addSpacing(4)

        self.requirements_list = PasswordRequirementsList()
        self.body.addWidget(
            self.requirements_list
        )

        self.password_field.input.textChanged.connect(
            self._update_requirements
        )

        self.body.addSpacing(6)

        self.confirm_field = IconField(
            "Confirm new password",
            "Confirm your new password",
            "fa5s.lock",
            is_password=True,
        )

        self.body.addWidget(
            self.confirm_field
        )

        self.body.addSpacing(16)

        self.submit_btn = PrimaryButton(
            "RESET PASSWORD"
        )

        self.submit_btn.clicked.connect(
            self.handle_submit
        )

        self.body.addWidget(
            self.submit_btn
        )

        self.body.addSpacing(14)

        back_link = simple_link(
            "Back to sign in"
        )

        back_link.linkActivated.connect(
            lambda: self._navigate("login")
        )

        self.body.addWidget(back_link)

        self.confirm_field.input.returnPressed.connect(
            self.handle_submit
        )

        self.password_field.input.setFocus()

    def _update_requirements(self, password):
        self.requirements_list.update_status(
            password
        )

    def handle_submit(self):
        if (
            self.submit_worker is not None
            and self.submit_worker.isRunning()
        ):
            return

        new_password = self.password_field.text()
        confirm_password = self.confirm_field.text()

        self.banner.hide_banner()
        self.password_field.clear_error()
        self.confirm_field.clear_error()

        if not new_password:
            self.password_field.set_error(
                "Please enter your new password."
            )
            return

        if not confirm_password:
            self.confirm_field.set_error(
                "Please confirm your new password."
            )
            return

        self._set_loading(True)

        self.submit_worker = ResetSubmitWorker(
            self.token,
            new_password,
            confirm_password,
        )

        self.submit_worker.success.connect(
            self._handle_success
        )

        self.submit_worker.failure.connect(
            self._handle_failure
        )

        self.submit_worker.start()

    def _set_loading(self, is_loading):
        self.submit_btn.set_loading(
            is_loading,
            "Resetting password...",
        )

        self.password_field.set_disabled(
            is_loading
        )

        self.confirm_field.set_disabled(
            is_loading
        )

    def _handle_failure(self, error):
        self._set_loading(False)

        if isinstance(
            error,
            PasswordMismatchError,
        ):
            self.confirm_field.set_error(
                str(error)
            )

        elif isinstance(
            error,
            WeakPasswordError,
        ):
            self.password_field.set_error(
                str(error)
            )

        elif isinstance(
            error,
            EmptyFieldError,
        ):
            self.banner.show_error(
                str(error)
            )

        elif isinstance(
            error,
            (InvalidTokenError, ExpiredTokenError),
        ):
            self._show_token_error(error)

        elif isinstance(
            error,
            (ServerUnavailableError, NetworkError),
        ):
            self.banner.show_error(
                "Something went wrong. "
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
        self._clear_body()

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
            screen_title(
                "Password reset successfully"
            )
        )

        self.body.addWidget(
            screen_subtitle(
                "Your password has been changed successfully. "
                "You can now sign in with your new password."
            )
        )

        self.body.addSpacing(16)

        back_btn = PrimaryButton(
            "BACK TO SIGN IN"
        )

        back_btn.clicked.connect(
            lambda: self._navigate("login")
        )

        self.body.addWidget(
            back_btn
        )

    def closeEvent(self, event):
        if (
            self.token_worker is not None
            and self.token_worker.isRunning()
        ):
            self.token_worker.quit()
            self.token_worker.wait()

        if (
            self.submit_worker is not None
            and self.submit_worker.isRunning()
        ):
            self.submit_worker.quit()
            self.submit_worker.wait()

        super().closeEvent(event)