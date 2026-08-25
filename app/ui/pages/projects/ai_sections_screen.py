from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QMessageBox,
)

from app.ui.services.ai_section_proposal_service import (
    ai_section_proposal_service,
)


# ============================================================================
# AI PROPOSAL CARD
# ============================================================================

class AIProposalCard(QFrame):

    modified = Signal(object)
    rejected = Signal(object)
    accepted = Signal(object)

    def __init__(self, proposal, parent=None):
        super().__init__(parent)

        self.proposal = proposal

        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        # ==============================================================
        # HEADER
        # ==============================================================

        header = QHBoxLayout()

        title = QLabel(
            f"{proposal.order}. {proposal.title}"
        )

        title.setWordWrap(True)

        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 16px;
                font-weight: 700;
                border: none;
                background-color: transparent;
            }
            """
        )

        header.addWidget(
            title,
            1,
        )

        confidence = QLabel(
            f"{proposal.confidence_percentage}% confidence"
        )

        confidence.setStyleSheet(
            """
            QLabel {
                color: #6941C6;
                background-color: #F4EBFF;
                border-radius: 8px;
                padding: 5px 9px;
                font-size: 11px;
                font-weight: 700;
                border: none;
            }
            """
        )

        header.addWidget(
            confidence
        )

        layout.addLayout(
            header
        )

        # ==============================================================
        # METADATA
        # ==============================================================

        metadata = QLabel(
            f"Level {proposal.level}  •  "
            f"Role: {proposal.suggested_role}  •  "
            f"Complexity: {proposal.complexity}"
        )

        metadata.setStyleSheet(
            """
            QLabel {
                color: #667085;
                font-size: 11px;
                border: none;
                background-color: transparent;
            }
            """
        )

        layout.addWidget(
            metadata
        )

        # ==============================================================
        # CONTENT
        # ==============================================================

        content_title = QLabel(
            "Proposed content"
        )

        content_title.setStyleSheet(
            """
            QLabel {
                color: #344054;
                font-size: 12px;
                font-weight: 600;
                border: none;
                background-color: transparent;
            }
            """
        )

        layout.addWidget(
            content_title
        )

        content = QLabel(
            proposal.content
        )

        content.setWordWrap(True)

        content.setStyleSheet(
            """
            QLabel {
                color: #475467;
                background-color: #F8FAFC;
                border: none;
                border-radius: 7px;
                padding: 9px;
                font-size: 12px;
            }
            """
        )

        layout.addWidget(
            content
        )

        # ==============================================================
        # REASON
        # ==============================================================

        reason_title = QLabel(
            "Why the AI proposed this section"
        )

        reason_title.setStyleSheet(
            """
            QLabel {
                color: #344054;
                font-size: 12px;
                font-weight: 600;
                border: none;
                background-color: transparent;
            }
            """
        )

        layout.addWidget(
            reason_title
        )

        reason = QLabel(
            proposal.reason
        )

        reason.setWordWrap(True)

        reason.setStyleSheet(
            """
            QLabel {
                color: #667085;
                font-size: 11px;
                border: none;
                background-color: transparent;
            }
            """
        )

        layout.addWidget(
            reason
        )

        # ==============================================================
        # KEYWORDS
        # ==============================================================

        if proposal.keywords:

            keywords = QLabel(
                "Keywords: "
                + ", ".join(proposal.keywords)
            )

            keywords.setWordWrap(True)

            keywords.setStyleSheet(
                """
                QLabel {
                    color: #8A94A6;
                    font-size: 11px;
                    border: none;
                    background-color: transparent;
                }
                """
            )

            layout.addWidget(
                keywords
            )

        # ==============================================================
        # ACTIONS
        # ==============================================================

        actions = QHBoxLayout()

        actions.addStretch()

        reject_button = QPushButton(
            "Reject"
        )

        reject_button.setCursor(
            Qt.PointingHandCursor
        )

        reject_button.setStyleSheet(
            """
            QPushButton {
                color: #B42318;
                background-color: #FEE4E2;
                border: none;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #FECACA;
            }
            """
        )

        reject_button.clicked.connect(
            lambda: self.rejected.emit(
                self.proposal
            )
        )

        actions.addWidget(
            reject_button
        )

        modify_button = QPushButton(
            "Modify"
        )

        modify_button.setCursor(
            Qt.PointingHandCursor
        )

        modify_button.setStyleSheet(
            """
            QPushButton {
                color: #344054;
                background-color: #EAECF0;
                border: none;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #D0D5DD;
            }
            """
        )

        modify_button.clicked.connect(
            lambda: self.modified.emit(
                self.proposal
            )
        )

        actions.addWidget(
            modify_button
        )

        accept_button = QPushButton(
            "Accept"
        )

        accept_button.setCursor(
            Qt.PointingHandCursor
        )

        accept_button.setStyleSheet(
            """
            QPushButton {
                color: white;
                background-color: #1E4FD6;
                border: none;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #173FB0;
            }
            """
        )

        accept_button.clicked.connect(
            lambda: self.accepted.emit(
                self.proposal
            )
        )

        actions.addWidget(
            accept_button
        )

        layout.addLayout(
            actions
        )


# ============================================================================
# AI SECTIONS SCREEN
# ============================================================================

class AISectionsScreen(QWidget):

    back_requested = Signal()
    validation_requested = Signal()

    def __init__(
        self,
        project=None,
        document_id=None,
        user=None,
        parent=None,
    ):
        super().__init__(parent)

        self.project = project
        self.document_id = document_id
        self.user = user

        self.proposals = []
        self.accepted_proposals = []

        self.setStyleSheet(
            """
            QWidget {
                background-color: #F7F8FA;
            }
            """
        )

        self._build_ui()
        self.load_proposals()

    # ==================================================================
    # BUILD UI
    # ==================================================================

    def _build_ui(self):

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        main_layout.setSpacing(
            18
        )

        # ==============================================================
        # HEADER
        # ==============================================================

        header = QHBoxLayout()

        back_button = QPushButton(
            "← Back"
        )

        back_button.setCursor(
            Qt.PointingHandCursor
        )

        back_button.setStyleSheet(
            """
            QPushButton {
                color: #344054;
                background-color: white;
                border: 1px solid #D0D5DD;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #F8FAFC;
            }
            """
        )

        back_button.clicked.connect(
            self.back_requested.emit
        )

        header.addWidget(
            back_button
        )

        header.addStretch()

        refresh_button = QPushButton(
            "Refresh"
        )

        refresh_button.setCursor(
            Qt.PointingHandCursor
        )

        refresh_button.setStyleSheet(
            """
            QPushButton {
                color: #344054;
                background-color: white;
                border: 1px solid #D0D5DD;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #F8FAFC;
            }
            """
        )

        refresh_button.clicked.connect(
            self.load_proposals
        )

        header.addWidget(
            refresh_button
        )

        main_layout.addLayout(
            header
        )

        # ==============================================================
        # TITLE
        # ==============================================================

        title = QLabel(
            "AI Section Analysis"
        )

        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 24px;
                font-weight: 700;
            }
            """
        )

        main_layout.addWidget(
            title
        )

        subtitle = QLabel(
            "Review the AI-generated section proposals "
            "before creating the final document sections."
        )

        subtitle.setWordWrap(True)

        subtitle.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 13px;
            }
            """
        )

        main_layout.addWidget(
            subtitle
        )

        # ==============================================================
        # SUMMARY
        # ==============================================================

        self.summary_label = QLabel(
            "Loading proposals..."
        )

        self.summary_label.setStyleSheet(
            """
            QLabel {
                color: #6941C6;
                background-color: #F4EBFF;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 12px;
                font-weight: 600;
            }
            """
        )

        main_layout.addWidget(
            self.summary_label
        )

        # ==============================================================
        # SCROLL AREA
        # ==============================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            """
        )

        container = QWidget()

        self.proposals_layout = QVBoxLayout(
            container
        )

        self.proposals_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.proposals_layout.setSpacing(
            14
        )

        self.proposals_layout.addStretch()

        scroll.setWidget(
            container
        )

        main_layout.addWidget(
            scroll,
            1
        )

        # ==============================================================
        # VALIDATE
        # ==============================================================

        footer = QHBoxLayout()

        footer.addStretch()

        self.validate_button = QPushButton(
            "Validate Proposals"
        )

        self.validate_button.setCursor(
            Qt.PointingHandCursor
        )

        self.validate_button.setStyleSheet(
            """
            QPushButton {
                color: white;
                background-color: #1E4FD6;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #173FB0;
            }

            QPushButton:disabled {
                background-color: #D0D5DD;
                color: #667085;
            }
            """
        )

        self.validate_button.clicked.connect(
            self._validate_proposals
        )

        footer.addWidget(
            self.validate_button
        )

        main_layout.addLayout(
            footer
        )

    # ==================================================================
    # LOAD
    # ==================================================================

    def load_proposals(self):

        self._clear_proposals()

        try:

            self.proposals = (
                ai_section_proposal_service.get_proposals(
                    document_id=self.document_id
                )
            )

        except Exception as exc:

            self.summary_label.setText(
                "Unable to load AI proposals."
            )

            error = QLabel(
                f"Error: {exc}"
            )

            error.setStyleSheet(
                "color: #B42318; font-size: 12px;"
            )

            self.proposals_layout.insertWidget(
                0,
                error
            )

            return

        self.accepted_proposals = []

        self.summary_label.setText(
            f"{len(self.proposals)} sections proposed by AI. "
            "Review them before validation."
        )

        for proposal in self.proposals:

            card = AIProposalCard(
                proposal
            )

            card.accepted.connect(
                self._accept_proposal
            )

            card.rejected.connect(
                self._reject_proposal
            )

            card.modified.connect(
                self._modify_proposal
            )

            self.proposals_layout.insertWidget(
                self.proposals_layout.count() - 1,
                card
            )

        self._update_validation_button()

    # ==================================================================
    # ACTIONS
    # ==================================================================

    def _accept_proposal(self, proposal):

        if proposal not in self.accepted_proposals:

            self.accepted_proposals.append(
                proposal
            )

        proposal.selected = True

        self._update_validation_button()

    def _reject_proposal(self, proposal):

        if proposal in self.accepted_proposals:

            self.accepted_proposals.remove(
                proposal
            )

        proposal.selected = False

        self._update_validation_button()

        QMessageBox.information(
            self,
            "Proposal rejected",
            f'The proposal "{proposal.title}" has been rejected.'
        )

    def _modify_proposal(self, proposal):

        QMessageBox.information(
            self,
            "Modification",
            "Proposal modification will be implemented "
            "in the next step."
        )

    def _validate_proposals(self):

        if not self.accepted_proposals:

            QMessageBox.warning(
                self,
                "No proposals selected",
                "Please accept at least one AI proposal "
                "before validation."
            )

            return

        self.validation_requested.emit()

    # ==================================================================
    # HELPERS
    # ==================================================================

    def _update_validation_button(self):

        self.validate_button.setEnabled(
            bool(self.accepted_proposals)
        )

    def _clear_proposals(self):

        while self.proposals_layout.count():

            item = self.proposals_layout.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()

        self.proposals_layout.addStretch()