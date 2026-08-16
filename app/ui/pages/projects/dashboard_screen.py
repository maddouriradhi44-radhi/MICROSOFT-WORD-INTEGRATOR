
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Optional
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


# --------------------------------------------------------------------------- #
# Data contracts (kept local so the screen can be dropped in before the real
# DTOs / service call exist; swap for the real imports when available, e.g.:
#   from app.ui.services.project_service import ProjectService
#   from app.schemas.project_schema import DashboardSummarySchema
# --------------------------------------------------------------------------- #
@dataclass
class WorkItem:
    title: str
    document_name: str
    status: str  # "in_progress" | "pending" | "completed"
    section_id: str


@dataclass
class ActivityItem:
    title: str
    timestamp: str
    kind: str  # "assigned" | "completed" | "updated" | "comment"


@dataclass
class DashboardSummary:
    user_name: str
    user_role: str
    project_name: str
    project_status: str
    in_progress_count: int
    completed_count: int
    pending_count: int
    work_items: list[WorkItem] = field(default_factory=list)
    activity_items: list[ActivityItem] = field(default_factory=list)


STATUS_STYLES = {
    "in_progress": ("IN PROGRESS", "#E8F0FE", "#3E63DD"),
    "pending": ("PENDING", "#FFF4E5", "#B76E00"),
    "completed": ("COMPLETED", "#E6F7EE", "#1C9457"),
}

ACTIVITY_DOT_COLORS = {
    "assigned": "#3E63DD",
    "completed": "#1C9457",
    "updated": "#8A94A6",
    "comment": "#F5A623",
}


# --------------------------------------------------------------------------- #
# Small reusable building blocks
# --------------------------------------------------------------------------- #
class StatusBadge(QLabel):
    """Pill-shaped status label, e.g. IN PROGRESS / PENDING / COMPLETED."""

    def __init__(self, status: str, parent: Optional[QWidget] = None):
        text, bg, fg = STATUS_STYLES.get(status, (status.upper(), "#EEE", "#333"))
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                border-radius: 10px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 600;
            }}
            """
        )


class StatCard(QFrame):
    """One of the three summary cards at the top (In Progress / Completed / Pending)."""

    def __init__(
        self,
        value: int,
        label: str,
        sublabel: str,
        icon_bg: str,
        icon_fg: str,
        icon_char: str,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setStyleSheet(
            """
            #StatCard {
                background-color: white;
                border: 1px solid #ECEEF2;
                border-radius: 12px;
            }
            """
        )
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 18, 20, 18)
        outer.setSpacing(10)

        top_row = QHBoxLayout()
        icon_label = QLabel(icon_char)
        icon_label.setFixedSize(36, 36)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(
            f"""
            background-color: {icon_bg};
            color: {icon_fg};
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            """
        )
        value_label = QLabel(str(value))
        value_label.setStyleSheet("font-size: 26px; font-weight: 700; color: #14171F;")

        top_row.addWidget(icon_label)
        top_row.addStretch()
        top_row.addWidget(value_label)
        outer.addLayout(top_row)

        title_label = QLabel(label)
        title_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #14171F;")
        outer.addWidget(title_label)

        sub_label = QLabel(sublabel)
        sub_label.setWordWrap(True)
        sub_label.setStyleSheet("font-size: 12px; color: #8A94A6;")
        outer.addWidget(sub_label)


class WorkItemRow(QFrame):
    """One row inside the 'My Work' card."""

    open_clicked = Signal(str)  # emits section_id

    def __init__(self, item: WorkItem, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.item = item
        self.setStyleSheet("QFrame { border-bottom: 1px solid #F0F1F5; }")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 14, 0, 14)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        title = QLabel(item.title)
        title.setStyleSheet("font-size: 14px; font-weight: 600; color: #14171F;")
        doc = QLabel(f"Document: {item.document_name}")
        doc.setStyleSheet("font-size: 12px; color: #8A94A6;")
        text_col.addWidget(title)
        text_col.addWidget(doc)

        layout.addLayout(text_col)
        layout.addStretch()

        layout.addWidget(StatusBadge(item.status))
        layout.addSpacing(12)

        btn_text = "View Section" if item.status == "completed" else "Open Section"
        btn = QPushButton(btn_text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #D8DCE5;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: 600;
                color: #14171F;
                background-color: white;
            }
            QPushButton:hover { background-color: #F5F6F9; }
            """
        )
        btn.clicked.connect(lambda: self.open_clicked.emit(item.section_id))
        layout.addWidget(btn)


class ActivityRow(QFrame):
    """One row inside the 'Recent Activity' card."""

    def __init__(self, item: ActivityItem, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(10)

        dot = QLabel()
        dot.setFixedSize(10, 10)
        color = ACTIVITY_DOT_COLORS.get(item.kind, "#8A94A6")
        dot.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
        dot_wrap = QVBoxLayout()
        dot_wrap.setContentsMargins(0, 4, 0, 0)
        dot_wrap.addWidget(dot)
        dot_wrap.addStretch()

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        title = QLabel(item.title)
        title.setWordWrap(True)
        title.setStyleSheet("font-size: 13px; font-weight: 600; color: #14171F;")
        ts = QLabel(item.timestamp)
        ts.setStyleSheet("font-size: 11px; color: #8A94A6;")
        text_col.addWidget(title)
        text_col.addWidget(ts)

        layout.addLayout(dot_wrap)
        layout.addLayout(text_col, 1)


class CardContainer(QFrame):
    """White rounded card used for 'My Work' and 'Recent Activity'."""

    def __init__(
        self,
        title: str,
        parent: Optional[QWidget] = None,
        header_action_text: Optional[str] = None,
    ):
        super().__init__(parent)
        self.setObjectName("CardContainer")
        self.setStyleSheet(
            """
            #CardContainer {
                background-color: white;
                border: 1px solid #ECEEF2;
                border-radius: 12px;
            }
            """
        )
        self.outer = QVBoxLayout(self)
        self.outer.setContentsMargins(20, 16, 20, 16)
        self.outer.setSpacing(4)

        header = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 15px; font-weight: 700; color: #14171F;")
        header.addWidget(title_label)
        header.addStretch()

        self.header_action_btn = None
        if header_action_text:
            self.header_action_btn = QPushButton(header_action_text)
            self.header_action_btn.setCursor(Qt.PointingHandCursor)
            self.header_action_btn.setFlat(True)
            self.header_action_btn.setStyleSheet(
                "QPushButton { color: #3E63DD; font-size: 12px; font-weight: 600; border: none; }"
                "QPushButton:hover { text-decoration: underline; }"
            )
            header.addWidget(self.header_action_btn)

        self.outer.addLayout(header)

        self.body = QVBoxLayout()
        self.body.setSpacing(0)
        self.outer.addLayout(self.body)

    def add_row(self, row: QWidget):
        self.body.addWidget(row)


# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
class Sidebar(QFrame):
    nav_clicked = Signal(str)  # "dashboard" | "sections" | "document" | "notifications"
    logout_clicked = Signal()
    settings_clicked = Signal()

    NAV_ITEMS = [
        ("dashboard", "Dashboard"),
        ("sections", "My Sections"),
        ("document", "Document"),
        ("notifications", "Notifications"),
    ]

    def __init__(self, workspace_name: str = "CAPGEMINI", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFixedWidth(220)
        self.setStyleSheet("background-color: #0B1B3B;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(6)

        brand_row = QHBoxLayout()
        logo = QLabel()
        logo.setFixedSize(28, 28)
        logo.setStyleSheet("background-color: #3E63DD; border-radius: 6px;")
        brand_label = QLabel(workspace_name)
        brand_label.setStyleSheet("color: white; font-size: 14px; font-weight: 700;")
        brand_row.addWidget(logo)
        brand_row.addWidget(brand_label)
        brand_row.addStretch()
        layout.addLayout(brand_row)
        layout.addSpacing(24)

        self._nav_buttons: dict[str, QPushButton] = {}
        for key, label in self.NAV_ITEMS:
            btn = self._make_nav_button(label)
            btn.clicked.connect(lambda _, k=key: self.nav_clicked.emit(k))
            self._nav_buttons[key] = btn
            layout.addWidget(btn)

        layout.addStretch()

        settings_btn = self._make_nav_button("Settings", active_bg=False)
        settings_btn.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(settings_btn)

        logout_btn = self._make_nav_button("Logout", active_bg=False, danger=True)
        logout_btn.clicked.connect(self.logout_clicked.emit)
        layout.addWidget(logout_btn)

        self.set_active("dashboard")

    def _make_nav_button(self, label: str, active_bg: bool = True, danger: bool = False) -> QPushButton:
        btn = QPushButton(label)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setCheckable(True)
        color = "#FF6B6B" if danger else "#C6CCDA"
        btn.setStyleSheet(
            f"""
            QPushButton {{
                text-align: left;
                padding: 10px 12px;
                border-radius: 8px;
                color: {color};
                font-size: 13px;
                font-weight: 500;
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{ background-color: #142A57; color: white; }}
            QPushButton:checked {{ background-color: #1E4FD6; color: white; font-weight: 600; }}
            """
        )
        return btn

    def set_active(self, key: str):
        for k, btn in self._nav_buttons.items():
            btn.setChecked(k == key)


# --------------------------------------------------------------------------- #
# Top bar
# --------------------------------------------------------------------------- #
class TopBar(QFrame):
    notifications_clicked = Signal()

    def __init__(
        self,
        project_name: str,
        project_status: str,
        user_name: str,
        user_role: str,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.setStyleSheet("background-color: white; border-bottom: 1px solid #ECEEF2;")
        self.setFixedHeight(64)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)

        title = QLabel(project_name)
        title.setStyleSheet("font-size: 15px; font-weight: 700; color: #14171F;")
        layout.addWidget(title)

        status_dot = QLabel("●")
        is_active = project_status.lower() == "active"
        status_dot.setStyleSheet(f"color: {'#1C9457' if is_active else '#8A94A6'}; font-size: 10px;")
        status_text = QLabel(project_status)
        status_text.setStyleSheet(
            f"color: {'#1C9457' if is_active else '#8A94A6'}; font-size: 12px; font-weight: 600;"
        )
        layout.addSpacing(10)
        layout.addWidget(status_dot)
        layout.addWidget(status_text)

        layout.addStretch()

        bell_btn = QPushButton("🔔")
        bell_btn.setCursor(Qt.PointingHandCursor)
        bell_btn.setFixedSize(32, 32)
        bell_btn.setStyleSheet(
            "QPushButton { border: none; background: transparent; font-size: 16px; }"
            "QPushButton:hover { background-color: #F5F6F9; border-radius: 16px; }"
        )
        bell_btn.clicked.connect(self.notifications_clicked.emit)
        layout.addWidget(bell_btn)
        layout.addSpacing(16)

        name_col = QVBoxLayout()
        name_col.setSpacing(0)
        name_label = QLabel(user_name)
        name_label.setAlignment(Qt.AlignRight)
        name_label.setStyleSheet("font-size: 13px; font-weight: 700; color: #14171F;")
        role_label = QLabel(user_role.upper())
        role_label.setAlignment(Qt.AlignRight)
        role_label.setStyleSheet("font-size: 10px; color: #8A94A6;")
        name_col.addWidget(name_label)
        name_col.addWidget(role_label)
        layout.addLayout(name_col)

        avatar = QLabel(user_name[:1].upper() if user_name else "?")
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(
            "background-color: #E8F0FE; color: #3E63DD; border-radius: 18px; font-weight: 700;"
        )
        layout.addSpacing(10)
        layout.addWidget(avatar)


# --------------------------------------------------------------------------- #
# Main dashboard screen
# --------------------------------------------------------------------------- #
class DashboardScreen(QWidget):
    """
    Top-level widget for the Dashboard tab of a project workspace.

    Usage:
        screen = DashboardScreen()
        screen.load_summary(summary)  # DashboardSummary from the service layer
        screen.section_open_requested.connect(on_open_section)
        screen.nav_requested.connect(on_nav_change)
    """

    section_open_requested = Signal(str)  # section_id
    nav_requested = Signal(str)           # "dashboard" | "sections" | "document" | "notifications"
    logout_requested = Signal()
    settings_requested = Signal()

    def __init__(
    self,
    project: Optional[object] = None,
    parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.project = project
        self._summary: Optional[DashboardSummary] = None

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.nav_clicked.connect(self.nav_requested.emit)
        self.sidebar.logout_clicked.connect(self.logout_requested.emit)
        self.sidebar.settings_clicked.connect(self.settings_requested.emit)
        root.addWidget(self.sidebar)

        right_col = QVBoxLayout()
        right_col.setSpacing(0)
        root.addLayout(right_col)

        self.top_bar = TopBar("Project", "Active", "", "")
        self.top_bar.notifications_clicked.connect(lambda: self.nav_requested.emit("notifications"))
        right_col.addWidget(self.top_bar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background-color: #F7F8FA; border: none; }")
        right_col.addWidget(scroll)

        content = QWidget()
        content.setStyleSheet("background-color: #F7F8FA;")
        scroll.setWidget(content)

        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(28, 24, 28, 24)
        self.content_layout.setSpacing(18)

        self.welcome_label = QLabel("Welcome back 👋")
        self.welcome_label.setStyleSheet("font-size: 22px; font-weight: 700; color: #14171F;")
        self.content_layout.addWidget(self.welcome_label)

        self.subtitle_label = QLabel("Here is the current state of your project workspace.")
        self.subtitle_label.setStyleSheet("font-size: 13px; color: #8A94A6;")
        self.content_layout.addWidget(self.subtitle_label)

        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(16)
        self.content_layout.addLayout(self.stats_row)

        lower_row = QHBoxLayout()
        lower_row.setSpacing(16)
        self.content_layout.addLayout(lower_row)

        self.work_card = CardContainer("My Work", header_action_text="VIEW ALL")
        if self.work_card.header_action_btn:
            self.work_card.header_action_btn.clicked.connect(lambda: self.nav_requested.emit("sections"))
        lower_row.addWidget(self.work_card, 2)

        self.activity_card = CardContainer("Recent Activity")
        lower_row.addWidget(self.activity_card, 1)

        self.content_layout.addStretch()

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def load_summary(self, summary: DashboardSummary):
        """Populate the screen from a DashboardSummary (fetched via the service layer)."""
        self._summary = summary

        self.top_bar.deleteLater()
        parent_layout = self.layout().itemAt(1).layout()  # right_col
        self.top_bar = TopBar(
            summary.project_name, summary.project_status, summary.user_name, summary.user_role
        )
        self.top_bar.notifications_clicked.connect(lambda: self.nav_requested.emit("notifications"))
        parent_layout.insertWidget(0, self.top_bar)

        self.welcome_label.setText(f"Welcome back, {summary.user_name} 👋")

        self._clear_layout(self.stats_row)
        self.stats_row.addWidget(
            StatCard(
                summary.in_progress_count,
                "In Progress",
                "Sections currently being worked on",
                "#E8F0FE",
                "#3E63DD",
                "⏱",
            )
        )
        self.stats_row.addWidget(
            StatCard(
                summary.completed_count,
                "Completed",
                "Sections successfully validated",
                "#E6F7EE",
                "#1C9457",
                "✓",
            )
        )
        self.stats_row.addWidget(
            StatCard(
                summary.pending_count,
                "Pending",
                "Sections waiting to be started",
                "#FFF4E5",
                "#B76E00",
                "⚠",
            )
        )

        self._clear_layout(self.work_card.body)
        for item in summary.work_items:
            row = WorkItemRow(item)
            row.open_clicked.connect(self.section_open_requested.emit)
            self.work_card.add_row(row)
        if not summary.work_items:
            self.work_card.add_row(self._empty_state("No sections assigned yet."))

        self._clear_layout(self.activity_card.body)
        for item in summary.activity_items:
            self.activity_card.add_row(ActivityRow(item))
        if not summary.activity_items:
            self.activity_card.add_row(self._empty_state("No recent activity."))

    def set_active_nav(self, key: str):
        self.sidebar.set_active(key)

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    @staticmethod
    def _empty_state(text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet("color: #8A94A6; font-size: 12px; padding: 12px 0;")
        return label


# --------------------------------------------------------------------------- #
# Manual smoke test: `python -m app.ui.pages.projects.dashboard_screen`
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    demo_summary = DashboardSummary(
        user_name="Anwer",
        user_role="Collaborator",
        project_name="Project Cahier des Charges Capgemini",
        project_status="Active",
        in_progress_count=4,
        completed_count=7,
        pending_count=2,
        work_items=[
            WorkItem("Introduction", "Cahier des charges", "in_progress", "sec-1"),
            WorkItem("Functional Requirements", "Cahier des charges", "pending", "sec-2"),
            WorkItem("Technical Architecture", "Cahier des charges", "completed", "sec-3"),
        ],
        activity_items=[
            ActivityItem('Section "Introduction" assigned', "Today · 10:42 AM", "assigned"),
            ActivityItem("Requirements completed", "Yesterday · 04:20 PM", "completed"),
            ActivityItem("Document updated", "Yesterday · 02:05 PM", "updated"),
            ActivityItem("New comment added", "Yesterday · 11:32 AM", "comment"),
        ],
    )

    window = DashboardScreen()
    window.load_summary(demo_summary)
    window.resize(1100, 700)
    window.setWindowTitle("Dashboard - Preview")
    window.show()

    sys.exit(app.exec())