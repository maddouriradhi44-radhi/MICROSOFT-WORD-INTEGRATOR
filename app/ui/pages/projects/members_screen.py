import requests

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QScrollArea,
    QMessageBox,
    QComboBox,
    QInputDialog,
)

from api.api_client import api_client


class MembersScreen(QWidget):

    back_requested = Signal()

    def __init__(self, project=None, user=None, parent=None):
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

    # ==========================================================
    # UI
    # ==========================================================

    def _build_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # ---------------- HEADER ----------------

        header = QHBoxLayout()

        titles = QVBoxLayout()

        title = QLabel("Members")
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
            "Manage project members and their roles"
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
            }
            """
        )

        titles.addWidget(title)
        titles.addWidget(subtitle)

        header.addLayout(titles)
        header.addStretch()

        # ADD MEMBER

        add_button = QPushButton("+ Add Member")
        add_button.setFixedHeight(36)
        add_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3E63DD;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 16px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #3154C6;
            }
            """
        )

        add_button.clicked.connect(self._add_member_dialog)

        header.addWidget(add_button)

        # REFRESH

        refresh_button = QPushButton("Refresh")
        refresh_button.setFixedHeight(36)
        refresh_button.clicked.connect(self._load_members)

        header.addWidget(refresh_button)

        # BACK

        back = QPushButton("Back")
        back.setFixedHeight(36)

        back.clicked.connect(
            self.back_requested.emit
        )

        header.addWidget(back)

        layout.addLayout(header)

        # ---------------- MEMBERS CONTAINER ----------------

        container = QFrame()

        container.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            """
        )

        container_layout = QVBoxLayout(container)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()

        self.members_layout = QVBoxLayout(content)
        self.members_layout.setSpacing(10)
        self.members_layout.setContentsMargins(
            15, 15, 15, 15
        )

        scroll.setWidget(content)

        container_layout.addWidget(scroll)

        layout.addWidget(container, 1)

        self.setLayout(layout)

        # LOAD REAL MEMBERS

        self._load_members()

    # ==========================================================
    # PROJECT ID
    # ==========================================================

    def _get_project_id(self):

        if self.project is None:
            return None

        if isinstance(self.project, dict):
            return (
                self.project.get("id")
                or self.project.get("project_id")
            )

        return getattr(
            self.project,
            "id",
            None,
        ) or getattr(
            self.project,
            "project_id",
            None,
        )

    # ==========================================================
    # LOAD MEMBERS
    # ==========================================================

    def _load_members(self):

        project_id = self._get_project_id()

        if not project_id:
            self._show_error(
                "Project ID is missing."
            )
            return

        self._clear_members()

        try:

            response = api_client.get(
                f"/projects/{project_id}/members"
            )

        except requests.exceptions.ConnectionError:

            self._show_error(
                "Unable to connect to the server."
            )
            return

        except requests.exceptions.Timeout:

            self._show_error(
                "The server took too long to respond."
            )
            return

        except requests.exceptions.RequestException as exc:

            self._show_error(
                f"Network error: {exc}"
            )
            return

        if response.status_code == 401:

            self._show_error(
                "Your authentication session has expired."
            )
            return

        if response.status_code != 200:

            try:
                detail = response.json().get(
                    "detail",
                    "Unable to load project members."
                )
            except Exception:
                detail = (
                    "Unable to load project members."
                )

            self._show_error(
                f"{detail}"
            )
            return

        try:
            members = response.json()
        except ValueError:

            self._show_error(
                "The server returned an invalid response."
            )
            return

        if not isinstance(members, list):

            self._show_error(
                "Invalid members response."
            )
            return

        if not members:

            empty = QLabel(
                "No members in this project."
            )

            empty.setStyleSheet(
                """
                QLabel {
                    color: #6B7280;
                    font-size: 14px;
                    padding: 30px;
                }
                """
            )

            empty.setAlignment(
                Qt.AlignCenter
            )

            self.members_layout.addWidget(
                empty
            )

            return

        for member in members:
            self._create_member_card(
                member
            )

        self.members_layout.addStretch()

    # ==========================================================
    # MEMBER CARD
    # ==========================================================

    def _create_member_card(self, member):

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
        row.setContentsMargins(
            15, 12, 15, 12
        )

        # USER INFO

        user_id = member.get(
            "user_id",
            member.get("id")
        )

        first_name = member.get("first_name") or member.get("prenom") or ""
        last_name = member.get("last_name") or member.get("nom") or ""

        name = f"{first_name} {last_name}".strip()

        if not name:
            name = member.get("name") or member.get("email") or f"User {user_id}"

        email = member.get(
            "email",
            ""
        )

        info = QVBoxLayout()

        name_label = QLabel(name)

        name_label.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 14px;
                font-weight: 600;
                border: none;
            }
            """
        )

        info.addWidget(name_label)

        if email:

            email_label = QLabel(email)

            email_label.setStyleSheet(
                """
                QLabel {
                    color: #6B7280;
                    font-size: 12px;
                    border: none;
                }
                """
            )

            info.addWidget(email_label)

        row.addLayout(info)

        row.addStretch()

        # ROLE

        role = (
            member.get("role")
            or member.get("project_role")
            or "UNKNOWN"
        )

        role_text = str(role)

        role_label = QLabel(
            role_text
        )

        role_label.setStyleSheet(
            """
            QLabel {
                color: #3E63DD;
                background-color: #EEF2FF;
                border: none;
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 11px;
                font-weight: 600;
            }
            """
        )

        row.addWidget(role_label)

        # CHANGE ROLE

        change_button = QPushButton(
            "Role"
        )

        change_button.setFixedHeight(30)

        change_button.clicked.connect(
            lambda checked=False,
            uid=user_id,
            current=role:
            self._change_role(
                uid,
                current
            )
        )

        row.addWidget(
            change_button
        )

        # REMOVE

        remove_button = QPushButton(
            "Remove"
        )

        remove_button.setFixedHeight(30)

        remove_button.setStyleSheet(
            """
            QPushButton {
                color: #DC2626;
                background-color: #FEF2F2;
                border: 1px solid #FECACA;
                border-radius: 6px;
                padding: 0 10px;
            }

            QPushButton:hover {
                background-color: #FEE2E2;
            }
            """
        )

        remove_button.clicked.connect(
            lambda checked=False,
            uid=user_id:
            self._remove_member(uid)
        )

        row.addWidget(
            remove_button
        )

        self.members_layout.addWidget(
            card
        )

    # ==========================================================
    # ADD MEMBER
    # ==========================================================

    def _add_member_dialog(self):

        project_id = self._get_project_id()

        if not project_id:
            return

        email, ok = QInputDialog.getText(
            self,
            "Add Member",
            "Member email:"
        )

        if not ok or not email.strip():
            return

        roles = [
            "COLLABORATOR",
            "READER",
        ]

        role, ok = QInputDialog.getItem(
            self,
            "Member Role",
            "Role:",
            roles,
            0,
            False,
        )

        if not ok:
            return

        try:

            response = api_client.post(
                f"/projects/{project_id}/members",
                json={
                    "email": email.strip(),
                    "role": role,
                },
            )

        except requests.exceptions.RequestException:

            self._show_error(
                "Unable to connect to the server."
            )
            return

        if response.status_code not in (
            200,
            201,
        ):

            try:
                detail = response.json().get(
                    "detail",
                    "Unable to add member."
                )
            except Exception:
                detail = "Unable to add member."

            self._show_error(
                str(detail)
            )
            return

        QMessageBox.information(
            self,
            "Member Added",
            "The member was added successfully."
        )

        self._load_members()

    # ==========================================================
    # CHANGE ROLE
    # ==========================================================

    def _change_role(
        self,
        user_id,
        current_role,
    ):

        project_id = self._get_project_id()

        if not project_id or not user_id:
            return

        roles = [
            "PROJECT_MANAGER",
            "COLLABORATOR",
            "READER",
        ]

        current_role = str(
            current_role
        )

        index = (
            roles.index(current_role)
            if current_role in roles
            else 0
        )

        role, ok = QInputDialog.getItem(
            self,
            "Change Member Role",
            "New role:",
            roles,
            index,
            False,
        )

        if not ok:
            return

        try:

            response = api_client.put(
                f"/projects/{project_id}/members/{user_id}",
                json={
                    "role": role,
                },
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
                    "Unable to update member role."
                )
            except Exception:
                detail = (
                    "Unable to update member role."
                )

            self._show_error(
                str(detail)
            )
            return

        self._load_members()

    # ==========================================================
    # REMOVE MEMBER
    # ==========================================================

    def _remove_member(
        self,
        user_id,
    ):

        project_id = self._get_project_id()

        if not project_id or not user_id:
            return

        answer = QMessageBox.question(
            self,
            "Remove Member",
            "Are you sure you want to remove this member?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        try:

            response = api_client.delete(
                f"/projects/{project_id}/members/{user_id}"
            )

        except requests.exceptions.RequestException:

            self._show_error(
                "Unable to connect to the server."
            )
            return

        if response.status_code not in (
            200,
            204,
        ):

            try:
                detail = response.json().get(
                    "detail",
                    "Unable to remove member."
                )
            except Exception:
                detail = "Unable to remove member."

            self._show_error(
                str(detail)
            )
            return

        self._load_members()

    # ==========================================================
    # HELPERS
    # ==========================================================

    def _clear_members(self):

        while self.members_layout.count():

            item = self.members_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    def _show_error(self, message):

        QMessageBox.warning(
            self,
            "Members",
            message,
        )