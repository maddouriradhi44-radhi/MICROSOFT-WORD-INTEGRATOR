from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer

from app.ui.components.auth_widgets import (
    AuthCard,
    wordmark,
    app_name,
    screen_title,
    screen_subtitle,
    GlobalBanner,
    PrimaryButton,
    simple_link,
    TEXT_SECONDARY,
    PRIMARY,
)


RESEND_COOLDOWN_SECONDS = 45


class EmailVerificationScreen(QWidget):
    def __init__(self, email="", on_resend=None, on_navigate=None):
        super().__init__()

        self.email = email
        self.on_resend = on_resend
        self.on_navigate = on_navigate
        self.seconds_left = RESEND_COOLDOWN_SECONDS

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._tick)

        self._build_ui()
        self._start_cooldown()

    def _build_ui(self):
        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignCenter)

        self.card = AuthCard()
        body = self.card.body()

        body.addWidget(wordmark())
        body.addWidget(app_name())
        body.addSpacing(20)

        icon_label = QLabel("✉")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(
            f"font-size: 40px; color: {PRIMARY};"
        )
        body.addWidget(icon_label)
        body.addSpacing(8)

        self.title_label = screen_title(
            "Verify your email address"
        )
        body.addWidget(self.title_label)

        self.subtitle_label = screen_subtitle(
            "We've sent a verification link to your email address."
        )
        body.addWidget(self.subtitle_label)
        body.addSpacing(10)

        self.message_label = QLabel(
            "Please check your inbox and click the verification "
            "link to activate your account."
        )
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet(
            f"color: {TEXT_SECONDARY}; font-size: 12px;"
        )
        body.addWidget(self.message_label)
        body.addSpacing(16)

        self.banner = GlobalBanner()
        body.addWidget(self.banner)

        self.didnt_receive_label = QLabel(
            "Didn't receive the email?"
        )
        self.didnt_receive_label.setAlignment(Qt.AlignCenter)
        self.didnt_receive_label.setStyleSheet(
            f"color: {TEXT_SECONDARY}; font-size: 11px;"
        )
        body.addWidget(self.didnt_receive_label)
        body.addSpacing(6)

        self.resend_btn = PrimaryButton("RESEND EMAIL")
        self.resend_btn.clicked.connect(self._handle_resend)
        body.addWidget(self.resend_btn)
        body.addSpacing(14)

        self.back_link = simple_link("Back to sign in")
        self.back_link.linkActivated.connect(
            lambda: self._navigate("login")
        )
        body.addWidget(self.back_link)

        outer.addWidget(self.card)
        self.setLayout(outer)

    def _navigate(self, screen_name):
        if self.on_navigate:
            self.on_navigate(screen_name)

    def _start_cooldown(self):
        self.seconds_left = RESEND_COOLDOWN_SECONDS
        self.resend_btn.setDisabled(True)
        self._update_cooldown_text()
        self.timer.start()

    def _tick(self):
        self.seconds_left -= 1

        if self.seconds_left <= 0:
            self.timer.stop()
            self.resend_btn.setDisabled(False)
            self.resend_btn.setText("RESEND EMAIL")
        else:
            self._update_cooldown_text()

    def _update_cooldown_text(self):
        self.resend_btn.setText(
            f"Resend available in {self.seconds_left} seconds"
        )

    def _handle_resend(self):
        if self.resend_btn.isEnabled():
            if self.on_resend:
                self.on_resend(self.email)

            self.banner.show_success(
                "Verification email sent again."
            )

            self._start_cooldown()

    def show_verified_success(self):
        self.timer.stop()

        self.title_label.setText(
            "Email verified successfully!"
        )

        self.subtitle_label.setText(
            "Your account has been successfully verified."
        )

        self.message_label.setVisible(False)
        self.didnt_receive_label.setVisible(False)
        self.banner.hide_banner()

        try:
            self.resend_btn.clicked.disconnect(
                self._handle_resend
            )
        except (TypeError, RuntimeError):
            pass

        self.resend_btn.setDisabled(False)
        self.resend_btn.setText("CONTINUE TO SIGN IN")

        self.resend_btn.clicked.connect(
            lambda: self._navigate("login")
        )

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)