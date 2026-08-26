from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QScrollArea,
)
from pages.projects.dashboard_screen import DashboardScreen
from models.project import Project
from services.project_service import project_service


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
            color: #1A1A1A;
            font-size: 17px;
            font-weight: 700;
            border: none;
            """
        )

        role_label = QLabel(project.role)
        role_label.setStyleSheet(
            f"""
            color: {accent};
            font-size: 12px;
            font-weight: 700;
            border: none;
            """
        )

        info_layout.addWidget(name_label)
        info_layout.addWidget(role_label)

        if project.description:
            description_label = QLabel(project.description)
            description_label.setWordWrap(True)
            description_label.setStyleSheet(
                """
                color: #6B7280;
                font-size: 11px;
                border: none;
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
                opacity: 0.9;
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

class ProjectsWorker(QThread):

    success = Signal(object)
    failure = Signal(object)

    def run(self):
        try:
            data = project_service.get_projects()
        except Exception as error:
            self.failure.emit(error)
        else:
            self.success.emit(data)



class MyProjectsScreen(QWidget):

    open_project = Signal(object)

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.worker = None

        self.setStyleSheet(
            """
            QWidget {
                background-color: #F5F7FA;
            }
            """
        )


        self._build_ui()
        self.load_projects()

    def _build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(20)

        company_label = QLabel("CAPGEMINI")
        company_label.setAlignment(Qt.AlignCenter)
        company_label.setStyleSheet(
            """
            color: #001D5C;
            font-size: 18px;
            font-weight: 800;
            letter-spacing: 2px;
            """
        )

        first_name = self.user.get("first_name", "")
        last_name = self.user.get("last_name", "")

        full_name = f"{first_name} {last_name}".strip()

        greeting_label = QLabel(
            f"Good Morning , {full_name}"
        )
        greeting_label.setAlignment(Qt.AlignCenter)
        greeting_label.setStyleSheet(
            """
            color: #1A1A1A;
            font-size: 22px;
            font-weight: 700;
            """
        )

        subtitle_label = QLabel(
            " Welcome to your workspace "
        )
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(
            """
            color: #6B7280;
            font-size: 13px;
            """
        )

        title_label = QLabel("MY PROJECTS")
        title_label.setStyleSheet(
            """
            color: #1A1A1A;
            font-size: 18px;
            font-weight: 700;
            """
        )

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(
            """
            color: #6B7280;
            font-size: 13px;
            """
        )

        self.retry_button = QPushButton("RETRY")
        self.retry_button.setFixedSize(110, 40)
        self.retry_button.setCursor(Qt.PointingHandCursor)
        self.retry_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0070AD;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #005E92;
            }
            """
        )
        self.retry_button.clicked.connect(self.load_projects)
        self.retry_button.setVisible(False)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }
            """
        )

        self.projects_container = QWidget()

        self.projects_layout = QVBoxLayout()
        self.projects_layout.setContentsMargins(0, 0, 0, 0)
        self.projects_layout.setSpacing(16)

        self.projects_container.setLayout(
            self.projects_layout
        )

        self.scroll_area.setWidget(
            self.projects_container
        )

        main_layout.addWidget(company_label)
        main_layout.addWidget(greeting_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addSpacing(15)
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(
            self.retry_button,
            alignment=Qt.AlignCenter,
        )
        main_layout.addWidget(self.scroll_area, 1)

        self.setLayout(main_layout)

    def clear_projects(self):
        while self.projects_layout.count():
            item = self.projects_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def load_projects(self):

        if self.worker is not None and self.worker.isRunning():
            return

        self.clear_projects()

        self.retry_button.setVisible(False)

        self.status_label.setText(
            "Loading projects..."
        )

        self.worker = ProjectsWorker()

        self.worker.success.connect(
            self._handle_projects_success
        )

        self.worker.failure.connect(
            self._handle_projects_failure
        )

        self.worker.finished.connect(
            self._cleanup_worker
        )

        self.worker.start()

    def _handle_projects_success(self, data):

        try:
            projects = [
                Project.from_dict(project_data)
                for project_data in data
            ]

        except Exception:
            self.status_label.setText(
                "Unable to load your projects."
            )
            self.retry_button.setVisible(True)
            return

        if not projects:
            self.status_label.setText(
                "No projects available.\n"
                "You are not currently assigned to any project."
            )
            return

        self.status_label.clear()

        for project in projects:

            card = ProjectCard(project)

            card.open_project.connect(
                self.open_project.emit
            )

            self.projects_layout.addWidget(
                card
            )

        self.projects_layout.addStretch()

    def _handle_projects_failure(self, error):

        self.status_label.setText(
            "Unable to load your projects."
        )

        self.retry_button.setVisible(True)

    def _cleanup_worker(self):

        if self.worker is not None:

            self.worker.deleteLater()

            self.worker = None