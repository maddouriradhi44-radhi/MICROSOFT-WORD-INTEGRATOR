from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
QWidget,
QFrame,
QHBoxLayout,
QVBoxLayout,
QLabel,
QPushButton,
QGridLayout,
)

from services.notification_service import notification_service
from services.section_service import section_service

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

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def _build_ui(self):

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ======================================================
        # SIDEBAR
        # ======================================================

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

        self._build_sidebar_navigation(
            sidebar_layout
        )

        self.sidebar.setLayout(
            sidebar_layout
        )

        # ======================================================
        # CONTENT
        # ======================================================

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

        content_layout.addWidget(
            self.header
        )

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
        body_layout.setContentsMargins(
            30,
            28,
            30,
            30,
        )
        body_layout.setSpacing(18)

        # ======================================================
        # WELCOME
        # ======================================================

        first_name = ""

        if isinstance(self.user, dict):
            first_name = self.user.get(
                "first_name",
                "",
            )

        if first_name:
            welcome_text = (
                f"Welcome back, {first_name}"
            )
        else:
            welcome_text = "Welcome back"

        welcome = QLabel(
            welcome_text
        )

        welcome.setStyleSheet(
            """
            color: #6B7280;
            font-size: 13px;
            border: none;
            """
        )

        body_layout.addWidget(
            welcome
        )

        project_name = QLabel(
            self.project.name
        )

        project_name.setStyleSheet(
            """
            color: #14171F;
            font-size: 26px;
            font-weight: 700;
            border: none;
            """
        )

        body_layout.addWidget(
            project_name
        )

        project_description = getattr(
            self.project,
            "description",
            None,
        )

        if project_description:

            description = QLabel(
                project_description
            )

            description.setWordWrap(True)

            description.setStyleSheet(
                """
                color: #6B7280;
                font-size: 12px;
                border: none;
                """
            )

            body_layout.addWidget(
                description
            )

        # ======================================================
        # STATISTICS
        # ======================================================

        stats_layout = QGridLayout()
        stats_layout.setSpacing(14)

        self.sections_value = QLabel("0")
        self.documents_value = QLabel("1")
        self.progress_value = QLabel("0%")
        self.status_value = QLabel(
            str(self.project.status)
        )

        self._add_stat_card(
            stats_layout,
            0,
            0,
            "My Sections",
            self.sections_value,
        )

        self._add_stat_card(
            stats_layout,
            0,
            1,
            "Documents",
            self.documents_value,
        )

        self._add_stat_card(
            stats_layout,
            0,
            2,
            "Progress",
            self.progress_value,
        )

        self._add_stat_card(
            stats_layout,
            0,
            3,
            "Project Status",
            self.status_value,
        )

        body_layout.addLayout(
            stats_layout
        )

        # ======================================================
        # QUICK ACTIONS
        # ======================================================

        quick_title = QLabel(
            "Quick Actions"
        )

        quick_title.setStyleSheet(
            """
            color: #14171F;
            font-size: 16px;
            font-weight: 700;
            border: none;
            """
        )

        body_layout.addWidget(
            quick_title
        )

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        self._add_action_button(
            actions_layout,
            "My Sections",
            "sections",
        )

        self._add_action_button(
            actions_layout,
            "Document",
            "document",
        )

        self._add_action_button(
            actions_layout,
            "Notifications",
            "notifications",
        )

        self._add_action_button(
            actions_layout,
            "Activity",
            "activity",
        )

        body_layout.addLayout(
            actions_layout
        )

        # ======================================================
        # WORKFLOW
        # ======================================================

        workflow_card = QFrame()

        workflow_card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            """
        )

        workflow_layout = QVBoxLayout()
        workflow_layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )
        workflow_layout.setSpacing(8)

        workflow_title = QLabel(
            "Your Workspace"
        )

        workflow_title.setStyleSheet(
            """
            color: #14171F;
            font-size: 15px;
            font-weight: 700;
            border: none;
            """
        )

        workflow_layout.addWidget(
            workflow_title
        )

        workflow_text = QLabel(
            "Work on your assigned sections through "
            "Microsoft Word. Export your section, make "
            "your modifications, then import the updated "
            "version for validation."
        )

        workflow_text.setWordWrap(True)

        workflow_text.setStyleSheet(
            """
            color: #6B7280;
            font-size: 12px;
            border: none;
            """
        )

        workflow_layout.addWidget(
            workflow_text
        )

        workflow_card.setLayout(
            workflow_layout
        )

        body_layout.addWidget(
            workflow_card
        )

        # ======================================================
        # RECENT ACTIVITY
        # ======================================================

        activity_title = QLabel(
            "Recent Activity"
        )

        activity_title.setStyleSheet(
            """
            color: #14171F;
            font-size: 16px;
            font-weight: 700;
            border: none;
            """
        )

        body_layout.addWidget(
            activity_title
        )

        activity_card = QFrame()

        activity_card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            """
        )

        activity_layout = QVBoxLayout()
        activity_layout.setContentsMargins(
            20,
            16,
            20,
            16,
        )
        activity_layout.setSpacing(10)

        recent_items = [
            "Open Activity to view your latest actions.",
            "Open My Sections to continue your assigned work.",
            "Check Notifications for project updates.",
        ]

        for item_text in recent_items:

            item = QLabel(
                f"• {item_text}"
            )

            item.setStyleSheet(
                """
                color: #6B7280;
                font-size: 12px;
                border: none;
                """
            )

            activity_layout.addWidget(
                item
            )

        activity_card.setLayout(
            activity_layout
        )

        body_layout.addWidget(
            activity_card
        )

        body_layout.addStretch()

        body.setLayout(
            body_layout
        )

        content_layout.addWidget(
            body,
            1,
        )

        self.content.setLayout(
            content_layout
        )

        main_layout.addWidget(
            self.sidebar
        )

        main_layout.addWidget(
            self.content,
            1,
        )

        self.setLayout(
            main_layout
        )

        self._load_dashboard_data()

    # ==========================================================
    # STAT CARD
    # ==========================================================

    def _add_stat_card(
        self,
        layout,
        row,
        column,
        title,
        value_label,
    ):

        card = QFrame()

        card.setMinimumHeight(100)

        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }
            """
        )

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        card_layout.setSpacing(5)

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet(
            """
            color: #8A94A6;
            font-size: 11px;
            font-weight: 600;
            border: none;
            """
        )

        value_label.setStyleSheet(
            """
            color: #14171F;
            font-size: 22px;
            font-weight: 700;
            border: none;
            """
        )

        card_layout.addWidget(
            title_label
        )

        card_layout.addWidget(
            value_label
        )

        card_layout.addStretch()

        card.setLayout(
            card_layout
        )

        layout.addWidget(
            card,
            row,
            column,
        )

    # ==========================================================
    # QUICK ACTION
    # ==========================================================

    def _add_action_button(
        self,
        layout,
        text,
        key,
    ):

        button = QPushButton(
            text
        )

        button.setCursor(
            Qt.PointingHandCursor
        )

        button.setMinimumHeight(
            42
        )

        button.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                color: #344054;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 0 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #F3F4F6;
                border-color: #D0D5DD;
            }
            """
        )

        button.clicked.connect(
            lambda checked=False, key=key:
            self._handle_navigation(key)
        )

        layout.addWidget(
            button
        )

    # ==========================================================
    # LOAD DASHBOARD DATA
    # ==========================================================

    def _load_dashboard_data(self):

        try:

            sections = (
                section_service.get_my_sections()
            )

            project_id = getattr(
                self.project,
                "id",
                None,
            )

            project_sections = [
                section
                for section in sections
                if (
                    project_id is not None
                    and getattr(
                        section,
                        "project_id",
                        None,
                    )
                    == project_id
                )
            ]

            self.sections_value.setText(
                str(len(project_sections))
            )

            if project_sections:

                validated = sum(
                    1
                    for section in project_sections
                    if str(
                        getattr(
                            section,
                            "status",
                            "",
                        )
                    ).lower()
                    == "validated"
                )

                progress = int(
                    (
                        validated
                        / len(project_sections)
                    )
                    * 100
                )

                self.progress_value.setText(
                    f"{progress}%"
                )

            else:

                self.progress_value.setText(
                    "0%"
                )

        except Exception:

            self.sections_value.setText(
                "—"
            )

            self.progress_value.setText(
                "—"
            )

    # ==========================================================
    # SIDEBAR
    # ==========================================================

    def _build_sidebar_navigation(
        self,
        layout,
    ):

        navigation_items = [
            ("dashboard", "Dashboard"),
            ("sections", "My Sections"),
            ("document", "Document"),
            ("notifications", "Notifications"),
            ("activity", "Activity"),
        ]

        self.nav_buttons = {}

        for key, label in navigation_items:

            button = QPushButton(
                label
            )

            button.setCursor(
                Qt.PointingHandCursor
            )

            button.setCheckable(
                True
            )

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

            layout.addWidget(
                button
            )

        layout.addStretch()

        settings_button = QPushButton(
            "Settings"
        )

        settings_button.setCursor(
            Qt.PointingHandCursor
        )

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

        layout.addWidget(
            settings_button
        )

        logout_button = QPushButton(
            "Logout"
        )

        logout_button.setCursor(
            Qt.PointingHandCursor
        )

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

        layout.addWidget(
            logout_button
        )

        self._set_active_navigation(
            "dashboard"
        )

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    def _handle_navigation(
        self,
        key,
    ):

        self._set_active_navigation(
            key
        )

        self.nav_requested.emit(
            key
        )

    def _set_active_navigation(
        self,
        key,
    ):

        for button_key, button in self.nav_buttons.items():

            button.setChecked(
                button_key == key
            )
