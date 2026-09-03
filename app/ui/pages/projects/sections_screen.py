from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QLineEdit,
    QScrollArea,
)


class SectionsScreen(QWidget):

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

    def _build_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        title = QLabel("Sections")
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
            "Manage the sections of your project"
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

        back_button = QPushButton("Back")
        back_button.setFixedHeight(36)
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(
            self.back_requested.emit
        )

        header.addWidget(back_button)

        main_layout.addLayout(header)

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search sections..."
        )
        self.search_input.setFixedHeight(40)

        self.search_input.setStyleSheet(
            """
            QLineEdit {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 0 12px;
                font-size: 13px;
            }

            QLineEdit:focus {
                border: 1px solid #3E63DD;
            }
            """
        )

        main_layout.addWidget(
            self.search_input
        )

        # Container
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
        container_layout.setContentsMargins(
            20, 20, 20, 20
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()

        self.sections_layout = QVBoxLayout(content)
        self.sections_layout.setSpacing(10)

        scroll.setWidget(content)

        container_layout.addWidget(scroll)

        main_layout.addWidget(
            container,
            1
        )

        self.setLayout(main_layout)

        self._load_sections()

    def _load_sections(self):

        self._clear_sections()

        # Temporary frontend state.
        # Backend integration will be connected
        # once the manager section endpoint is used.

        self._add_section(
            "Introduction",
            "Section",
            "Assigned",
        )

        self._add_section(
            "Project Requirements",
            "Section",
            "In progress",
        )

        self._add_section(
            "Technical Architecture",
            "Section",
            "Pending",
        )

    def _add_section(
        self,
        title,
        section_type,
        status,
    ):

        card = QFrame()

        card.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }
            """
        )

        layout = QHBoxLayout(card)
        layout.setContentsMargins(
            16, 14, 16, 14
        )

        text_layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 14px;
                font-weight: 600;
                border: none;
            }
            """
        )

        type_label = QLabel(section_type)
        type_label.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 11px;
                border: none;
            }
            """
        )

        text_layout.addWidget(
            title_label
        )

        text_layout.addWidget(
            type_label
        )

        layout.addLayout(
            text_layout
        )

        layout.addStretch()

        status_label = QLabel(status)
        status_label.setStyleSheet(
            """
            QLabel {
                color: #3E63DD;
                font-size: 11px;
                font-weight: 600;
                border: none;
            }
            """
        )

        layout.addWidget(
            status_label
        )

        self.sections_layout.addWidget(
            card
        )

    def _clear_sections(self):

        while self.sections_layout.count():

            item = self.sections_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()