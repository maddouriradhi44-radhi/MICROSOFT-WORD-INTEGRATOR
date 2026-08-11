from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QThread, Signal

from app.ui.services.auth_service import auth_service
from app.ui.services.auth_exceptions import (
    EmptyFieldError,
    InvalidEmailFormatError,
    PasswordMismatchError,
    WeakPasswordError,
    EmailAlreadyRegisteredError,
    ServerUnavailableError,
    NetworkError,
)

from app.ui.components.auth_widgets import (
    AuthCard,
    wordmark,
    app_name,
    screen_title,
    screen_subtitle,
    GlobalBanner,
    IconField,
    PrimaryButton,
    link_label,
)


class SignUpWorker(QThread):
    success = Signal(object)
    failure = Signal(object)

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password,
        confirm_password,
    ):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

    def run(self):
        try:
            result = auth_service.register(
                self.first_name,
                self.last_name,
                self.email,
                self.password,
                self.confirm_password,
            )
        except Exception as error:
            self.failure.emit(error)
        else:
            self.success.emit(result)


class SignUpScreen(QWidget):

    def __init__(
        self,
        on_success=None,
        on_navigate=None,
    ):
        super().__init__()

        self.on_success = on_success
        self.on_navigate = on_navigate
        self.worker = None

        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignCenter)

        card = AuthCard(width=400)
        body = card.body()

        body.addWidget(wordmark())
        body.addWidget(app_name())
        body.addSpacing(16)

        body.addWidget(
            screen_title("Create your account")
        )

        body.addWidget(
            screen_subtitle(
                "Join the collaborative document platform"
            )
        )

        body.addSpacing(14)

        self.banner = GlobalBanner()
        body.addWidget(self.banner)

        self.first_name_field = IconField(
            "First name",
            "Enter your first name",
            "fa5s.user",
        )

        body.addWidget(self.first_name_field)
        body.addSpacing(8)

        self.last_name_field = IconField(
            "Last name",
            "Enter your last name",
            "fa5s.user",
        )

        body.addWidget(self.last_name_field)
        body.addSpacing(8)

        self.email_field = IconField(
            "Professional email",
            "your.email@capgemini.com",
            "fa5s.envelope",
        )

        body.addWidget(self.email_field)
        body.addSpacing(8)

        self.password_field = IconField(
            "Password",
            "Create a password",
            "fa5s.lock",
            is_password=True,
        )

        body.addWidget(self.password_field)
        body.addSpacing(8)

        self.confirm_password_field = IconField(
            "Confirm password",
            "Confirm your password",
            "fa5s.lock",
            is_password=True,
        )

        body.addWidget(self.confirm_password_field)
        body.addSpacing(16)

        self.submit_btn = PrimaryButton(
            "CREATE ACCOUNT"
        )

        self.submit_btn.clicked.connect(
            self.handle_register
        )

        body.addWidget(self.submit_btn)
        body.addSpacing(14)

        login_link = link_label(
            "Already have an account?",
            "Sign in",
        )

        login_link.linkActivated.connect(
            lambda: self._navigate("login")
        )

        body.addWidget(login_link)

        outer.addWidget(card)
        self.setLayout(outer)

        self.confirm_password_field.input.returnPressed.connect(
            self.handle_register
        )

        self.first_name_field.input.setFocus()

    def _navigate(self, screen_name):
        if self.on_navigate:
            self.on_navigate(screen_name)

    def handle_register(self):
        if (
            self.worker is not None
            and self.worker.isRunning()
        ):
            return

        first_name = self.first_name_field.text()
        last_name = self.last_name_field.text()
        email = self.email_field.text()
        password = self.password_field.text()
        confirm_password = (
            self.confirm_password_field.text()
        )

        self.banner.hide_banner()

        fields = (
            self.first_name_field,
            self.last_name_field,
            self.email_field,
            self.password_field,
            self.confirm_password_field,
        )

        for field in fields:
            field.clear_error()

        has_error = False

        if not first_name:
            self.first_name_field.set_error(
                "First name is required."
            )
            has_error = True

        if not last_name:
            self.last_name_field.set_error(
                "Last name is required."
            )
            has_error = True

        if not email:
            self.email_field.set_error(
                "Email is required."
            )
            has_error = True

        if not password:
            self.password_field.set_error(
                "Password is required."
            )
            has_error = True

        if not confirm_password:
            self.confirm_password_field.set_error(
                "Please confirm your password."
            )
            has_error = True

        if has_error:
            return

        self._set_loading(True)

        self.worker = SignUpWorker(
            first_name,
            last_name,
            email,
            password,
            confirm_password,
        )

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
            "Creating account...",
        )

        fields = (
            self.first_name_field,
            self.last_name_field,
            self.email_field,
            self.password_field,
            self.confirm_password_field,
        )

        for field in fields:
            field.set_disabled(is_loading)

    def _handle_success(self, result):
        self._set_loading(False)

        self.banner.show_success(
            "Account created successfully!"
        )

        if self.on_success:
            self.on_success(
                self.email_field.text()
            )

    def _handle_failure(self, error):
        self._set_loading(False)

        if isinstance(
            error,
            InvalidEmailFormatError,
        ):
            self.email_field.set_error(
                str(error)
            )

        elif isinstance(
            error,
            PasswordMismatchError,
        ):
            self.confirm_password_field.set_error(
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
            EmailAlreadyRegisteredError,
        ):
            self.email_field.set_error(
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