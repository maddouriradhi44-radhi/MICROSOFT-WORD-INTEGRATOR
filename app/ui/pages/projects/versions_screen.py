from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
)


class VersionsScreen(QWidget):

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

        layout = QVBoxLayout()

        layout.setContentsMargins(
            30, 30, 30, 30
        )

        layout.setSpacing(20)

        header = QHBoxLayout()

        titles = QVBoxLayout()

        title = QLabel("Versions")

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
            "Review document and section versions"
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

        back = QPushButton("Back")

        back.clicked.connect(
            self.back_requested.emit
        )

        header.addWidget(back)

        layout.addLayout(header)

        self._add_version(
            layout,
            "Version 3",
            "Current version",
        )

        self._add_version(
            layout,
            "Version 2",
            "Archived",
        )

        self._add_version(
            layout,
            "Version 1",
            "Archived",
        )

        layout.addStretch()

        self.setLayout(layout)

    def _add_version(
        self,
        parent_layout,
        version,
        status,
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

        title = QLabel(version)

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

        row.addWidget(title)
        row.addStretch()

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

        row.addWidget(status_label)

        parent_layout.addWidget(card)