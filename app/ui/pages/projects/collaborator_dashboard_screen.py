from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
)

from app.ui.services.notification_service import notification_service


class DashboardHeader(QFrame):

    notifications_clicked = Signal()
    logout_clicked = Signal()

    def __init__(self, project, user=None, parent=None):
        super().__init__(parent)

        self.project = project
        self.user = user

        self.setFixedHeight(70)

        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-bottom: 1px solid #E5E7EB;
            }
            """
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(12)

        # Project name
        project_label = QLabel(project.name)
        project_label.setStyleSheet(
            """
            color: #14171F;
            font-size: 16px;
            font-weight: 700;
            border: none;
            """
        )

        layout.addWidget(project_label)

        # Project status
        status_label = QLabel(project.status)
        status_label.setStyleSheet(
            """
            color: #1C9457;
            font-size: 12px;
            font-weight: 600;
            border: none;
            """
        )

        layout.addWidget(status_label)

        layout.addStretch()

        # Notification button
        notification_button = QPushButton("🔔")
        notification_button.setFixedSize(36, 36)
        notification_button.setCursor(Qt.PointingHandCursor)

        notification_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                background-color: transparent;
                font-size: 17px;
            }

            QPushButton:hover {
                background-color: #F3F4F6;
                border-radius: 18px;
            }
            """
        )

        notification_button.clicked.connect(
            self.notifications_clicked.emit
        )

        self.notification_button = notification_button

        layout.addWidget(notification_button)

        # Notification unread badge
        self.notification_badge = QLabel("0")
        self.notification_badge.setAlignment(Qt.AlignCenter)
        self.notification_badge.setFixedSize(18, 18)

        self.notification_badge.setStyleSheet(
            """
            QLabel {
                background-color: #D92D20;
                color: white;
                border-radius: 9px;
                font-size: 10px;
                font-weight: 700;
                border: none;
            }
            """
        )

        self.notification_badge.hide()

        layout.addWidget(self.notification_badge)

        # User information
        first_name = ""
        last_name = ""

        if isinstance(user, dict):
            first_name = user.get("first_name", "")
            last_name = user.get("last_name", "")

        full_name = f"{first_name} {last_name}".strip()

        if not full_name:
            full_name = "User"

        user_layout = QVBoxLayout()
        user_layout.setSpacing(0)

        name_label = QLabel(full_name)
        name_label.setAlignment(Qt.AlignRight)
        name_label.setStyleSheet(
            """
            color: #14171F;
            font-size: 13px;
            font-weight: 700;
            border: none;
            """
        )

        role_label = QLabel("COLLABORATOR")
        role_label.setAlignment(Qt.AlignRight)
        role_label.setStyleSheet(
            """
            color: #8A94A6;
            font-size: 10px;
            font-weight: 600;
            border: none;
            """
        )

        user_layout.addWidget(name_label)
        user_layout.addWidget(role_label)

        layout.addLayout(user_layout)

        # Avatar
        initials = "".join(
            part[0]
            for part in full_name.split()
            if part
        )[:2].upper()

        avatar = QLabel(initials)
        avatar.setFixedSize(38, 38)
        avatar.setAlignment(Qt.AlignCenter)

        avatar.setStyleSheet(
            """
            QLabel {
                background-color: #E8F0FE;
                color: #3E63DD;
                border-radius: 19px;
                font-size: 13px;
                font-weight: 700;
                border: none;
            }
            """
        )

        layout.addWidget(avatar)

        self.setLayout(layout)

        # Load unread notifications count
        self._load_unread_count()

    def _load_unread_count(self):
        try:
            count = notification_service.get_unread_count()

            if count > 0:
                self.notification_badge.setText(str(count))
                self.notification_badge.show()
            else:
                self.notification_badge.hide()

        except Exception:
            self.notification_badge.hide()
    def refresh_unread_count(self):
        self._load_unread_count()


class CollaboratorDashboardScreen(QWidget):

    section_open_requested = Signal(str)
    nav_requested = Signal(str)
    logout_requested = Signal()
    settings_requested = Signal()

    def __init__(self, project, user=None, parent=None):
        super().__init__(parent)

        self.project = project
        self.user = user

        self.setStyleSheet(
            """
            QWidget {
                background-color: #F7F8FA;
            }
            """
        )

        self._build_ui()

        self.header.notifications_clicked.connect(
            lambda: self._handle_navigation("notifications")
        )

    def _build_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(220)

        self.sidebar.setStyleSheet(
            """
            QFrame {
                background-color: #0B1B3B;
            }
            """
        )

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 24, 20, 24)
        sidebar_layout.setSpacing(10)

        title = QLabel("CAPGEMINI")
        title.setStyleSheet(
            """
            color: white;
            font-size: 16px;
            font-weight: 700;
            """
        )

        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(24)

        self._build_sidebar_navigation(sidebar_layout)

        self.sidebar.setLayout(sidebar_layout)

        self.content = QFrame()
        self.content.setStyleSheet(
            """
            QFrame {
                background-color: #F7F8FA;
            }
            """
        )

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.header = DashboardHeader(
            project=self.project,
            user=self.user,
        )

        content_layout.addWidget(self.header)

        body = QFrame()
        body.setStyleSheet(
            """
            QFrame {
                background-color: #F7F8FA;
                border: none;
            }
            """
        )

        body_layout = QVBoxLayout()
        body_layout.setContentsMargins(30, 30, 30, 30)

        project_name = QLabel(self.project.name)
        project_name.setStyleSheet(
            """
            color: #14171F;
            font-size: 24px;
            font-weight: 700;
            border: none;
            """
        )

        welcome = QLabel("Welcome back")
        welcome.setStyleSheet(
            """
            color: #6B7280;
            font-size: 14px;
            border: none;
            """
        )

        body_layout.addWidget(welcome)
        body_layout.addWidget(project_name)
        body_layout.addStretch()

        body.setLayout(body_layout)

        content_layout.addWidget(body, 1)

        self.content.setLayout(content_layout)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content, 1)

        self.setLayout(main_layout)

    def _build_sidebar_navigation(self, layout):
        navigation_items = [
            ("dashboard", "Dashboard"),
            ("sections", "My Sections"),
            ("document", "Document"),
            ("notifications", "Notifications"),
        ]

        self.nav_buttons = {}

        for key, label in navigation_items:
            button = QPushButton(label)
            button.setCursor(Qt.PointingHandCursor)
            button.setCheckable(True)

            button.setStyleSheet(
                """
                QPushButton {
                    text-align: left;
                    padding: 10px 12px;
                    border: none;
                    border-radius: 8px;
                    background-color: transparent;
                    color: #C6CCDA;
                    font-size: 13px;
                }

                QPushButton:hover {
                    background-color: #142A57;
                    color: white;
                }

                QPushButton:checked {
                    background-color: #1E4FD6;
                    color: white;
                    font-weight: 600;
                }
                """
            )

            button.clicked.connect(
                lambda checked=False, key=key:
                self._handle_navigation(key)
            )

            self.nav_buttons[key] = button
            layout.addWidget(button)

        layout.addStretch()

        settings_button = QPushButton("Settings")
        settings_button.setCursor(Qt.PointingHandCursor)

        settings_button.setStyleSheet(
            """
            QPushButton {
                text-align: left;
                padding: 10px 12px;
                border: none;
                border-radius: 8px;
                color: #C6CCDA;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #142A57;
                color: white;
            }
            """
        )

        settings_button.clicked.connect(
            self.settings_requested.emit
        )

        layout.addWidget(settings_button)

        logout_button = QPushButton("Logout")
        logout_button.setCursor(Qt.PointingHandCursor)

        logout_button.setStyleSheet(
            """
            QPushButton {
                text-align: left;
                padding: 10px 12px;
                border: none;
                border-radius: 8px;
                color: #FF6B6B;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #142A57;
                color: white;
            }
            """
        )

        logout_button.clicked.connect(
            self.logout_requested.emit
        )

        layout.addWidget(logout_button)

        self._set_active_navigation("dashboard")

    def _handle_navigation(self, key):
        self._set_active_navigation(key)
        self.nav_requested.emit(key)

    def _set_active_navigation(self, key):
        for button_key, button in self.nav_buttons.items():
            button.setChecked(button_key == key)