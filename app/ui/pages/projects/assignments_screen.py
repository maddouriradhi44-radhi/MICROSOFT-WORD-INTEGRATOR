import requests

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QComboBox,
    QMessageBox,
    QScrollArea,
)

from api.api_client import api_client


class AssignmentsScreen(QWidget):

    back_requested = Signal()

    def __init__(self, project=None, user=None, parent=None):
        super().__init__(parent)

        self.project = project
        self.user = user
        self.members = []

        self.setStyleSheet(
            """
            QWidget {
                background-color: #F7F8FA;
            }
            """
        )

        self._build_ui()
        self._load_data()

    def _build_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel("Assignments")
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
            "Assign project sections to collaborators"
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

        header.addLayout(title_layout)
        header.addStretch()

        refresh = QPushButton("Refresh")
        refresh.setFixedHeight(36)
        refresh.clicked.connect(self._load_data)
        header.addWidget(refresh)

        back = QPushButton("Back")
        back.setFixedHeight(36)
        back.clicked.connect(self.back_requested.emit)
        header.addWidget(back)

        layout.addLayout(header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        self.sections_layout = QVBoxLayout(content)
        self.sections_layout.setSpacing(10)
        self.sections_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll.setWidget(content)

        layout.addWidget(self.scroll, 1)

        self.setLayout(layout)

    def _get_project_id(self):
        if self.project is None:
            return None

        if isinstance(self.project, dict):
            return (
                self.project.get("id")
                or self.project.get("project_id")
            )

        return (
            getattr(self.project, "id", None)
            or getattr(self.project, "project_id", None)
        )

    def _load_data(self):

        project_id = self._get_project_id()

        if not project_id:
            self._show_error("Project ID is missing.")
            return

        self._clear_sections()

        try:
            members_response = api_client.get(
                f"/projects/{project_id}/members"
            )

            sections_response = api_client.get(
                f"/sections/project/{project_id}"
            )

        except requests.exceptions.RequestException:
            self._show_error(
                "Unable to connect to the server."
            )
            return

        if members_response.status_code != 200:
            self._show_error(
                "Unable to load project members."
            )
            return

        if sections_response.status_code != 200:
            self._show_error(
                "Unable to load project sections."
            )
            return

        try:
            self.members = members_response.json()
            sections = sections_response.json()
        except ValueError:
            self._show_error(
                "Invalid response from server."
            )
            return

        if not sections:
            label = QLabel("No sections found in this project.")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(
                """
                QLabel {
                    color: #6B7280;
                    font-size: 14px;
                    padding: 30px;
                }
                """
            )
            self.sections_layout.addWidget(label)
            return

        for section in sections:
            self._add_assignment(section)

        self.sections_layout.addStretch()

    def _add_assignment(self, section):

        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }
            """
        )

        row = QHBoxLayout(card)
        row.setContentsMargins(15, 12, 15, 12)

        info = QVBoxLayout()

        title = QLabel(
            section.get("title", "Untitled section")
        )
        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 14px;
                font-weight: 600;
                border: none;
            }
            """
        )

        status = section.get("status", "UNKNOWN")

        status_label = QLabel(
            f"Status: {status}"
        )
        status_label.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 11px;
                border: none;
            }
            """
        )

        info.addWidget(title)
        info.addWidget(status_label)

        row.addLayout(info)
        row.addStretch()

        combo = QComboBox()
        combo.setMinimumWidth(190)

        combo.addItem(
            "Not assigned",
            None
        )

        assigned_user_id = section.get(
            "assigned_user_id"
        )

        selected_index = 0

        for member in self.members:

            user_id = member.get(
                "user_id",
                member.get("id")
            )

            first_name = (
                member.get("first_name")
                or member.get("prenom")
                or ""
            )

            last_name = (
                member.get("last_name")
                or member.get("nom")
                or ""
            )

            name = f"{first_name} {last_name}".strip()

            if not name:
                name = (
                    member.get("email")
                    or f"User {user_id}"
                )

            combo.addItem(
                name,
                user_id
            )

            if user_id == assigned_user_id:
                selected_index = combo.count() - 1

        combo.setCurrentIndex(selected_index)

        combo.currentIndexChanged.connect(
            lambda index,
            sid=section.get("id"),
            cb=combo:
            self._assign_section(
                sid,
                cb.itemData(index)
            )
        )

        row.addWidget(combo)

        self.sections_layout.addWidget(card)

    def _assign_section(self, section_id, user_id):

        if not section_id:
            return

        if user_id is None:
            return

        try:
            response = api_client.put(
                f"/sections/{section_id}/assign/{user_id}"
            )
        except requests.exceptions.RequestException:
            self._show_error(
                "Unable to connect to the server."
            )
            return

        if response.status_code != 200:
            try:
                detail = response.json().get(
                    "detail",
                    "Unable to assign section."
                )
            except Exception:
                detail = "Unable to assign section."

            self._show_error(str(detail))
            self._load_data()
            return

        self._load_data()

    def _clear_sections(self):

        while self.sections_layout.count():

            item = self.sections_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    def _show_error(self, message):

        QMessageBox.warning(
            self,
            "Assignments",
            message,
        )