from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import qtawesome as qta


PRIMARY = "#0070AD"
PRIMARY_DARK = "#001D5C"
PRIMARY_HOVER = "#005E92"
PRIMARY_PRESSED = "#004A75"
BG_WINDOW = "#F5F7FA"
CARD_BG = "#FFFFFF"
BORDER = "#D9E2EC"
TEXT = "#1A1A1A"
TEXT_SECONDARY = "#6B7280"
ERROR = "#C0392B"
ERROR_BG = "#FBEAE8"
SUCCESS = "#1E8E5A"
SUCCESS_BG = "#E7F6EF"

LABEL_STYLE = f"""
color: {TEXT};
font-size: 12px;
font-weight: 600;
"""


class AuthCard(QFrame):
    def __init__(self, width=380):
        super().__init__()

        self.setFixedWidth(width)
        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {CARD_BG};
                border-radius: 16px;
            }}
            """
        )

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 6)
        self.setGraphicsEffect(shadow)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(32, 28, 32, 28)
        self._layout.setSpacing(5)

        self.setLayout(self._layout)

    def body(self):
        return self._layout


def wordmark():
    label = QLabel("CAPGEMINI")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet(
        f"""
        color: {PRIMARY_DARK};
        font-size: 16px;
        font-weight: 800;
        letter-spacing: 2px;
        """
    )
    return label


def app_name():
    label = QLabel("Microsoft Word Integrator")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet(
        f"""
        color: {TEXT_SECONDARY};
        font-size: 12px;
        font-weight: 500;
        """
    )
    return label


def screen_title(text):
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    label.setWordWrap(True)
    label.setStyleSheet(
        f"""
        color: {TEXT};
        font-size: 21px;
        font-weight: 700;
        """
    )
    return label


def screen_subtitle(text):
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    label.setWordWrap(True)
    label.setStyleSheet(
        f"""
        color: {TEXT_SECONDARY};
        font-size: 12px;
        """
    )
    return label


class GlobalBanner(QLabel):
    def __init__(self):
        super().__init__("")

        self.setWordWrap(True)
        self.setAlignment(Qt.AlignCenter)
        self.setVisible(False)

    def show_error(self, message):
        self.setText(message)
        self.setStyleSheet(
            f"""
            background-color: {ERROR_BG};
            color: {ERROR};
            font-size: 11px;
            border-radius: 8px;
            padding: 8px;
            """
        )
        self.setVisible(True)

    def show_success(self, message):
        self.setText(message)
        self.setStyleSheet(
            f"""
            background-color: {SUCCESS_BG};
            color: {SUCCESS};
            font-size: 11px;
            border-radius: 8px;
            padding: 8px;
            """
        )
        self.setVisible(True)

    def hide_banner(self):
        self.setVisible(False)
        self.setText("")


class IconField(QWidget):
    def __init__(
        self,
        label_text,
        placeholder,
        icon_name,
        is_password=False,
    ):
        super().__init__()

        self.is_password = is_password
        self.password_visible = False

        outer = QVBoxLayout()
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(4)

        label = QLabel(label_text)
        label.setStyleSheet(LABEL_STYLE)
        outer.addWidget(label)

        self.row = QFrame()
        self.row.setFixedHeight(48)

        self._set_border(BORDER)

        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(12, 4, 12, 4)
        row_layout.setSpacing(8)

        left_icon = QLabel()
        left_icon.setFixedSize(17, 17)
        left_icon.setAlignment(Qt.AlignCenter)
        left_icon.setPixmap(
            qta.icon(
                icon_name,
                color=TEXT_SECONDARY,
            ).pixmap(15, 15)
        )

        row_layout.addWidget(
            left_icon,
            alignment=Qt.AlignVCenter,
        )

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setMinimumHeight(30)
        self.input.setMaximumHeight(34)

        self.input.setStyleSheet(
            f"""
            QLineEdit {{
                border: none;
                background: transparent;
                color: {TEXT};
                font-size: 14px;
                padding: 0px;
                margin: 0px;
            }}
            """
        )

        if is_password:
            self.input.setEchoMode(QLineEdit.Password)
        else:
            self.input.setEchoMode(QLineEdit.Normal)

        row_layout.addWidget(
            self.input,
            1,
            alignment=Qt.AlignVCenter,
        )

        self.input.focusInEvent = self._wrap_focus(
            self.input.focusInEvent,
            True,
        )

        self.input.focusOutEvent = self._wrap_focus(
            self.input.focusOutEvent,
            False,
        )

        self.input.textChanged.connect(
            self.clear_error
        )

        if is_password:
            self.toggle_btn = QPushButton()

            self.toggle_btn.setIcon(
                qta.icon(
                    "fa5s.eye",
                    color=TEXT_SECONDARY,
                )
            )

            self.toggle_btn.setFixedSize(24, 24)
            self.toggle_btn.setCursor(
                Qt.PointingHandCursor
            )

            self.toggle_btn.setStyleSheet(
                """
                QPushButton {
                    border: none;
                    background: transparent;
                    padding: 0px;
                    margin: 0px;
                }
                """
            )

            self.toggle_btn.clicked.connect(
                self._toggle_visibility
            )

            row_layout.addWidget(
                self.toggle_btn,
                alignment=Qt.AlignVCenter,
            )

        self.row.setLayout(row_layout)
        outer.addWidget(self.row)

        self.error_label = QLabel("")
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet(
            f"""
            color: {ERROR};
            font-size: 10px;
            """
        )
        self.error_label.setVisible(False)

        outer.addWidget(self.error_label)

        self.setLayout(outer)

    def _toggle_visibility(self):
        self.password_visible = not self.password_visible

        if self.password_visible:
            self.input.setEchoMode(QLineEdit.Normal)
            self.toggle_btn.setIcon(
                qta.icon(
                    "fa5s.eye-slash",
                    color=PRIMARY,
                )
            )
        else:
            self.input.setEchoMode(QLineEdit.Password)
            self.toggle_btn.setIcon(
                qta.icon(
                    "fa5s.eye",
                    color=TEXT_SECONDARY,
                )
            )

    def _wrap_focus(self, original_handler, focused):
        def handler(event):
            original_handler(event)
            self._set_border(
                PRIMARY if focused else BORDER
            )

        return handler

    def _set_border(self, color):
        self.row.setStyleSheet(
            f"""
            QFrame {{
                background-color: {CARD_BG};
                border: 1.5px solid {color};
                border-radius: 10px;
            }}
            """
        )

    def set_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)
        self._set_border(ERROR)

    def clear_error(self):
        self.error_label.setVisible(False)
        self.error_label.setText("")
        self._set_border(BORDER)

    def text(self):
        if self.is_password:
            return self.input.text()

        return self.input.text().strip()

    def set_disabled(self, disabled):
        self.input.setDisabled(disabled)

        if self.is_password:
            self.toggle_btn.setDisabled(disabled)


class PrimaryButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

        self._default_text = text

        self.setFixedHeight(46)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                font-size: 13px;
                font-weight: 700;
                border: none;
                border-radius: 10px;
            }}

            QPushButton:hover {{
                background-color: {PRIMARY_HOVER};
            }}

            QPushButton:pressed {{
                background-color: {PRIMARY_PRESSED};
            }}

            QPushButton:disabled {{
                background-color: #9FC7DE;
                color: #F0F0F0;
            }}
            """
        )

    def set_loading(self, is_loading, loading_text):
        self.setDisabled(is_loading)

        self.setText(
            loading_text
            if is_loading
            else self._default_text
        )


def link_label(prefix_text, link_text):
    label = QLabel(
        f'<span style="color: {TEXT_SECONDARY};">'
        f'{prefix_text} '
        f'</span>'
        f'<a href="#" style="color: {PRIMARY};">'
        f'{link_text}'
        f'</a>'
    )

    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet(
        "font-size: 12px;"
    )

    return label


def simple_link(text):
    label = QLabel(
        f'<a href="#" style="color: {PRIMARY};">'
        f'{text}'
        f'</a>'
    )

    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet(
        "font-size: 12px;"
    )

    return label


class PasswordRequirementsList(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(2)

        self.requirements = {
            "length": QLabel("• At least 8 characters"),
            "uppercase": QLabel("• One uppercase letter"),
            "lowercase": QLabel("• One lowercase letter"),
            "digit": QLabel("• One number"),
            "special": QLabel("• One special character"),
        }

        for label in self.requirements.values():
            label.setStyleSheet(
                f"""
                color: {TEXT_SECONDARY};
                font-size: 10px;
                """
            )
            layout.addWidget(label)

        self.setLayout(layout)

    def update_status(self, password):
        checks = {
            "length": len(password) >= 8,
            "uppercase": any(c.isupper() for c in password),
            "lowercase": any(c.islower() for c in password),
            "digit": any(c.isdigit() for c in password),
            "special": any(
                not c.isalnum()
                for c in password
            ),
        }

        for key, valid in checks.items():
            label = self.requirements[key]

            if valid:
                label.setStyleSheet(
                    f"""
                    color: {SUCCESS};
                    font-size: 10px;
                    """
                )
            else:
                label.setStyleSheet(
                    f"""
                    color: {TEXT_SECONDARY};
                    font-size: 10px;
                    """
                )