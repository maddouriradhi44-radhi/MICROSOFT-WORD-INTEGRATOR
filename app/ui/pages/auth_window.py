from PySide6.QtWidgets import QMainWindow, QStackedWidget

from pages.projects.my_projects_screen import MyProjectsScreen
from components.auth_widgets import BG_WINDOW

from pages.login_screen import LoginScreen
from pages.signup_screen import SignUpScreen
from pages.email_verification_screen import EmailVerificationScreen
from pages.forget_password_screen import ForgotPasswordScreen
from pages.reset_password_screen import ResetPasswordScreen

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
from pages.projects.document_screen import DocumentScreen

class AuthWindow(QMainWindow):

    def __init__(self, on_authenticated=None):
        super().__init__()

        self.on_authenticated = on_authenticated

        self.my_projects_screen = None
        self.dashboard_screen = None
        self.collaborator_dashboard = None
        self.document_screen = None
        self.notifications_screen = None
        self.current_user = None

        self.my_sections_screen = None
        self.section_workspace_screen = None

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

        if project.role == "COLLABORATOR":

            self.collaborator_dashboard = (
                CollaboratorDashboardScreen(
                    project=project,
                    user=self.current_user,
                )
            )

            self.collaborator_dashboard.nav_requested.connect(
                self._handle_collaborator_navigation
            )

            self.stack.addWidget(
                self.collaborator_dashboard
            )

            self.stack.setCurrentWidget(
                self.collaborator_dashboard
            )

        elif project.role == "PROJECT_MANAGER":

            print(
                "Manager Dashboard will be implemented later."
            )

        elif project.role == "READER":

            print(
                "Reader Dashboard will be implemented later."
            )

        else:

            print(
                f"Unknown project role: {project.role}"
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

            # --------------------------------------------------
            # IMPORTANT:
            # Make My Sections the current screen
            # --------------------------------------------------

            self.stack.setCurrentWidget(
                self.my_sections_screen
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

            else:

                self.document_screen.load_document()

            self.stack.setCurrentWidget(
                self.document_screen
            )
            print("\n========== STACK DEBUG ==========")

            print(
                "CURRENT WIDGET:",
                self.stack.currentWidget()
            )

            print(
                "MY SECTIONS VISIBLE:",
                self.my_sections_screen.isVisible()
            )

            print(
                "MY SECTIONS HIDDEN:",
                self.my_sections_screen.isHidden()
            )

            print(
                "MY SECTIONS SIZE:",
                self.my_sections_screen.size()
            )

            print(
                "STACK VISIBLE:",
                self.stack.isVisible()
            )

            print(
                "STACK SIZE:",
                self.stack.size()
            )

            print(
                "MY SECTIONS PARENT:",
                self.my_sections_screen.parent()
            )

            print(
                "MY SECTIONS PARENT VISIBLE:",
                self.my_sections_screen.parent().isVisible()
                if self.my_sections_screen.parent()
                else None
            )

            print("=================================\n")
        # ------------------------------------------------------
        # Dashboard
        # ------------------------------------------------------

        elif key == "dashboard":

            if self.collaborator_dashboard is not None:

                self.collaborator_dashboard.header.refresh_unread_count()

                self.stack.setCurrentWidget(
                    self.collaborator_dashboard
                )

    # ==========================================================
    # OPEN SECTION WORKSPACE
    # ==========================================================

    def _handle_section_open(self, section_id):
        """
        Open the workspace of the selected section.
        """

        print()
        print("==========================================")
        print("        SECTION WORKSPACE DEBUG")
        print("==========================================")
        print(
            "Section ID requested:",
            section_id
        )

        section = None

        # ------------------------------------------------------
        # Find selected section
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # Selected section information
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # Back to My Sections
        # ------------------------------------------------------

        self.section_workspace_screen.back_requested.connect(
            self._return_to_my_sections
        )

        # ------------------------------------------------------
        # Add workspace to stack
        # ------------------------------------------------------

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
        """
        Return from Section Workspace to My Sections.
        """

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