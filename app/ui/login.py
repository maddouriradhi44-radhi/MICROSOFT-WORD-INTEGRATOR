# Import PySide6 widgets required to create the graphical user interface.
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)

# Import Qt core functionalities such as widget alignment.
from PySide6.QtCore import Qt

# Import the authentication service responsible for user verification.
from services.auth_service import auth_service


# Window responsible for user authentication before accessing the application.
class LoginWindow(QWidget):

    def __init__(self, on_success=None):
        # Initialize the parent QWidget class.
        super().__init__()

        # Store the callback function that will be executed after successful login.
        self.on_success = on_success

        # Configure the login window properties.
        self.setWindowTitle("Connexion - Plateforme Documents")
        self.setFixedSize(320, 220)

        # Initialize and display all user interface components.
        self._build_ui()


    def _build_ui(self):
        # Create the main vertical layout used to organize widgets.
        layout = QVBoxLayout()

        # Set the spacing between interface elements.
        layout.setSpacing(12)


        # Create and configure the login title.
        title = QLabel("Connexion")

        # Center the title text horizontally.
        title.setAlignment(Qt.AlignCenter)

        # Apply visual styling to the title.
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Add the title widget to the layout.
        layout.addWidget(title)


        # Create the email input field.
        self.email_input = QLineEdit()

        # Display a hint text when the field is empty.
        self.email_input.setPlaceholderText("Email")

        # Add the email input field to the layout.
        layout.addWidget(self.email_input)


        # Create the password input field.
        self.password_input = QLineEdit()

        # Display a hint text for the password field.
        self.password_input.setPlaceholderText("Mot de passe")

        # Hide entered characters for security reasons.
        self.password_input.setEchoMode(QLineEdit.Password)

        # Add the password input field to the layout.
        layout.addWidget(self.password_input)


        # Create the authentication button.
        self.login_button = QPushButton("Connexion")

        # Connect the button click event to the login processing method.
        self.login_button.clicked.connect(self.handle_login)

        # Add the login button to the layout.
        layout.addWidget(self.login_button)


        # Allow users to press Enter in the password field
        # to trigger the authentication process.
        self.password_input.returnPressed.connect(self.handle_login)


        # Apply the created layout to the login window.
        self.setLayout(layout)


    def handle_login(self):
        # Retrieve the email entered by the user and remove extra spaces.
        email = self.email_input.text().strip()

        # Retrieve the password entered by the user.
        password = self.password_input.text()


        # Validate that required fields are not empty.
        if not email or not password:
            QMessageBox.warning(
                self,
                "Champs manquants",
                "Merci de remplir tous les champs."
            )
            return


        try:
            # Call the authentication service to verify user credentials.
            result = auth_service.login(email, password)


        except ValueError as e:
            # Handle authentication errors such as invalid credentials.
            QMessageBox.warning(
                self,
                "Échec de connexion",
                str(e)
            )
            return


        except Exception as e:
            # Handle unexpected application or system errors.
            QMessageBox.critical(
                self,
                "Erreur",
                f"Une erreur est survenue : {e}"
            )
            return


        # Display a confirmation message after successful authentication.
        QMessageBox.information(
            self,
            "Bienvenue",
            f"Connecté en tant que {result.user} ({result.role})"
        )


        # Execute the success callback if it was provided.
        # This allows the application to open the main window after login.
        if self.on_success:
            self.on_success(result)


        # Close the login window after successful authentication.
        self.close()
