from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QFrame,
    QScrollArea,
)

from app.ui.services.section_service import section_service


class SectionCard(QFrame):

    open_requested = Signal(int)

    def __init__(self, section, parent=None):
        super().__init__(parent)

        self.section = section

        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        header = QHBoxLayout()

        title = QLabel(section.title)
        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 15px;
                font-weight: 700;
                border: none;
            }
            """
        )

        header.addWidget(title)
        header.addStretch()

        status = QLabel(self._status_label(section.status))
        status.setStyleSheet(
            self._status_style(section.status)
        )

        header.addWidget(status)

        layout.addLayout(header)

        document_label = QLabel(
            f"Document ID: {section.document_id}"
        )

        document_label.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 12px;
                border: none;
            }
            """
        )

        layout.addWidget(document_label)

        module_label = QLabel(
            f"Module: {section.module}"
        )

        module_label.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 11px;
                border: none;
            }
            """
        )

        layout.addWidget(module_label)

        lock_label = QLabel(
            "Locked" if section.is_locked else "Available"
        )

        lock_label.setStyleSheet(
            """
            QLabel {
                color: #B42318;
                font-size: 11px;
                font-weight: 600;
                border: none;
            }
            """
            if section.is_locked
            else
            """
            QLabel {
                color: #1C9457;
                font-size: 11px;
                font-weight: 600;
                border: none;
            }
            """
        )

        layout.addWidget(lock_label)

        footer = QHBoxLayout()
        footer.addStretch()

        open_button = QPushButton(
            "View Section"
            if section.is_locked
            else "Open Section"
        )

        open_button.setCursor(Qt.PointingHandCursor)

        open_button.setStyleSheet(
            """
            QPushButton {
                color: white;
                background-color: #1E4FD6;
                border: none;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #173FB0;
            }
            """
        )

        open_button.clicked.connect(
            lambda: self.open_requested.emit(section.id)
        )

        footer.addWidget(open_button)

        layout.addLayout(footer)

    @staticmethod
    def _status_label(status):
        labels = {
            "pending": "PENDING",
            "in_progress": "IN PROGRESS",
            "pending_validation": "PENDING VALIDATION",
            "validated": "VALIDATED",
            "rejected": "REJECTED",
        }

        return labels.get(
            str(status).lower(),
            str(status).upper(),
        )

    @staticmethod
    def _status_style(status):
        status = str(status).lower()

        if status == "validated":
            return """
            QLabel {
                color: #1C9457;
                background-color: #E8F7EF;
                border-radius: 8px;
                padding: 4px 8px;
                font-size: 10px;
                font-weight: 700;
                border: none;
            }
            """

        if status == "rejected":
            return """
            QLabel {
                color: #B42318;
                background-color: #FEE4E2;
                border-radius: 8px;
                padding: 4px 8px;
                font-size: 10px;
                font-weight: 700;
                border: none;
            }
            """

        if status == "pending":
            return """
            QLabel {
                color: #B54708;
                background-color: #FEF0C7;
                border-radius: 8px;
                padding: 4px 8px;
                font-size: 10px;
                font-weight: 700;
                border: none;
            }
            """

        return """
        QLabel {
            color: #3E63DD;
            background-color: #E8F0FE;
            border-radius: 8px;
            padding: 4px 8px;
            font-size: 10px;
            font-weight: 700;
            border: none;
        }
        """


class MySectionsScreen(QWidget):

    back_requested = Signal()
    section_open_requested = Signal(int)

    def __init__(self, project=None, user=None, parent=None):
        super().__init__(parent)

        self.project = project
        self.user = user
        self.sections = []
        self.filtered_sections = []

        self.setStyleSheet(
            """
            QWidget {
                background-color: #F7F8FA;
            }
            """
        )

        self._build_ui()
        self.load_sections()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(18)

        header_layout = QHBoxLayout()

        back_button = QPushButton("← Dashboard")
        back_button.setCursor(Qt.PointingHandCursor)

        back_button.setStyleSheet(
            """
            QPushButton {
                color: #3E63DD;
                background-color: transparent;
                border: none;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                text-decoration: underline;
            }
            """
        )

        back_button.clicked.connect(
            self.back_requested.emit
        )

        header_layout.addWidget(back_button)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        title = QLabel("My Sections")

        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 24px;
                font-weight: 700;
                border: none;
            }
            """
        )

        main_layout.addWidget(title)

        self.subtitle = QLabel(
            "View and manage the sections assigned to you."
        )

        self.subtitle.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
                border: none;
            }
            """
        )

        main_layout.addWidget(self.subtitle)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search sections..."
        )

        self.search_input.setStyleSheet(
            """
            QLineEdit {
                background-color: white;
                border: 1px solid #D8DCE5;
                border-radius: 7px;
                padding: 9px 12px;
                font-size: 12px;
            }

            QLineEdit:focus {
                border: 1px solid #3E63DD;
            }
            """
        )

        self.search_input.textChanged.connect(
            self._apply_filters
        )

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(
            self.search_input,
            1,
        )

        self.status_filter = QComboBox()

        self.status_filter.addItems(
            [
                "All",
                "Pending",
                "In Progress",
                "Pending Validation",
                "Validated",
                "Rejected",
            ]
        )

        self.status_filter.setStyleSheet(
            """
            QComboBox {
                background-color: white;
                border: 1px solid #D8DCE5;
                border-radius: 7px;
                padding: 8px 12px;
                font-size: 12px;
            }
            """
        )

        self.status_filter.currentTextChanged.connect(
            self._apply_filters
        )

        filter_layout.addWidget(
            self.status_filter
        )

        main_layout.addLayout(filter_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            """
        )

        self.container = QWidget()

        self.sections_layout = QVBoxLayout(
            self.container
        )

        self.sections_layout.setContentsMargins(
            0, 0, 0, 0
        )

        self.sections_layout.setSpacing(10)

        self.scroll.setWidget(self.container)

        main_layout.addWidget(
            self.scroll,
            1,
        )

    def load_sections(self):
        self._show_loading()

        try:
            self.sections = section_service.get_my_sections()
            self.filtered_sections = list(self.sections)

            self._update_counter()
            self._display_sections()

        except Exception:
            self._show_error()

    def _apply_filters(self):
        search = self.search_input.text().strip().lower()
        selected_status = self.status_filter.currentText()

        status_mapping = {
            "Pending": "pending",
            "In Progress": "in_progress",
            "Pending Validation": "pending_validation",
            "Validated": "validated",
            "Rejected": "rejected",
        }

        filtered = []

        for section in self.sections:

            matches_search = (
                not search
                or search in section.title.lower()
                or search in section.module.lower()
            )

            matches_status = (
                selected_status == "All"
                or section.status.lower()
                == status_mapping[selected_status]
            )

            if matches_search and matches_status:
                filtered.append(section)

        self.filtered_sections = filtered
        self._display_sections()

    def _display_sections(self):
        self._clear_sections()

        if not self.filtered_sections:
            if self.sections:
                self._show_no_results()
            else:
                self._show_empty()

            return

        for section in self.filtered_sections:
            card = SectionCard(section)

            card.open_requested.connect(
                self.section_open_requested.emit
            )

            self.sections_layout.addWidget(card)

        self.sections_layout.addStretch()

    def _update_counter(self):
        count = len(self.sections)

        self.subtitle.setText(
            f"{count} section{'s' if count != 1 else ''} assigned"
        )

    def _show_loading(self):
        self._clear_sections()

        loading = QLabel(
            "Loading your sections..."
        )

        loading.setAlignment(Qt.AlignCenter)

        loading.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
                padding: 40px;
            }
            """
        )

        self.sections_layout.addWidget(loading)

    def _show_empty(self):
        self._clear_sections()

        empty = QLabel(
            "No sections assigned yet\n\n"
            "Your assigned sections will appear here "
            "once they are assigned to you."
        )

        empty.setAlignment(Qt.AlignCenter)

        empty.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
                padding: 40px;
            }
            """
        )

        self.sections_layout.addWidget(empty)

    def _show_no_results(self):
        self._clear_sections()

        empty = QLabel(
            "No sections found\n\n"
            "Try another search or clear your filters."
        )

        empty.setAlignment(Qt.AlignCenter)

        empty.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
                padding: 40px;
            }
            """
        )

        self.sections_layout.addWidget(empty)

    def _show_error(self):
        self._clear_sections()

        error = QLabel(
            "Unable to load your sections\n\n"
            "Something went wrong while loading your assigned sections."
        )

        error.setAlignment(Qt.AlignCenter)
        error.setWordWrap(True)

        error.setStyleSheet(
            """
            QLabel {
                color: #B42318;
                font-size: 13px;
                padding: 40px;
            }
            """
        )

        self.sections_layout.addWidget(error)

        retry_button = QPushButton("Retry")
        retry_button.setCursor(Qt.PointingHandCursor)

        retry_button.setStyleSheet(
            """
            QPushButton {
                color: white;
                background-color: #1E4FD6;
                border: none;
                border-radius: 7px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 600;
            }
            """
        )

        retry_button.clicked.connect(
            self.load_sections
        )

        self.sections_layout.addWidget(
            retry_button,
            alignment=Qt.AlignCenter,
        )

    def _clear_sections(self):
        while self.sections_layout.count():
            item = self.sections_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()