from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QGridLayout,
)


class ProjectManagerDashboardScreen(QWidget):
    """
    Dashboard principal du PROJECT_MANAGER.

    L'IA reste un assistant du Chef de Projet.
    Elle propose des analyses et des validations,
    mais ne réalise aucune assignation automatique.
    """

    nav_requested = Signal(str)
    logout_requested = Signal()
    settings_requested = Signal()

    def __init__(
        self,
        project: Optional[object] = None,
        user: Optional[object] = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self.project = project
        self.user = user

        self._build_ui()

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def _build_ui(self):

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ======================================================
        # SIDEBAR
        # ======================================================

        sidebar = QFrame()
        sidebar.setFixedWidth(185)

        sidebar.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border-right: 1px solid #E5E7EB;
            }
            """
        )

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(
            14, 18, 14, 18
        )
        sidebar_layout.setSpacing(5)

        brand = QLabel("▣  Microsoft Word Integrator")
        brand.setStyleSheet(
            """
            QLabel {
                color: #173F8A;
                font-size: 11px;
                font-weight: 700;
                padding: 5px;
            }
            """
        )

        sidebar_layout.addWidget(brand)
        sidebar_layout.addSpacing(18)

        workspace = QLabel("WORKSPACE")
        self._section_label(workspace)
        sidebar_layout.addWidget(workspace)

        self.dashboard_button = self._nav_button(
            "▦   Overview",
            "dashboard",
            active=True,
        )

        self.sections_button = self._nav_button(
            "▤   Sections",
            "sections",
        )

        self.documents_button = self._nav_button(
            "▧   Documents",
            "documents",
        )

        self.members_button = self._nav_button(
            "♙   Members",
            "members",
        )

        self.assignments_button = self._nav_button(
            "☷   Assignments",
            "assignments",
        )

        for button in (
            self.dashboard_button,
            self.sections_button,
            self.documents_button,
            self.members_button,
            self.assignments_button,
        ):
            sidebar_layout.addWidget(button)

        sidebar_layout.addSpacing(18)

        workflow = QLabel("WORKFLOW")
        self._section_label(workflow)
        sidebar_layout.addWidget(workflow)

        validation_button = self._nav_button(
            "✓   Validation",
            "validation",
            badge="3",
        )

        comments_button = self._nav_button(
            "◌   Comments",
            "comments",
        )

        versions_button = self._nav_button(
            "◷   Versions",
            "versions",
        )

        sidebar_layout.addWidget(validation_button)
        sidebar_layout.addWidget(comments_button)
        sidebar_layout.addWidget(versions_button)

        sidebar_layout.addSpacing(18)

        activity = QLabel("ACTIVITY")
        self._section_label(activity)
        sidebar_layout.addWidget(activity)

        activity_button = self._nav_button(
            "♧   Activity",
            "activity",
        )

        notifications_button = self._nav_button(
            "♧   Notifications",
            "notifications",
            badge="3",
        )

        sidebar_layout.addWidget(activity_button)
        sidebar_layout.addWidget(notifications_button)

        sidebar_layout.addSpacing(18)

        intelligence = QLabel("INTELLIGENCE")
        self._section_label(intelligence)
        sidebar_layout.addWidget(intelligence)

        ai_button = self._nav_button(
            "✣   AI Insights",
            "ai_insights",
        )

        sidebar_layout.addWidget(ai_button)

        sidebar_layout.addStretch()

        settings_button = self._nav_button(
            "⚙   Settings",
            "settings",
        )

        settings_button.clicked.connect(
            self.settings_requested.emit
        )

        sidebar_layout.addWidget(settings_button)

        logout_button = self._nav_button(
            "←   Logout",
            "logout",
        )

        logout_button.clicked.connect(
            self.logout_requested.emit
        )

        sidebar_layout.addWidget(logout_button)

        root.addWidget(sidebar)

        # ======================================================
        # RIGHT SIDE
        # ======================================================

        right_side = QVBoxLayout()
        right_side.setContentsMargins(0, 0, 0, 0)
        right_side.setSpacing(0)

        root.addLayout(right_side)

        # ======================================================
        # TOP BAR
        # ======================================================

        top_bar = QFrame()
        top_bar.setFixedHeight(58)

        top_bar.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E5E7EB;
            }
            """
        )

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(
            18, 0, 20, 0
        )

        menu_label = QLabel("☰")
        menu_label.setStyleSheet(
            """
            QLabel {
                color: #667085;
                font-size: 15px;
            }
            """
        )

        top_layout.addWidget(menu_label)
        top_layout.addStretch()

        notification = QLabel("♧  3")
        notification.setStyleSheet(
            """
            QLabel {
                color: #174EA6;
                font-size: 12px;
                font-weight: 700;
            }
            """
        )

        top_layout.addWidget(notification)

        user_label = QLabel(
            self._user_name()
        )

        user_label.setStyleSheet(
            """
            QLabel {
                color: #1F2937;
                font-size: 11px;
                font-weight: 700;
                padding-left: 12px;
            }
            """
        )

        top_layout.addWidget(user_label)

        role_label = QLabel("Project Manager")
        role_label.setStyleSheet(
            """
            QLabel {
                color: #98A2B3;
                font-size: 9px;
            }
            """
        )

        top_layout.addWidget(role_label)

        right_side.addWidget(top_bar)

        # ======================================================
        # SCROLL
        # ======================================================

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: #F7F8FA;
            }
            """
        )

        content = QWidget()

        content.setStyleSheet(
            """
            QWidget {
                background-color: #F7F8FA;
            }
            """
        )

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(
            14, 14, 14, 20
        )
        content_layout.setSpacing(12)

        # ======================================================
        # PROJECT HEADER
        # ======================================================

        header_grid = QGridLayout()
        header_grid.setSpacing(10)

        project_card = self._card()

        project_layout = QVBoxLayout(project_card)
        project_layout.setContentsMargins(
            16, 14, 16, 14
        )

        back = QLabel("←  My Projects")
        back.setStyleSheet(
            """
            QLabel {
                color: #174EA6;
                font-size: 10px;
            }
            """
        )

        project_layout.addWidget(back)

        title_row = QHBoxLayout()

        title = QLabel(
            self._project_name()
            + " – Cahier des charges"
        )

        title.setStyleSheet(
            """
            QLabel {
                color: #202124;
                font-size: 15px;
                font-weight: 700;
            }
            """
        )

        title_row.addWidget(title)

        active = QLabel("ACTIVE")
        active.setStyleSheet(
            """
            QLabel {
                color: #16803C;
                background-color: #E8F5E9;
                border-radius: 8px;
                padding: 3px 7px;
                font-size: 8px;
                font-weight: 700;
            }
            """
        )

        title_row.addWidget(active)
        title_row.addStretch()

        project_layout.addLayout(title_row)

        description = QLabel(
            "Document de référence pour le projet de transformation digitale."
        )

        description.setStyleSheet(
            """
            QLabel {
                color: #667085;
                font-size: 9px;
            }
            """
        )

        project_layout.addWidget(description)
        project_layout.addSpacing(6)

        info = QLabel(
            f"Project Manager: {self._user_name()}    "
            "◷ Last activity: Today, 14:32"
        )

        info.setStyleSheet(
            """
            QLabel {
                color: #667085;
                font-size: 9px;
            }
            """
        )

        project_layout.addWidget(info)

        header_grid.addWidget(
            project_card, 0, 0
        )

        # ======================================================
        # PROGRESS
        # ======================================================

        progress_card = self._card()

        progress_layout = QVBoxLayout(progress_card)
        progress_layout.setContentsMargins(
            14, 14, 14, 14
        )

        progress_title = QLabel(
            "Project Progress"
        )
        self._card_title(progress_title)
        progress_layout.addWidget(progress_title)

        progress_row = QHBoxLayout()

        circle = QLabel("78%")
        circle.setAlignment(Qt.AlignCenter)
        circle.setFixedSize(65, 65)
        circle.setStyleSheet(
            """
            QLabel {
                border: 5px solid #2374D8;
                border-radius: 32px;
                color: #174EA6;
                font-size: 13px;
                font-weight: 700;
                background-color: white;
            }
            """
        )

        progress_row.addWidget(circle)

        progress_info = QVBoxLayout()

        completed = QLabel(
            "14 of 18 sections completed"
        )
        self._card_title(completed)
        progress_info.addWidget(completed)

        bar = QProgressBar()
        bar.setValue(78)
        bar.setTextVisible(False)
        bar.setFixedHeight(5)
        bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #E5E7EB;
                border: none;
                border-radius: 3px;
            }

            QProgressBar::chunk {
                background-color: #2374D8;
                border-radius: 3px;
            }
            """
        )

        progress_info.addWidget(bar)

        stats = QLabel(
            "● 9 Validated     "
            "● 6 In Progress     "
            "● 3 Pending     "
            "● 0 Rejected"
        )

        stats.setStyleSheet(
            """
            QLabel {
                color: #667085;
                font-size: 8px;
            }
            """
        )

        progress_info.addWidget(stats)

        progress_row.addLayout(progress_info)

        progress_layout.addLayout(progress_row)

        header_grid.addWidget(
            progress_card, 0, 1
        )

        # ======================================================
        # ACTION REQUIRED
        # ======================================================

        action_card = self._card()

        action_layout = QVBoxLayout(action_card)
        action_layout.setContentsMargins(
            14, 14, 14, 14
        )

        action_title = QLabel(
            "Action Required"
        )
        self._card_title(action_title)
        action_layout.addWidget(action_title)

        for text in (
            "⚠  3 sections waiting for validation",
            "⚠  1 section rejected",
            "♙  2 members have no assignment",
            "▣  1 document currently locked",
        ):
            label = QLabel(text)
            label.setStyleSheet(
                """
                QLabel {
                    color: #475467;
                    font-size: 8px;
                    padding: 2px;
                }
                """
            )
            action_layout.addWidget(label)

        review = QPushButton("Review Now")
        self._small_button(review)
        action_layout.addWidget(review)

        header_grid.addWidget(
            action_card, 0, 2
        )

        content_layout.addLayout(header_grid)

        # ======================================================
        # STATISTICS
        # ======================================================

        stats_grid = QGridLayout()
        stats_grid.setSpacing(8)

        cards = [
            ("▦", "18", "Sections", "Total sections"),
            ("♙", "6", "Members", "Active members"),
            ("▧", "1", "Document", "Main document"),
            ("◷", "3", "Pending Actions", "Require attention"),
            ("◷", "42", "Versions", "Document versions"),
            ("◌", "12", "Comments", "Total comments"),
        ]

        for index, item in enumerate(cards):

            card = self._stat_card(*item)

            stats_grid.addWidget(
                card,
                0,
                index,
            )

        content_layout.addLayout(stats_grid)

        # ======================================================
        # MAIN PANELS
        # ======================================================

        main_grid = QGridLayout()
        main_grid.setSpacing(10)

        sections_card = self._sections_overview()
        validation_card = self._validation_center()
        team_card = self._team_assignments()

        main_grid.addWidget(
            sections_card, 0, 0
        )

        main_grid.addWidget(
            validation_card, 0, 1
        )

        main_grid.addWidget(
            team_card, 0, 2
        )

        content_layout.addLayout(main_grid)

        # ======================================================
        # SECOND ROW
        # ======================================================

        second_grid = QGridLayout()
        second_grid.setSpacing(10)

        document_card = self._document_card()
        project_team = self._project_team()

        second_grid.addWidget(
            document_card, 0, 0
        )

        second_grid.addWidget(
            project_team, 0, 1
        )

        content_layout.addLayout(second_grid)

        # ======================================================
        # BOTTOM
        # ======================================================

        bottom_grid = QGridLayout()
        bottom_grid.setSpacing(10)

        bottom_grid.addWidget(
            self._activity_card(),
            0, 0
        )

        bottom_grid.addWidget(
            self._notifications_card(),
            0, 1
        )

        bottom_grid.addWidget(
            self._ai_card(),
            0, 2
        )

        bottom_grid.addWidget(
            self._quick_actions(),
            0, 3
        )

        content_layout.addLayout(
            bottom_grid
        )

        scroll.setWidget(content)

        right_side.addWidget(scroll)

    # ==========================================================
    # CARDS
    # ==========================================================

    def _card(self):

        card = QFrame()

        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
            }
            """
        )

        return card

    def _card_title(self, label):

        label.setStyleSheet(
            """
            QLabel {
                color: #202124;
                font-size: 10px;
                font-weight: 700;
            }
            """
        )

    def _section_label(self, label):

        label.setStyleSheet(
            """
            QLabel {
                color: #98A2B3;
                font-size: 8px;
                font-weight: 700;
                padding-left: 6px;
            }
            """
        )

    # ==========================================================
    # STAT CARD
    # ==========================================================

    def _stat_card(
        self,
        icon,
        value,
        title,
        subtitle,
    ):

        card = self._card()

        layout = QHBoxLayout(card)
        layout.setContentsMargins(
            10, 10, 10, 10
        )

        icon_label = QLabel(icon)
        icon_label.setFixedWidth(25)
        icon_label.setStyleSheet(
            """
            QLabel {
                color: #2374D8;
                font-size: 17px;
            }
            """
        )

        layout.addWidget(icon_label)

        info = QVBoxLayout()

        value_label = QLabel(value)
        value_label.setStyleSheet(
            """
            QLabel {
                color: #202124;
                font-size: 14px;
                font-weight: 700;
            }
            """
        )

        info.addWidget(value_label)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            """
            QLabel {
                color: #344054;
                font-size: 8px;
                font-weight: 700;
            }
            """
        )

        info.addWidget(title_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(
            """
            QLabel {
                color: #98A2B3;
                font-size: 7px;
            }
            """
        )

        info.addWidget(subtitle_label)

        layout.addLayout(info)

        return card

    # ==========================================================
    # SECTIONS OVERVIEW
    # ==========================================================

    def _sections_overview(self):

        card = self._card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            12, 12, 12, 12
        )

        title = QLabel(
            "Sections Overview"
        )
        self._card_title(title)
        layout.addWidget(title)

        search = QLabel(
            "⌕  Search sections...       "
            "All Status ▼       Sort by ▼"
        )

        search.setStyleSheet(
            """
            QLabel {
                border: 1px solid #D0D5DD;
                border-radius: 5px;
                padding: 6px;
                color: #98A2B3;
                font-size: 8px;
            }
            """
        )

        layout.addWidget(search)

        sections = [
            ("1. Introduction", "VALIDATED"),
            ("2. Architecture", "IN PROGRESS"),
            ("3. Requirements", "PENDING VALIDATION"),
            ("4. Design", "UNASSIGNED"),
            ("5. Implementation", "IN PROGRESS"),
            ("6. Testing", "LOCKED"),
            ("7. Deployment", "UNASSIGNED"),
        ]

        for index, (name, status) in enumerate(sections):

            row = QHBoxLayout()

            label = QLabel(name)
            label.setStyleSheet(
                """
                QLabel {
                    color: #344054;
                    font-size: 8px;
                    font-weight: 600;
                }
                """
            )

            row.addWidget(label)
            row.addStretch()

            status_label = QLabel(status)
            status_label.setStyleSheet(
                """
                QLabel {
                    color: #667085;
                    font-size: 7px;
                    font-weight: 700;
                }
                """
            )

            row.addWidget(status_label)

            button = QPushButton(
                "Review"
                if "PENDING" in status
                else "View"
            )

            self._small_button(button)
            row.addWidget(button)

            layout.addLayout(row)

        layout.addStretch()

        return card

    # ==========================================================
    # VALIDATION CENTER
    # ==========================================================

    def _validation_center(self):

        card = self._card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            12, 12, 12, 12
        )

        title = QLabel(
            "Validation Center       3"
        )

        self._card_title(title)
        layout.addWidget(title)

        items = [
            ("Architecture", "2 changes"),
            ("Requirements", "5 changes"),
            ("Design", "3 changes"),
        ]

        for name, changes in items:

            row = QVBoxLayout()

            section = QLabel(name)
            self._card_title(section)
            row.addWidget(section)

            change = QLabel(
                f"Submitted recently                 {changes}"
            )

            change.setStyleSheet(
                """
                QLabel {
                    color: #667085;
                    font-size: 7px;
                }
                """
            )

            row.addWidget(change)

            button = QPushButton(
                "Review Changes"
            )

            self._small_button(button)
            row.addWidget(button)

            layout.addLayout(row)

        layout.addStretch()

        return card

    # ==========================================================
    # TEAM ASSIGNMENTS
    # ==========================================================

    def _team_assignments(self):

        card = self._card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            12, 12, 12, 12
        )

        title = QLabel(
            "Team Assignments"
        )

        self._card_title(title)
        layout.addWidget(title)

        members = [
            ("Ali Maaloudi", "4 sections assigned", 80),
            ("Dhia Tarhouni", "5 sections assigned", 60),
            ("Nouha Trabelsi", "6 sections assigned", 90),
        ]

        for name, text, value in members:

            label = QLabel(
                f"{name}  —  {text}"
            )

            label.setStyleSheet(
                """
                QLabel {
                    color: #344054;
                    font-size: 8px;
                    font-weight: 600;
                }
                """
            )

            layout.addWidget(label)

            bar = QProgressBar()
            bar.setValue(value)
            bar.setTextVisible(False)
            bar.setFixedHeight(4)

            bar.setStyleSheet(
                """
                QProgressBar {
                    background-color: #E5E7EB;
                    border: none;
                }

                QProgressBar::chunk {
                    background-color: #2374D8;
                }
                """
            )

            layout.addWidget(bar)

        button = QPushButton(
            "Manage Assignments"
        )

        self._small_button(button)
        layout.addWidget(button)

        return card

    # ==========================================================
    # DOCUMENT
    # ==========================================================

    def _document_card(self):

        card = self._card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            12, 12, 12, 12
        )

        title = QLabel(
            "Project Document"
        )

        self._card_title(title)
        layout.addWidget(title)

        document = QLabel(
            "▣   Cahier des charges.docx"
        )

        document.setStyleSheet(
            """
            QLabel {
                color: #344054;
                font-size: 11px;
                font-weight: 700;
            }
            """
        )

        layout.addWidget(document)

        details = QLabel(
            "18 sections     ◷ 42 versions\n"
            "Last modified: Today, 14:20"
        )

        details.setStyleSheet(
            """
            QLabel {
                color: #667085;
                font-size: 8px;
            }
            """
        )

        layout.addWidget(details)

        row = QHBoxLayout()

        open_button = QPushButton(
            "Open Document"
        )

        self._primary_button(open_button)
        row.addWidget(open_button)

        versions = QPushButton(
            "View Versions"
        )

        self._small_button(versions)
        row.addWidget(versions)

        layout.addLayout(row)

        return card

    # ==========================================================
    # PROJECT TEAM
    # ==========================================================

    def _project_team(self):

        card = self._card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            12, 12, 12, 12
        )

        title = QLabel(
            "Project Team"
        )

        self._card_title(title)
        layout.addWidget(title)

        members = [
            ("Radhi Maddouri", "PROJECT MANAGER"),
            ("Ali Maaloudi", "COLLABORATOR"),
            ("Dhia Tarhouni", "COLLABORATOR"),
            ("Nouha Trabelsi", "COLLABORATOR"),
        ]

        for name, role in members:

            label = QLabel(
                f"●  {name}   {role}"
            )

            label.setStyleSheet(
                """
                QLabel {
                    color: #475467;
                    font-size: 8px;
                    padding: 4px;
                }
                """
            )

            layout.addWidget(label)

        button = QPushButton(
            "View All Members"
        )

        self._small_button(button)

        layout.addWidget(button)

        return card

    # ==========================================================
    # ACTIVITY
    # ==========================================================

    def _activity_card(self):

        return self._simple_list_card(
            "Recent Activity",
            [
                'Ali Maaloudi updated section "Architecture"',
                'Dhia Tarhouni submitted "Requirements" for validation',
                'Nouha Trabelsi completed section "Introduction"',
                'Radhi Maddouri added new member to project',
            ],
        )

    # ==========================================================
    # NOTIFICATIONS
    # ==========================================================

    def _notifications_card(self):

        return self._simple_list_card(
            "Notifications",
            [
                'Section "Requirements" submitted for validation',
                'Section "Design" was rejected',
                'Section "Introduction" was validated',
                'New comment on section "Architecture"',
            ],
        )

    # ==========================================================
    # AI
    # ==========================================================

    def _ai_card(self):

        card = self._card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            12, 12, 12, 12
        )

        title = QLabel(
            "AI Insights"
        )

        title.setStyleSheet(
            """
            QLabel {
                color: #7C3AED;
                font-size: 10px;
                font-weight: 700;
            }
            """
        )

        layout.addWidget(title)

        for text in (
            "12 changes detected",
            "3 potential risks",
            "2 inconsistencies",
        ):

            label = QLabel(text)

            label.setStyleSheet(
                """
                QLabel {
                    color: #667085;
                    font-size: 8px;
                    padding: 5px;
                }
                """
            )

            layout.addWidget(label)

        button = QPushButton(
            "Open AI Dashboard"
        )

        self._small_button(button)

        layout.addWidget(button)

        return card

    # ==========================================================
    # QUICK ACTIONS
    # ==========================================================

    def _quick_actions(self):

        card = self._card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            12, 12, 12, 12
        )

        title = QLabel(
            "Quick Actions"
        )

        self._card_title(title)
        layout.addWidget(title)

        actions = [
            "＋  New Section",
            "♙  Assign Sections",
            "♧  Add Member",
            "⌕  Review Validations",
            "▣  Open Document",
        ]

        for text in actions:

            button = QPushButton(text)

            self._small_button(button)

            layout.addWidget(button)

        return card

    # ==========================================================
    # SIMPLE LIST
    # ==========================================================

    def _simple_list_card(
        self,
        title_text,
        items,
    ):

        card = self._card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            12, 12, 12, 12
        )

        title = QLabel(title_text)

        self._card_title(title)
        layout.addWidget(title)

        for text in items:

            label = QLabel(
                "●  " + text
            )

            label.setWordWrap(True)

            label.setStyleSheet(
                """
                QLabel {
                    color: #667085;
                    font-size: 8px;
                    padding: 4px;
                }
                """
            )

            layout.addWidget(label)

        layout.addStretch()

        return card

    # ==========================================================
    # BUTTONS
    # ==========================================================

    def _nav_button(
        self,
        text,
        key,
        active=False,
        badge=None,
    ):

        button = QPushButton(text)

        button.setCursor(
            Qt.PointingHandCursor
        )

        background = (
            "#EAF2FF"
            if active
            else "transparent"
        )

        color = (
            "#174EA6"
            if active
            else "#667085"
        )

        button.setStyleSheet(
            f"""
            QPushButton {{
                text-align: left;
                background-color: {background};
                color: {color};
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 9px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                background-color: #EAF2FF;
                color: #174EA6;
            }}
            """
        )

        button.clicked.connect(
            lambda: self.nav_requested.emit(key)
        )

        return button

    def _small_button(self, button):

        button.setCursor(
            Qt.PointingHandCursor
        )

        button.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                color: #174EA6;
                border: 1px solid #D0D5DD;
                border-radius: 5px;
                padding: 4px 8px;
                font-size: 7px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #EAF2FF;
            }
            """
        )

    def _primary_button(self, button):

        button.setCursor(
            Qt.PointingHandCursor
        )

        button.setStyleSheet(
            """
            QPushButton {
                background-color: #1769D1;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 8px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #1257AE;
            }
            """
        )

    # ==========================================================
    # HELPERS
    # ==========================================================

    def _project_name(self):

        if self.project is None:
            return "Project Test"

        return getattr(
            self.project,
            "name",
            getattr(
                self.project,
                "title",
                "Project Test",
            ),
        )

    def _user_name(self):

        if self.user is None:
            return "Project Manager"

        if isinstance(self.user, dict):

            first_name = self.user.get(
                "first_name",
                self.user.get("prenom", ""),
            )

            last_name = self.user.get(
                "last_name",
                self.user.get("nom", ""),
            )

        else:

            first_name = getattr(
                self.user,
                "prenom",
                "",
            )

            last_name = getattr(
                self.user,
                "nom",
                "",
            )

        full_name = (
            f"{first_name} {last_name}"
        ).strip()

        if full_name:
            return full_name

        if isinstance(self.user, dict):
            return self.user.get(
                "name",
                "Project Manager",
            )

        return getattr(
            self.user,
            "name",
            "Project Manager",
        )


if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = ProjectManagerDashboardScreen()

    window.resize(
        1400,
        850,
    )

    window.setWindowTitle(
        "Project Manager Dashboard"
    )

    window.show()

    sys.exit(
        app.exec()
    )