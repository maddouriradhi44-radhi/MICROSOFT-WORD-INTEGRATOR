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

from services.section_service import section_service


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

        # ======================================================
        # HEADER
        # ======================================================

        header = QHBoxLayout()

        title = QLabel(
            section.title
        )

        title.setWordWrap(True)

        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 15px;
                font-weight: 700;
                border: none;
                background-color: transparent;
            }
            """
        )

        header.addWidget(
            title,
            1,
        )

        status = QLabel(
            self._status_label(
                section.status
            )
        )

        status.setStyleSheet(
            self._status_style(
                section.status
            )
        )

        header.addWidget(
            status
        )

        layout.addLayout(
            header
        )

        # ======================================================
        # DOCUMENT
        # ======================================================

        document_label = QLabel(
            f"Document ID: {section.document_id}"
        )

        document_label.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 12px;
                border: none;
                background-color: transparent;
            }
            """
        )

        layout.addWidget(
            document_label
        )

        # ======================================================
        # MODULE
        # ======================================================

        module_label = QLabel(
            f"Module: {section.module}"
        )

        module_label.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 11px;
                border: none;
                background-color: transparent;
            }
            """
        )

        layout.addWidget(
            module_label
        )

        # ======================================================
        # WORKFLOW STATUS
        # ======================================================

        workflow_label = QLabel(
            self._workflow_message(
                section
            )
        )

        workflow_label.setWordWrap(True)

        workflow_label.setStyleSheet(
            self._workflow_style(
                section
            )
        )

        layout.addWidget(
            workflow_label
        )

        # ======================================================
        # FOOTER
        # ======================================================

        footer = QHBoxLayout()

        footer.addStretch()

        open_button = QPushButton(
            self._button_text(
                section
            )
        )

        open_button.setCursor(
            Qt.PointingHandCursor
        )

        open_button.setStyleSheet(
            self._button_style(
                section
            )
        )

        open_button.clicked.connect(
            lambda: self.open_requested.emit(
                section.id
            )
        )

        footer.addWidget(
            open_button
        )

        layout.addLayout(
            footer
        )

    # ==========================================================
    # STATUS LABEL
    # ==========================================================

    @staticmethod
    def _status_label(status):

        labels = {
            "pending": "PENDING",
            "in_progress": "IN PROGRESS",
            "pending_validation": "PENDING VALIDATION",
            "validated": "VALIDATED",
            "rejected": "REJECTED",
        }

        normalized_status = str(
            status
        ).lower()

        return labels.get(
            normalized_status,
            str(status).upper(),
        )

    # ==========================================================
    # STATUS STYLE
    # ==========================================================

    @staticmethod
    def _status_style(status):

        status = str(
            status
        ).lower()

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

        if status == "pending_validation":

            return """
            QLabel {
                color: #6941C6;
                background-color: #F4EBFF;
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

    # ==========================================================
    # WORKFLOW MESSAGE
    # ==========================================================

    @staticmethod
    def _workflow_message(section):

        status = str(
            section.status
        ).lower()

        if getattr(
            section,
            "is_locked",
            False,
        ):
            return (
                "This section is currently locked. "
                "You can view its workspace, but editing "
                "is temporarily unavailable."
            )

        if status == "pending_validation":
            return (
                "The latest modification is waiting "
                "for validation."
            )

        if status == "validated":
            return (
                "This section has been validated."
            )

        if status == "rejected":
            return (
                "The latest modification was rejected. "
                "Open the section to review it."
            )

        if status == "in_progress":
            return (
                "This section is assigned to you. "
                "Modification is performed in Microsoft Word."
            )

        return (
            "This section is assigned to you. "
            "Open the workspace to start working."
        )

    # ==========================================================
    # WORKFLOW MESSAGE STYLE
    # ==========================================================

    @staticmethod
    def _workflow_style(section):

        if getattr(
            section,
            "is_locked",
            False,
        ):

            return """
            QLabel {
                color: #B42318;
                background-color: #FEF3F2;
                border: none;
                border-radius: 6px;
                padding: 7px 9px;
                font-size: 11px;
            }
            """

        status = str(
            section.status
        ).lower()

        if status == "pending_validation":

            return """
            QLabel {
                color: #6941C6;
                background-color: #F9F5FF;
                border: none;
                border-radius: 6px;
                padding: 7px 9px;
                font-size: 11px;
            }
            """

        if status == "validated":

            return """
            QLabel {
                color: #067647;
                background-color: #ECFDF3;
                border: none;
                border-radius: 6px;
                padding: 7px 9px;
                font-size: 11px;
            }
            """

        return """
        QLabel {
            color: #475467;
            background-color: #F8FAFC;
            border: none;
            border-radius: 6px;
            padding: 7px 9px;
            font-size: 11px;
        }
        """

    # ==========================================================
    # BUTTON TEXT
    # ==========================================================

    @staticmethod
    def _button_text(section):

        if getattr(
            section,
            "is_locked",
            False,
        ):
            return "View Section"

        status = str(
            section.status
        ).lower()

        if status == "pending_validation":
            return "View Section"

        return "Open Section"

    # ==========================================================
    # BUTTON STYLE
    # ==========================================================

    @staticmethod
    def _button_style(section):

        if getattr(
            section,
            "is_locked",
            False,
        ):

            return """
            QPushButton {
                color: #344054;
                background-color: #EAECF0;
                border: none;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #D0D5DD;
            }
            """

        status = str(
            section.status
        ).lower()

        if status == "pending_validation":

            return """
            QPushButton {
                color: white;
                background-color: #6941C6;
                border: none;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #53389E;
            }
            """

        return """
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


class MySectionsScreen(QWidget):

    back_requested = Signal()
    section_open_requested = Signal(int)

    def __init__(
        self,
        project=None,
        user=None,
        parent=None,
    ):
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

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def _build_ui(self):

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        main_layout.setSpacing(
            18
        )

        # ======================================================
        # HEADER
        # ======================================================

        header_layout = QHBoxLayout()

        back_button = QPushButton(
            "← Dashboard"
        )

        back_button.setCursor(
            Qt.PointingHandCursor
        )

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

        header_layout.addWidget(
            back_button
        )

        header_layout.addStretch()

        main_layout.addLayout(
            header_layout
        )

        # ======================================================
        # TITLE
        # ======================================================

        title = QLabel(
            "My Sections"
        )

        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 24px;
                font-weight: 700;
                border: none;
                background-color: transparent;
            }
            """
        )

        main_layout.addWidget(
            title
        )

        # ======================================================
        # SUBTITLE
        # ======================================================

        self.subtitle = QLabel(
            "View your assigned sections and work on them "
            "through Microsoft Word."
        )

        self.subtitle.setWordWrap(
            True
        )

        self.subtitle.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
                border: none;
                background-color: transparent;
            }
            """
        )

        main_layout.addWidget(
            self.subtitle
        )

        # ======================================================
        # SEARCH
        # ======================================================

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

        # ======================================================
        # STATUS FILTER
        # ======================================================

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

            QComboBox:focus {
                border: 1px solid #3E63DD;
            }
            """
        )

        self.status_filter.currentTextChanged.connect(
            self._apply_filters
        )

        filter_layout.addWidget(
            self.status_filter
        )

        main_layout.addLayout(
            filter_layout
        )

        # ======================================================
        # SECTIONS SCROLL AREA
        # ======================================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

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
            0,
            0,
            0,
            0,
        )

        self.sections_layout.setSpacing(
            10
        )

        self.scroll.setWidget(
            self.container
        )

        self.container.setVisible(True)
        self.scroll.setVisible(True)

        main_layout.addWidget(
            self.scroll,
            1,
        )

    # ==========================================================
    # LOAD SECTIONS
    # ==========================================================

    def load_sections(self):

        self._show_loading()

        try:

            all_sections = (
                section_service.get_my_sections()
            )

            current_project_id = (
                self.project.id
                if self.project is not None
                else None
            )

            self.sections = [
                section
                for section in all_sections
                if (
                    current_project_id is not None
                    and section.project_id == current_project_id
                )
            ]

            print("\n========== MY SECTIONS DEBUG ==========")
            print(
                "CURRENT PROJECT:",
                self.project,
            )
            print(
                "CURRENT PROJECT ID:",
                current_project_id,
            )
            print(
                "ALL ASSIGNED SECTIONS:",
                len(all_sections),
            )

            for section in all_sections:
                print(
                    f"SECTION: {section.id} | "
                    f"TITLE: {section.title} | "
                    f"PROJECT: {section.project_id} | "
                    f"ASSIGNED: {section.assigned_user_id}"
                )

            print(
                "FILTERED SECTIONS:",
                len(self.sections),
            )

            for section in self.sections:
                print(
                    f"VISIBLE: {section.id} | "
                    f"{section.title} | "
                    f"PROJECT: {section.project_id}"
                )

            print("========================================\n")

            self.filtered_sections = list(
                self.sections
            )

            self._update_counter()

            self._display_sections()

        except Exception:
            self._show_error()
    # ==========================================================
    # FILTERS
    # ==========================================================

    def _apply_filters(self):

        search = (
            self.search_input
            .text()
            .strip()
            .lower()
        )

        selected_status = (
            self.status_filter.currentText()
        )

        status_mapping = {
            "Pending": "pending",
            "In Progress": "in_progress",
            "Pending Validation": "pending_validation",
            "Validated": "validated",
            "Rejected": "rejected",
        }

        filtered = []

        for section in self.sections:

            title = str(
                getattr(
                    section,
                    "title",
                    "",
                )
            ).lower()

            module = str(
                getattr(
                    section,
                    "module",
                    "",
                )
            ).lower()

            status = str(
                getattr(
                    section,
                    "status",
                    "",
                )
            ).lower()

            matches_search = (
                not search
                or search in title
                or search in module
            )

            matches_status = (
                selected_status == "All"
                or status
                == status_mapping[
                    selected_status
                ]
            )

            if (
                matches_search
                and matches_status
            ):
                filtered.append(
                    section
                )

        self.filtered_sections = filtered

        self._display_sections()

    # ==========================================================
    # DISPLAY SECTIONS
    # ==========================================================

    def _display_sections(self):

        print("\n========== DISPLAY SECTIONS ==========")
        print(
            "NUMBER OF SECTIONS TO DISPLAY:",
            len(self.filtered_sections),
        )

        self._clear_sections()

        if not self.filtered_sections:

            print("NOTHING TO DISPLAY")

            if self.sections:
                self._show_no_results()
            else:
                self._show_empty()

            return

        for section in self.filtered_sections:

            print(
                f"CREATING CARD -> "
                f"ID: {section.id} | "
                f"TITLE: {section.title}"
            )

            card = SectionCard(
                section
            )

            card.open_requested.connect(
                self.section_open_requested.emit
            )

            self.sections_layout.addWidget(
                card
            )

        self.sections_layout.addStretch()

    # ==========================================================
    # COUNTER
    # ==========================================================

    def _update_counter(self):

        count = len(
            self.sections
        )

        self.subtitle.setText(
            f"{count} section"
            f"{'s' if count != 1 else ''} assigned. "
            "Open a section to work through Microsoft Word."
        )

    # ==========================================================
    # LOADING
    # ==========================================================

    def _show_loading(self):

        self._clear_sections()

        loading = QLabel(
            "Loading your sections..."
        )

        loading.setAlignment(
            Qt.AlignCenter
        )

        loading.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
                padding: 40px;
            }
            """
        )

        self.sections_layout.addWidget(
            loading
        )

    # ==========================================================
    # EMPTY
    # ==========================================================

    def _show_empty(self):

        self._clear_sections()

        empty = QLabel(
            "No sections assigned yet\n\n"
            "Your assigned sections will appear here "
            "once they are assigned to you."
        )

        empty.setAlignment(
            Qt.AlignCenter
        )

        empty.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
                padding: 40px;
            }
            """
        )

        self.sections_layout.addWidget(
            empty
        )

    # ==========================================================
    # NO RESULTS
    # ==========================================================

    def _show_no_results(self):

        self._clear_sections()

        empty = QLabel(
            "No sections found\n\n"
            "Try another search or clear your filters."
        )

        empty.setAlignment(
            Qt.AlignCenter
        )

        empty.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
                padding: 40px;
            }
            """
        )

        self.sections_layout.addWidget(
            empty
        )

    # ==========================================================
    # ERROR
    # ==========================================================

    def _show_error(self):

        self._clear_sections()

        error = QLabel(
            "Unable to load your sections\n\n"
            "Something went wrong while loading "
            "your assigned sections."
        )

        error.setAlignment(
            Qt.AlignCenter
        )

        error.setWordWrap(
            True
        )

        error.setStyleSheet(
            """
            QLabel {
                color: #B42318;
                font-size: 13px;
                padding: 40px;
            }
            """
        )

        self.sections_layout.addWidget(
            error
        )

        retry_button = QPushButton(
            "Retry"
        )

        retry_button.setCursor(
            Qt.PointingHandCursor
        )

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

            QPushButton:hover {
                background-color: #173FB0;
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

    # ==========================================================
    # CLEAR
    # ==========================================================

    def _clear_sections(self):

        while self.sections_layout.count():

            item = (
                self.sections_layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()