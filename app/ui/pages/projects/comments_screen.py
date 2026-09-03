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


class CommentsScreen(QWidget):

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
            30, 30, 30, 30
        )
        main_layout.setSpacing(20)

        # ------------------------------------------------------
        # Header
        # ------------------------------------------------------

        header = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        title = QLabel("Comments")

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
            "Review comments and discussions "
            "related to the project"
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
        back_button.setCursor(
            Qt.PointingHandCursor
        )

        back_button.clicked.connect(
            self.back_requested.emit
        )

        header.addWidget(back_button)

        main_layout.addLayout(header)

        # ------------------------------------------------------
        # Comments container
        # ------------------------------------------------------

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

        container_layout = QVBoxLayout(
            container
        )

        container_layout.setContentsMargins(
            20, 20, 20, 20
        )

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()

        self.comments_layout = QVBoxLayout(
            content
        )

        self.comments_layout.setSpacing(10)

        scroll.setWidget(content)

        container_layout.addWidget(scroll)

        main_layout.addWidget(
            container,
            1
        )

        self.setLayout(main_layout)

        self._load_comments()

    # ==========================================================
    # LOAD COMMENTS
    # ==========================================================

    def _load_comments(self):

        self._clear_comments()

        # Temporary frontend data.
        # Backend integration will be connected later.

        self._add_comment(
            "Collaborator",
            "Please review the latest changes "
            "in this section.",
            "Project Requirements",
        )

        self._add_comment(
            "Project Manager",
            "The proposed modification looks good.",
            "Technical Architecture",
        )

        self._add_comment(
            "Collaborator",
            "I need clarification about this requirement.",
            "Introduction",
        )

    # ==========================================================
    # ADD COMMENT
    # ==========================================================

    def _add_comment(
        self,
        author,
        content,
        section,
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

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            16, 14, 16, 14
        )

        layout.setSpacing(6)

        # ------------------------------------------------------
        # Comment header
        # ------------------------------------------------------

        header = QHBoxLayout()

        author_label = QLabel(author)

        author_label.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 13px;
                font-weight: 700;
                border: none;
            }
            """
        )

        header.addWidget(
            author_label
        )

        header.addStretch()

        section_label = QLabel(section)

        section_label.setStyleSheet(
            """
            QLabel {
                color: #3E63DD;
                font-size: 11px;
                font-weight: 600;
                border: none;
            }
            """
        )

        header.addWidget(
            section_label
        )

        layout.addLayout(header)

        # ------------------------------------------------------
        # Comment content
        # ------------------------------------------------------

        comment_label = QLabel(content)

        comment_label.setWordWrap(True)

        comment_label.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 12px;
                border: none;
            }
            """
        )

        layout.addWidget(
            comment_label
        )

        # ------------------------------------------------------
        # Actions
        # ------------------------------------------------------

        actions = QHBoxLayout()
        actions.addStretch()

        reply_button = QPushButton("Reply")
        reply_button.setFixedHeight(30)

        resolve_button = QPushButton("Resolve")
        resolve_button.setFixedHeight(30)

        actions.addWidget(
            reply_button
        )

        actions.addWidget(
            resolve_button
        )

        layout.addLayout(actions)

        self.comments_layout.addWidget(
            card
        )

    # ==========================================================
    # CLEAR COMMENTS
    # ==========================================================

    def _clear_comments(self):

        while self.comments_layout.count():

            item = self.comments_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()