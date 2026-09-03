from PySide6.QtWidgets import QMainWindow, QStackedWidget

from pages.projects.my_projects_screen import MyProjectsScreen
from components.auth_widgets import BG_WINDOW

from pages.login_screen import LoginScreen
from pages.signup_screen import SignUpScreen
from pages.email_verification_screen import EmailVerificationScreen
from pages.forget_password_screen import ForgotPasswordScreen
from pages.reset_password_screen import ResetPasswordScreen
from pages.projects.document_screen import DocumentScreen

from pages.projects.dashboard_screen import DashboardScreen
from pages.projects.collaborator_dashboard_screen import (
    CollaboratorDashboardScreen
)
from pages.projects.notifications_screen import (
    NotificationsScreen
)
from pages.projects.my_sections_screen import (
    MySectionsScreen
)
from pages.projects.section_workspace_screen import (
    SectionWorkspaceScreen
)

from pages.projects.activity import ActivityScreen
from pages.projects.settings import SettingsScreen
from pages.projects.ai_sections_screen import AISectionsScreen
from services.section_service import section_service

from pages.projects.sections_screen import SectionsScreen
from pages.projects.members_screen import MembersScreen
from pages.projects.assignments_screen import AssignmentsScreen
from pages.projects.validation_screen import ValidationScreen
from pages.projects.comments_screen import CommentsScreen
from pages.projects.versions_screen import VersionsScreen


class AuthWindow(QMainWindow):

    def __init__(self, on_authenticated=None):
        super().__init__()

        self.on_authenticated = on_authenticated

        self.my_projects_screen = None
        self.dashboard_screen = None
        self.collaborator_dashboard = None
        self.notifications_screen = None
        self.activity_screen = None
        self.settings_screen = None
        self.document_screen = None
        self.current_user = None
        self.ai_sections_screen = None

        self.my_sections_screen = None
        self.section_workspace_screen = None

        self.sections_screen = None
        self.members_screen = None
        self.assignments_screen = None
        self.validation_screen = None
        self.comments_screen = None
        self.versions_screen = None

        self.setWindowTitle("Microsoft Word Integrator")
        self.resize(480, 640)
        self.setMinimumSize(400, 500)
        

        self.setStyleSheet(
            f"QMainWindow {{ background-color: {BG_WINDOW}; }}"
        )

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_screen = LoginScreen(
            on_success=self._handle_authenticated,
            on_navigate=self.navigate_to,
        )

        self.stack.addWidget(
            self.login_screen
        )

        self.signup_screen = None
        self.email_verification_screen = None
        self.forgot_password_screen = None
        self.reset_password_screen = None

        self.stack.setCurrentWidget(
            self.login_screen
        )

    # ==========================================================
    # AUTHENTICATION
    # ==========================================================

    def _handle_authenticated(self, auth_result):

        user = auth_result.user
        self.current_user = user

        self.my_projects_screen = MyProjectsScreen(
            user=user
        )

        self.my_projects_screen.open_project.connect(
            self._handle_project_open
        )

        self.stack.addWidget(
            self.my_projects_screen
        )

        self.stack.setCurrentWidget(
            self.my_projects_screen
        )

    # ==========================================================
    # PROJECT
    # ==========================================================

    def _handle_project_open(self, project):

        if project.role == "PROJECT_MANAGER":

            self.dashboard_screen = DashboardScreen(
                project=project
            )

            self.dashboard_screen.nav_requested.connect(
                self._handle_manager_navigation
            )

            self.dashboard_screen.logout_requested.connect(
                self._handle_logout
            )

            self.dashboard_screen.settings_requested.connect(
                lambda: self._handle_manager_navigation("settings")
            )

            self.stack.addWidget(
                self.dashboard_screen
            )

            self.stack.setCurrentWidget(
                self.dashboard_screen
            )

        elif project.role == "COLLABORATOR":

            self.collaborator_dashboard = (
                CollaboratorDashboardScreen(
                    project=project,
                    user=self.current_user,
                )
            )

            self.collaborator_dashboard.nav_requested.connect(
                self._handle_collaborator_navigation
            )

            self.collaborator_dashboard.settings_requested.connect(
                lambda: self._handle_collaborator_navigation("settings")
            )

            self.collaborator_dashboard.logout_requested.connect(
                self._handle_logout
            )

            self.stack.addWidget(
                self.collaborator_dashboard
            )

            self.stack.setCurrentWidget(
                self.collaborator_dashboard
            )

        elif project.role == "READER":

            print("Reader Dashboard will be implemented later.")

        else:

            print(
                f"Unknown project role: {project.role}"
            )


# ==========================================================
# PROJECT MANAGER NAVIGATION
# ==========================================================

    def _handle_manager_navigation(self, key):

        if key == "overview":

            self.dashboard_screen.set_active_nav(
                "overview"
            )

            self.stack.setCurrentWidget(
                self.dashboard_screen
            )

        elif key == "sections":

            if self.sections_screen is None:

                self.sections_screen = SectionsScreen(
                    project=self.dashboard_screen.project,
                    user=self.current_user,
                )

                self.sections_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.stack.addWidget(
                    self.sections_screen
                )

            self.stack.setCurrentWidget(
                self.sections_screen
            )

        elif key == "documents":

            if self.document_screen is None:

                self.document_screen = DocumentScreen(
                    project=self.dashboard_screen.project,
                    user=self.current_user,
                )

                self.document_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.stack.addWidget(
                    self.document_screen
                )

            self.stack.setCurrentWidget(
                self.document_screen
            )

        elif key == "members":

            if self.members_screen is None:

                self.members_screen = MembersScreen(
                    project=self.dashboard_screen.project,
                    user=self.current_user,
                )

                self.members_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.stack.addWidget(
                    self.members_screen
                )

            self.stack.setCurrentWidget(
                self.members_screen
            )

        elif key == "assignments":

            if self.assignments_screen is None:

                self.assignments_screen = AssignmentsScreen(
                    project=self.dashboard_screen.project,
                    user=self.current_user,
                )

                self.assignments_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.stack.addWidget(
                    self.assignments_screen
                )

            self.stack.setCurrentWidget(
                self.assignments_screen
            )

        elif key == "validation":

            if self.validation_screen is None:

                self.validation_screen = ValidationScreen(
                    project=self.dashboard_screen.project,
                    user=self.current_user,
                )

                self.validation_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.stack.addWidget(
                    self.validation_screen
                )

            self.stack.setCurrentWidget(
                self.validation_screen
            )

        elif key == "comments":

            if self.comments_screen is None:

                self.comments_screen = CommentsScreen(
                    project=self.dashboard_screen.project,
                    user=self.current_user,
                )

                self.comments_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.stack.addWidget(
                    self.comments_screen
                )

            self.stack.setCurrentWidget(
                self.comments_screen
            )

        elif key == "versions":

            if self.versions_screen is None:

                self.versions_screen = VersionsScreen(
                    project=self.dashboard_screen.project,
                    user=self.current_user,
                )

                self.versions_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.stack.addWidget(
                    self.versions_screen
                )

            self.stack.setCurrentWidget(
                self.versions_screen
            )

        elif key == "activity":

            if self.activity_screen is None:

                self.activity_screen = ActivityScreen(
                    project=self.dashboard_screen.project,
                    user=self.current_user,
                )

                self.activity_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.stack.addWidget(
                    self.activity_screen
                )

            self.stack.setCurrentWidget(
                self.activity_screen
            )

        elif key == "notifications":

            if self.notifications_screen is None:

                self.notifications_screen = NotificationsScreen()

                self.notifications_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.stack.addWidget(
                    self.notifications_screen
                )

            self.notifications_screen.load_notifications()

            self.stack.setCurrentWidget(
                self.notifications_screen
            )

        elif key == "settings":

            if self.settings_screen is None:

                self.settings_screen = SettingsScreen(
                    user=self.current_user,
                )

                self.settings_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.stack.addWidget(
                    self.settings_screen
                )

            self.stack.setCurrentWidget(
                self.settings_screen
            )

        elif key == "ai_insights":

            if self.ai_sections_screen is None:

                self.ai_sections_screen = AISectionsScreen(
                    project=self.dashboard_screen.project,
                    user=self.current_user,
                )

                self.ai_sections_screen.back_requested.connect(
                    self._return_to_manager_dashboard
                )

                self.ai_sections_screen.refresh_requested.connect(
                    self._load_ai_proposals
                )

                self.ai_sections_screen.accept_requested.connect(
                    self._accept_ai_proposal
                )

                self.ai_sections_screen.reject_requested.connect(
                    self._reject_ai_proposal
                )

                self.ai_sections_screen.modify_requested.connect(
                    self._modify_ai_proposal
                )

                self.stack.addWidget(
                    self.ai_sections_screen
                )

            self._load_ai_proposals()

            self.stack.setCurrentWidget(
                self.ai_sections_screen
            )

        elif key == "logout":

            self._handle_logout()

    # ==========================================================
    # RETURN TO MANAGER DASHBOARD
    # ==========================================================

    def _return_to_manager_dashboard(self):

        if self.dashboard_screen is not None:

            self.stack.setCurrentWidget(
                self.dashboard_screen
            )

            self.dashboard_screen.set_active_nav(
                "overview"
            )

    # ==========================================================
    # COLLABORATOR NAVIGATION
    # ==========================================================

    def _handle_collaborator_navigation(self, key):

        # ------------------------------------------------------
        # Notifications
        # ------------------------------------------------------

        if key == "notifications":

            if self.notifications_screen is None:

                self.notifications_screen = (
                    NotificationsScreen()
                )

                self.notifications_screen.back_requested.connect(
                    self._return_to_collaborator_dashboard
                )

                self.stack.addWidget(
                    self.notifications_screen
                )

            self.notifications_screen.load_notifications()

            self.stack.setCurrentWidget(
                self.notifications_screen
            )

        # ------------------------------------------------------
        # My Sections
        # ------------------------------------------------------

        elif key == "sections":

            if self.my_sections_screen is None:

                self.my_sections_screen = MySectionsScreen(
                    project=self.collaborator_dashboard.project,
                    user=self.current_user,
                )

                self.my_sections_screen.back_requested.connect(
                    self._return_to_collaborator_dashboard
                )

                self.my_sections_screen.section_open_requested.connect(
                    self._handle_section_open
                )

                self.stack.addWidget(
                    self.my_sections_screen
                )

            else:

                self.my_sections_screen.project = (
                    self.collaborator_dashboard.project
                )

                self.my_sections_screen.user = (
                    self.current_user
                )

                self.my_sections_screen.load_sections()

            self.stack.setCurrentWidget(
                self.my_sections_screen
            )

        # ------------------------------------------------------
        # Dashboard
        # ------------------------------------------------------

        elif key == "dashboard":

            if self.collaborator_dashboard is not None:

                self.collaborator_dashboard.header.refresh_unread_count()

                self.stack.setCurrentWidget(
                    self.collaborator_dashboard
                )
                # ------------------------------------------------------
        # Document
        # ------------------------------------------------------

        elif key == "document":

            if self.document_screen is None:

                self.document_screen = DocumentScreen(
                    project=self.collaborator_dashboard.project,
                    user=self.current_user,
                )

                self.document_screen.back_requested.connect(
                    self._return_to_collaborator_dashboard
                )

                self.stack.addWidget(
                    self.document_screen
                )

            self.stack.setCurrentWidget(
                self.document_screen
            )

        # ------------------------------------------------------
        # Activity
        # ------------------------------------------------------

        elif key == "activity":

            if self.activity_screen is None:

                self.activity_screen = ActivityScreen(
                    project=self.collaborator_dashboard.project,
                    user=self.current_user,
                )

                self.activity_screen.back_requested.connect(
                    self._return_to_collaborator_dashboard
                )

                self.stack.addWidget(
                    self.activity_screen
                )

            self.stack.setCurrentWidget(
                self.activity_screen
            )

        # ------------------------------------------------------
        # Settings
        # ------------------------------------------------------

        elif key == "settings":

            if self.settings_screen is None:

                self.settings_screen = SettingsScreen(
                    user=self.current_user,
                )

                self.settings_screen.back_requested.connect(
                    self._return_to_collaborator_dashboard
                )

                self.stack.addWidget(
                    self.settings_screen
                )

            self.stack.setCurrentWidget(
                self.settings_screen
            )
        

    # ==========================================================
    # OPEN SECTION WORKSPACE
    # ==========================================================

    def _handle_section_open(self, section_id):

        print()
        print("==========================================")
        print("        SECTION WORKSPACE DEBUG")
        print("==========================================")
        print(
            "Section ID requested:",
            section_id
        )

        section = None

        if self.my_sections_screen is None:

            print(
                "ERROR: MySectionsScreen is None."
            )

            print("==========================================")
            print()

            return

        print(
            "Number of sections:",
            len(self.my_sections_screen.sections)
        )

        for item in self.my_sections_screen.sections:

            print(
                "Section:",
                "id =", item.id,
                "| title =", item.title,
                "| document_id =", item.document_id,
                "| module =", item.module,
                "| status =", item.status,
                "| content_exists =", bool(item.content),
            )

            if item.id == section_id:
                section = item

        print("------------------------------------------")

        if section is None:

            print(
                f"ERROR: Section {section_id} not found."
            )

            print("==========================================")
            print()

            return

        print("SELECTED SECTION")
        print(
            "id:",
            section.id
        )
        print(
            "title:",
            section.title
        )
        print(
            "document_id:",
            section.document_id
        )
        print(
            "module:",
            section.module
        )
        print(
            "status:",
            section.status
        )
        print(
            "content:",
            section.content[:100]
            if section.content
            else "(empty)"
        )

        print("==========================================")
        print()

        # ------------------------------------------------------
        # Remove old workspace
        # ------------------------------------------------------

        if self.section_workspace_screen is not None:

            self.stack.removeWidget(
                self.section_workspace_screen
            )

            self.section_workspace_screen.deleteLater()

            self.section_workspace_screen = None

        # ------------------------------------------------------
        # Create workspace
        # ------------------------------------------------------

        self.section_workspace_screen = (
            SectionWorkspaceScreen(
                section=section,
                user=self.current_user,
            )
        )

        self.section_workspace_screen.back_requested.connect(
            self._return_to_my_sections
        )

        self.stack.addWidget(
            self.section_workspace_screen
        )

        self.stack.setCurrentWidget(
            self.section_workspace_screen
        )

    # ==========================================================
    # RETURN TO MY SECTIONS
    # ==========================================================

    def _return_to_my_sections(self):

        if self.my_sections_screen is not None:

            self.my_sections_screen.load_sections()

            self.stack.setCurrentWidget(
                self.my_sections_screen
            )

    # ==========================================================
    # RETURN TO COLLABORATOR DASHBOARD
    # ==========================================================

    def _return_to_collaborator_dashboard(self):

        if self.collaborator_dashboard is not None:

            self.collaborator_dashboard.header.refresh_unread_count()

            self.stack.setCurrentWidget(
                self.collaborator_dashboard
            )

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    def navigate_to(self, screen_name, **kwargs):

        # ------------------------------------------------------
        # Login
        # ------------------------------------------------------

        if screen_name == "login":

            self.stack.setCurrentWidget(
                self.login_screen
            )

        # ------------------------------------------------------
        # Signup
        # ------------------------------------------------------

        elif screen_name == "signup":

            if self.signup_screen is None:

                self.signup_screen = SignUpScreen(
                    on_success=self._go_to_email_verification,
                    on_navigate=self.navigate_to,
                )

                self.stack.addWidget(
                    self.signup_screen
                )

            self.stack.setCurrentWidget(
                self.signup_screen
            )

        # ------------------------------------------------------
        # Email verification
        # ------------------------------------------------------

        elif screen_name == "email_verification":

            email = kwargs.get(
                "email",
                ""
            )

            if self.email_verification_screen is not None:

                self.stack.removeWidget(
                    self.email_verification_screen
                )

                self.email_verification_screen.deleteLater()

            self.email_verification_screen = (
                EmailVerificationScreen(
                    email=email,
                    on_resend=self._handle_resend_verification,
                    on_navigate=self.navigate_to,
                )
            )

            self.stack.addWidget(
                self.email_verification_screen
            )

            self.stack.setCurrentWidget(
                self.email_verification_screen
            )

        # ------------------------------------------------------
        # Forgot password
        # ------------------------------------------------------

        elif screen_name == "forgot_password":

            if self.forgot_password_screen is not None:

                self.stack.removeWidget(
                    self.forgot_password_screen
                )

                self.forgot_password_screen.deleteLater()

            self.forgot_password_screen = (
                ForgotPasswordScreen(
                    on_navigate=self.navigate_to
                )
            )

            self.stack.addWidget(
                self.forgot_password_screen
            )

            self.stack.setCurrentWidget(
                self.forgot_password_screen
            )

        # ------------------------------------------------------
        # Reset password
        # ------------------------------------------------------

        elif screen_name == "reset_password":

            token = kwargs.get(
                "token",
                ""
            )

            if self.reset_password_screen is not None:

                self.stack.removeWidget(
                    self.reset_password_screen
                )

                self.reset_password_screen.deleteLater()

            self.reset_password_screen = (
                ResetPasswordScreen(
                    token=token,
                    on_navigate=self.navigate_to,
                )
            )

            self.stack.addWidget(
                self.reset_password_screen
            )

            self.stack.setCurrentWidget(
                self.reset_password_screen
            )

    # ==========================================================
    # EMAIL VERIFICATION
    # ==========================================================

    def _go_to_email_verification(self, email):

        self.navigate_to(
            "email_verification",
            email=email,
        )

    def _handle_resend_verification(self, email):

        pass

    
# ==========================================================
# LOGOUT
# ==========================================================

    def _handle_logout(self):

        self.current_user = None

        self.my_projects_screen = None
        self.dashboard_screen = None
        self.collaborator_dashboard = None

        self.notifications_screen = None
        self.activity_screen = None
        self.settings_screen = None

        self.document_screen = None
        self.ai_sections_screen = None

        self.my_sections_screen = None
        self.section_workspace_screen = None

        self.sections_screen = None
        self.members_screen = None
        self.assignments_screen = None
        self.validation_screen = None
        self.comments_screen = None
        self.versions_screen = None

        self.stack.setCurrentWidget(
            self.login_screen
        )

    def _load_ai_proposals(self):

        print("Loading AI proposals...")

        if self.ai_sections_screen is None:
            return

        project = self.dashboard_screen.project

        document_id = getattr(project, "document_id", None)

        if document_id is None:
            print("ERROR: document_id not found in project.")
            self.ai_sections_screen.load_proposals([])
            return

        try:
            proposals = section_service.get_ai_proposals(
                document_id
            )

            print(
                "AI proposals loaded:",
                len(proposals)
            )

            self.ai_sections_screen.load_proposals(
                proposals
            )

        except Exception as exc:

            print(
                "ERROR loading AI proposals:",
                exc
            )

            self.ai_sections_screen.load_proposals([])

    def _accept_ai_proposal(self, proposal_id):

        try:
            result = section_service.accept_ai_proposal(
                proposal_id
            )

            print("AI proposal accepted:", result)

            self._load_ai_proposals()

        except Exception as exc:
            print("ERROR accepting AI proposal:", exc)

   

    def _reject_ai_proposal(self, proposal_id):

        try:
            result = section_service.reject_ai_proposal(
                proposal_id
            )

            print("AI proposal rejected:", result)

            self._load_ai_proposals()

        except Exception as exc:
            print("ERROR rejecting AI proposal:", exc)


    def _modify_ai_proposal(self, proposal_id):
        print(
            "AI proposal modification:",
            proposal_id
        )