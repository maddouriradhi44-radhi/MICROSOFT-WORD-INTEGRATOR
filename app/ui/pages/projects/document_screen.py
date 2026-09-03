from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
)


class DocumentScreen(QWidget):

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
        main_layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )
        main_layout.setSpacing(20)

        # ======================================================
        # HEADER
        # ======================================================

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        title = QLabel("Document")

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
            "View and manage the project document"
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

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        back_button = QPushButton("Back")

        back_button.setCursor(
            Qt.PointingHandCursor
        )

        back_button.setFixedHeight(36)

        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                color: #374151;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 0 16px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #F3F4F6;
            }
            """
        )

        back_button.clicked.connect(
            self.back_requested.emit
        )

        header_layout.addWidget(
            back_button
        )

        main_layout.addLayout(
            header_layout
        )

        # ======================================================
        # DOCUMENT CARD
        # ======================================================

        document_card = QFrame()

        document_card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            """
        )

        document_layout = QVBoxLayout()

        document_layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        document_layout.setSpacing(12)

        document_title = QLabel(
            self.project.name
            if self.project is not None
            else "Project Document"
        )

        document_title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 18px;
                font-weight: 700;
                border: none;
            }
            """
        )

        document_layout.addWidget(
            document_title
        )

        status = QLabel(
            "Document workspace"
        )

        status.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 13px;
                border: none;
            }
            """
        )

        document_layout.addWidget(
            status
        )

        info = QLabel(
            "The project document will be available here."
        )

        info.setWordWrap(True)

        info.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 12px;
                border: none;
            }
            """
        )

        document_layout.addWidget(
            info
        )

        document_layout.addStretch()

        document_card.setLayout(
            document_layout
        )

        main_layout.addWidget(
            document_card,
            1,
        )

        self.setLayout(
            main_layout
        )