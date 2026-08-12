from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from app.ui.models.project import Project


class ProjectCard(QFrame):

    open_project = Signal(object)

    def __init__(self, project: Project):
        super().__init__()

        self.project = project

        role_colors = {
            "PROJECT_MANAGER": "#C0392B",
            "COLLABORATOR": "#0070AD",
            "READER": "#6B7280",
        }

        accent = role_colors.get(project.role, "#6B7280")

        self.setMinimumHeight(110)

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: #FFFFFF;
                border: 1.5px solid #D9E2EC;
                border-left: 5px solid {accent};
                border-radius: 12px;
            }}
            """
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(24, 18, 20, 18)
        layout.setSpacing(20)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)

        name_label = QLabel(project.name)
        name_label.setStyleSheet(
            """
            QLabel {
                color: #1A1A1A;
                font-size: 17px;
                font-weight: 700;
                border: none;
            }
            """
        )

        role_label = QLabel(project.role)
        role_label.setStyleSheet(
            f"""
            QLabel {{
                color: {accent};
                font-size: 12px;
                font-weight: 700;
                border: none;
            }}
            """
        )

        info_layout.addWidget(name_label)
        info_layout.addWidget(role_label)

        if project.description:
            description_label = QLabel(project.description)
            description_label.setWordWrap(True)
            description_label.setStyleSheet(
                """
                QLabel {
                    color: #6B7280;
                    font-size: 11px;
                    border: none;
                }
                """
            )
            info_layout.addWidget(description_label)

        layout.addLayout(info_layout, 1)

        open_button = QPushButton("OPEN")
        open_button.setFixedSize(110, 42)
        open_button.setCursor(Qt.PointingHandCursor)

        open_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {accent};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 700;
            }}

            QPushButton:hover {{
                background-color: {accent};
            }}
            """
        )

        open_button.clicked.connect(
            lambda: self.open_project.emit(self.project)
        )

        layout.addWidget(
            open_button,
            alignment=Qt.AlignVCenter,
        )

        self.setLayout(layout)