from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QScrollArea,
)


class ActivityScreen(QWidget):

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
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        title = QLabel("Activity")
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
            "Recent activity and actions in your project"
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
        back_button.setCursor(Qt.PointingHandCursor)
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

        back_button.clicked.connect(self.back_requested.emit)

        header_layout.addWidget(back_button)

        refresh_button = QPushButton("Refresh")
        refresh_button.setCursor(Qt.PointingHandCursor)
        refresh_button.setFixedHeight(36)

        refresh_button.setStyleSheet(
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

        refresh_button.clicked.connect(self._load_activity)

        header_layout.addWidget(refresh_button)

        main_layout.addLayout(header_layout)

        # Activity container
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

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.activity_content = QWidget()

        self.activity_layout = QVBoxLayout()
        self.activity_layout.setContentsMargins(0, 0, 0, 0)
        self.activity_layout.setSpacing(0)

        self.activity_content.setLayout(self.activity_layout)

        scroll.setWidget(self.activity_content)

        container_layout.addWidget(scroll)

        container.setLayout(container_layout)

        main_layout.addWidget(container, 1)

        self.setLayout(main_layout)

        self._load_activity()

    def _load_activity(self):
        self._clear_activity()

        activities = [
            (
                "Document",
                "Document workspace opened",
                "Recently",
            ),
            (
                "Section",
                "Section workspace accessed",
                "Recently",
            ),
            (
                "Notification",
                "Notifications checked",
                "Recently",
            ),
        ]

        for activity_type, description, timestamp in activities:
            self._add_activity(
                activity_type,
                description,
                timestamp,
            )

    def _clear_activity(self):
        while self.activity_layout.count():
            item = self.activity_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _add_activity(
        self,
        activity_type,
        description,
        timestamp,
    ):
        row = QFrame()
        row.setStyleSheet(
            """
            QFrame {
                background-color: transparent;
                border: none;
                border-bottom: 1px solid #F0F1F3;
            }
            """
        )

        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(4, 16, 4, 16)
        row_layout.setSpacing(14)

        icon = QLabel(self._get_icon(activity_type))
        icon.setFixedSize(38, 38)
        icon.setAlignment(Qt.AlignCenter)

        icon.setStyleSheet(
            """
            QLabel {
                background-color: #EEF2FF;
                color: #3E63DD;
                border-radius: 19px;
                font-size: 15px;
                font-weight: 700;
                border: none;
            }
            """
        )

        row_layout.addWidget(icon)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)

        description_label = QLabel(description)
        description_label.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 13px;
                font-weight: 600;
                border: none;
            }
            """
        )

        type_label = QLabel(activity_type)
        type_label.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 11px;
                border: none;
            }
            """
        )

        text_layout.addWidget(description_label)
        text_layout.addWidget(type_label)

        row_layout.addLayout(text_layout)
        row_layout.addStretch()

        time_label = QLabel(timestamp)
        time_label.setStyleSheet(
            """
            QLabel {
                color: #9CA3AF;
                font-size: 11px;
                border: none;
            }
            """
        )

        row_layout.addWidget(time_label)

        row.setLayout(row_layout)

        self.activity_layout.addWidget(row)

    def _get_icon(self, activity_type):
        icons = {
            "Document": "📄",
            "Section": "▤",
            "Notification": "🔔",
            "Version": "↻",
            "Export": "⇩",
            "Import": "⇧",
            "Validation": "✓",
        }

        return icons.get(activity_type, "•")