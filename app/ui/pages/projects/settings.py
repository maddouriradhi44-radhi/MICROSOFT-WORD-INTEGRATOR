from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
QWidget,
QVBoxLayout,
QHBoxLayout,
QLabel,
QFrame,
QPushButton,
)

class SettingsScreen(QWidget):


    back_requested = Signal()

    def __init__(self, user=None, parent=None):
        super().__init__(parent)

        self.user = user

        self.setStyleSheet(
            """
            QWidget {
                background-color: #F7F8FA;
            }
            """
        )

        self._build_ui()

    def _build_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        title = QLabel("Settings")
        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 24px;
                font-weight: 700;
            }
            """
        )

        subtitle = QLabel(
            "Manage your account and preferences"
        )
        subtitle.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
            }
            """
        )

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        back_button = QPushButton("Back")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.setFixedHeight(36)

        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                color: #374151;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 0 16px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #F3F4F6;
            }
            """
        )

        back_button.clicked.connect(
            self.back_requested.emit
        )

        header_layout.addWidget(back_button)

        main_layout.addLayout(header_layout)

        # Profile card
        profile_card = QFrame()
        profile_card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            """
        )

        profile_layout = QVBoxLayout()
        profile_layout.setContentsMargins(24, 24, 24, 24)
        profile_layout.setSpacing(16)

        profile_title = QLabel("Profile")
        profile_title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 16px;
                font-weight: 700;
                border: none;
            }
            """
        )

        profile_layout.addWidget(profile_title)

        first_name = ""
        last_name = ""
        email = ""
        role = ""

        if isinstance(self.user, dict):

            first_name = self.user.get("first_name", "")
            last_name = self.user.get("last_name", "")
            email = self.user.get("email", "")
            role = self.user.get("role", "")

        else:

            first_name = getattr(
                self.user,
                "first_name",
                getattr(self.user, "prenom", ""),
            )

            last_name = getattr(
                self.user,
                "last_name",
                getattr(self.user, "nom", ""),
            )

            email = getattr(
                self.user,
                "email",
                "",
            )

            role = getattr(
                self.user,
                "role",
                "",
            )

        if hasattr(role, "value"):
            role = role.value

        self._add_info(
            profile_layout,
            "First name",
            first_name or "Not available",
        )

        self._add_info(
            profile_layout,
            "Last name",
            last_name or "Not available",
        )

        self._add_info(
            profile_layout,
            "Email",
            email or "Not available",
        )

        self._add_info(
            profile_layout,
            "Role",
            role or "Not available",
        )

        profile_card.setLayout(profile_layout)

        main_layout.addWidget(profile_card)

        # Preferences card
        preferences_card = QFrame()
        preferences_card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            """
        )

        preferences_layout = QVBoxLayout()
        preferences_layout.setContentsMargins(24, 24, 24, 24)
        preferences_layout.setSpacing(16)

        preferences_title = QLabel("Preferences")
        preferences_title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 16px;
                font-weight: 700;
                border: none;
            }
            """
        )

        preferences_layout.addWidget(preferences_title)

        notification_row = QHBoxLayout()

        notification_text = QVBoxLayout()
        notification_text.setSpacing(3)

        notification_title = QLabel(
            "Notifications"
        )
        notification_title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 13px;
                font-weight: 600;
                border: none;
            }
            """
        )

        notification_description = QLabel(
            "Receive project and document notifications"
        )
        notification_description.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 11px;
                border: none;
            }
            """
        )

        notification_text.addWidget(notification_title)
        notification_text.addWidget(notification_description)

        notification_row.addLayout(notification_text)
        notification_row.addStretch()

        notification_status = QLabel("Enabled")
        notification_status.setStyleSheet(
            """
            QLabel {
                color: #1C9457;
                font-size: 12px;
                font-weight: 600;
                border: none;
            }
            """
        )

        notification_row.addWidget(notification_status)

        preferences_layout.addLayout(notification_row)

        preferences_card.setLayout(preferences_layout)

        main_layout.addWidget(preferences_card)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def _add_info(self, layout, label, value):

        row = QHBoxLayout()

        label_widget = QLabel(label)
        label_widget.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 12px;
                border: none;
            }
            """
        )

        value_widget = QLabel(value)
        value_widget.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 13px;
                font-weight: 600;
                border: none;
            }
            """
        )

        row.addWidget(label_widget)
        row.addStretch()
        row.addWidget(value_widget)

        layout.addLayout(row)