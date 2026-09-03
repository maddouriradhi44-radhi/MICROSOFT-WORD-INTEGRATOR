from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QMessageBox,
    QScrollArea,
    QInputDialog,
)

import requests


class ValidationScreen(QWidget):

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

            QPushButton {
                padding: 8px 14px;
                border-radius: 6px;
                font-size: 13px;
            }
            """
        )

        self._build_ui()
        self.load_validations()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = QHBoxLayout()

        titles = QVBoxLayout()

        title = QLabel("Validation")
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
            "Review sections waiting for validation"
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

        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.load_validations)

        back = QPushButton("Back")
        back.clicked.connect(self.back_requested.emit)

        header.addWidget(refresh)
        header.addWidget(back)

        layout.addLayout(header)

        # -----------------------------------------------------
        # Scroll area
        # -----------------------------------------------------

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.container = QWidget()

        self.validation_layout = QVBoxLayout()
        self.validation_layout.setSpacing(12)
        self.validation_layout.setContentsMargins(0, 0, 0, 0)

        self.container.setLayout(self.validation_layout)

        self.scroll.setWidget(self.container)

        layout.addWidget(self.scroll)

        self.setLayout(layout)

    # =========================================================
    # API
    # =========================================================

    def _get_base_url(self):
        return "http://127.0.0.1:8000"

    def _get_token(self):
        if self.user is None:
            return None

        if isinstance(self.user, dict):
            return (
                self.user.get("access_token")
                or self.user.get("token")
            )

        return getattr(
            self.user,
            "access_token",
            None,
        )

    def _get_headers(self):

        token = self._get_token()

        if not token:
            return {}

        return {
            "Authorization": f"Bearer {token}"
        }

    # =========================================================
    # Load validations
    # =========================================================

    def load_validations(self):

        self._clear_validation_cards()

        if self.project is None:
            self._show_message(
                "No project selected."
            )
            return

        project_id = self._get_project_id()

        if project_id is None:
            self._show_message(
                "Unable to determine project."
            )
            return

        # -----------------------------------------------------
        # We first load project sections.
        # Then we load validation history for each section.
        # -----------------------------------------------------

        try:

            response = requests.get(
                f"{self._get_base_url()}/sections/project/{project_id}",
                headers=self._get_headers(),
                timeout=10,
            )

            if response.status_code != 200:
                self._show_message(
                    f"Unable to load sections ({response.status_code})."
                )
                return

            sections = response.json()

            found = False

            for section in sections:

                section_id = section.get("id")

                if section_id is None:
                    continue

                validation_response = requests.get(
                    f"{self._get_base_url()}/validations/section/{section_id}",
                    headers=self._get_headers(),
                    timeout=10,
                )

                if validation_response.status_code != 200:
                    continue

                validations = validation_response.json()

                for validation in validations:

                    status = (
                        validation.get("status")
                        or validation.get("decision")
                        or ""
                    ).lower()

                    # Only show validations that still need review.
                    if status in (
                        "pending",
                        "waiting",
                        "waiting_validation",
                        "en_attente",
                        "",
                    ):
                        found = True

                        self._add_validation_item(
                            validation=validation,
                            section=section,
                        )

            if not found:
                self._show_message(
                    "No sections are waiting for validation."
                )

            self.validation_layout.addStretch()

        except requests.RequestException as error:

            self._show_message(
                f"Connection error: {error}"
            )

    # =========================================================
    # Validation card
    # =========================================================

    def _add_validation_item(
        self,
        validation,
        section,
    ):

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

        # -----------------------------------------------------
        # Section information
        # -----------------------------------------------------

        info = QVBoxLayout()

        section_title = (
            section.get("title")
            or section.get("name")
            or "Untitled section"
        )

        label = QLabel(section_title)

        label.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 14px;
                font-weight: 600;
                border: none;
            }
            """
        )

        version_id = validation.get("version_id")

        version_label = QLabel(
            f"Version: {version_id if version_id is not None else '-'}"
        )

        version_label.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 12px;
                border: none;
            }
            """
        )

        info.addWidget(label)
        info.addWidget(version_label)

        row.addLayout(info)
        row.addStretch()

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        status_label = QLabel("Pending")

        status_label.setStyleSheet(
            """
            QLabel {
                color: #92400E;
                background-color: #FEF3C7;
                border: none;
                border-radius: 5px;
                padding: 5px 9px;
                font-size: 12px;
                font-weight: 600;
            }
            """
        )

        row.addWidget(status_label)

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        approve = QPushButton("Approve")
        reject = QPushButton("Reject")

        approve.clicked.connect(
            lambda: self.approve_validation(validation)
        )

        reject.clicked.connect(
            lambda: self.reject_validation(validation)
        )

        row.addWidget(approve)
        row.addWidget(reject)

        self.validation_layout.addWidget(card)

    # =========================================================
    # Approve
    # =========================================================

    def approve_validation(self, validation):

        validation_id = validation.get("id")

        if validation_id is None:
            QMessageBox.warning(
                self,
                "Validation",
                "Validation ID is missing.",
            )
            return

        reply = QMessageBox.question(
            self,
            "Approve validation",
            "Are you sure you want to approve this version?",
        )

        if reply != QMessageBox.Yes:
            return

        try:

            response = requests.patch(
                f"{self._get_base_url()}/validations/"
                f"{validation_id}/approve",
                headers=self._get_headers(),
                json={
                    "comment": None
                },
                timeout=10,
            )

            if response.status_code in (200, 204):

                QMessageBox.information(
                    self,
                    "Validation",
                    "Version approved successfully.",
                )

                self.load_validations()

            else:

                self._show_api_error(
                    response,
                    "Unable to approve validation.",
                )

        except requests.RequestException as error:

            QMessageBox.critical(
                self,
                "Connection error",
                str(error),
            )

    # =========================================================
    # Reject
    # =========================================================

    def reject_validation(self, validation):

        validation_id = validation.get("id")

        if validation_id is None:
            QMessageBox.warning(
                self,
                "Validation",
                "Validation ID is missing.",
            )
            return

        comment, ok = QInputDialog.getMultiLineText(
            self,
            "Reject validation",
            "Reason for rejection:",
        )

        if not ok:
            return

        if not comment.strip():
            QMessageBox.warning(
                self,
                "Reject validation",
                "A comment is required when rejecting.",
            )
            return

        try:

            response = requests.patch(
                f"{self._get_base_url()}/validations/"
                f"{validation_id}/reject",
                headers=self._get_headers(),
                json={
                    "comment": comment.strip()
                },
                timeout=10,
            )

            if response.status_code in (200, 204):

                QMessageBox.information(
                    self,
                    "Validation",
                    "Version rejected successfully.",
                )

                self.load_validations()

            else:

                self._show_api_error(
                    response,
                    "Unable to reject validation.",
                )

        except requests.RequestException as error:

            QMessageBox.critical(
                self,
                "Connection error",
                str(error),
            )

    # =========================================================
    # Helpers
    # =========================================================

    def _get_project_id(self):

        if isinstance(self.project, dict):
            return self.project.get("id")

        return getattr(
            self.project,
            "id",
            None,
        )

    def _clear_validation_cards(self):

        while self.validation_layout.count():

            item = self.validation_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _show_message(self, message):

        label = QLabel(message)

        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 14px;
                padding: 30px;
                border: none;
            }
            """
        )

        self.validation_layout.addWidget(label)

    def _show_api_error(
        self,
        response,
        default_message,
    ):

        try:
            data = response.json()
            detail = data.get("detail", default_message)
        except Exception:
            detail = default_message

        QMessageBox.warning(
            self,
            "Validation",
            str(detail),
        )