from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
)


class AIProposalCard(QFrame):

    accept_requested = Signal(int)
    reject_requested = Signal(int)
    modify_requested = Signal(int)

    def __init__(self, proposal, parent=None):
        super().__init__(parent)

        self.proposal = proposal
        proposal_id = proposal.get("id")

        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        # Header
        header = QHBoxLayout()

        title = QLabel(
            proposal.get("title", "Untitled proposal")
        )
        title.setStyleSheet("""
            QLabel {
                color: #14171F;
                font-size: 15px;
                font-weight: 700;
                border: none;
            }
        """)

        header.addWidget(title, 1)

        status = QLabel(
            proposal.get("status", "PENDING").upper()
        )
        status.setStyleSheet("""
            QLabel {
                background-color: #FFF4E5;
                color: #B76E00;
                border-radius: 10px;
                padding: 4px 10px;
                font-size: 10px;
                font-weight: 700;
            }
        """)

        header.addWidget(status)

        layout.addLayout(header)

        # Content
        content = QLabel(
            proposal.get("content", "")
        )
        content.setWordWrap(True)
        content.setStyleSheet("""
            QLabel {
                color: #596579;
                font-size: 12px;
                border: none;
            }
        """)

        layout.addWidget(content)

        # Metadata
        metadata = QLabel(
            f"Level: {proposal.get('level', '-')}"
            f"   •   Order: {proposal.get('order', '-')}"
            f"   •   Category: {proposal.get('category', '-')}"
            f"   •   Complexity: {proposal.get('complexity', '-')}"
        )

        metadata.setStyleSheet("""
            QLabel {
                color: #8A94A6;
                font-size: 11px;
                border: none;
            }
        """)

        layout.addWidget(metadata)

        confidence = QLabel(
            f"AI Confidence: {proposal.get('confidence', '-')}"
        )

        confidence.setStyleSheet("""
            QLabel {
                color: #3E63DD;
                font-size: 11px;
                font-weight: 600;
                border: none;
            }
        """)

        layout.addWidget(confidence)

        role = QLabel(
            f"Suggested role: {proposal.get('suggested_role', '-')}"
        )

        role.setStyleSheet("""
            QLabel {
                color: #596579;
                font-size: 11px;
                border: none;
            }
        """)

        layout.addWidget(role)

        reason = QLabel(
            f"Reason: {proposal.get('reason', '-')}"
        )

        reason.setWordWrap(True)

        reason.setStyleSheet("""
            QLabel {
                color: #596579;
                font-size: 11px;
                border: none;
            }
        """)

        layout.addWidget(reason)

        keywords = proposal.get("keywords", [])

        if isinstance(keywords, list):
            keywords = ", ".join(str(keyword) for keyword in keywords)

        keywords_label = QLabel(
            f"Keywords: {keywords or '-'}"
        )

        keywords_label.setWordWrap(True)

        keywords_label.setStyleSheet("""
            QLabel {
                color: #596579;
                font-size: 11px;
                border: none;
            }
        """)

        layout.addWidget(keywords_label)

        # Buttons
        buttons = QHBoxLayout()
        buttons.addStretch()

        modify_btn = QPushButton("Modify")
        accept_btn = QPushButton("Accept")
        reject_btn = QPushButton("Reject")

        for btn in (modify_btn, accept_btn, reject_btn):
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(32)

        modify_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #D8DCE5;
                border-radius: 6px;
                padding: 0 14px;
                color: #14171F;
            }
            QPushButton:hover {
                background-color: #F5F6F9;
            }
        """)

        accept_btn.setStyleSheet("""
            QPushButton {
                background-color: #185ABD;
                border: none;
                border-radius: 6px;
                padding: 0 14px;
                color: white;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #144A9E;
            }
        """)

        reject_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #D8DCE5;
                border-radius: 6px;
                padding: 0 14px;
                color: #B42318;
            }
            QPushButton:hover {
                background-color: #FFF5F4;
            }
        """)

        modify_btn.clicked.connect(
            lambda: self.modify_requested.emit(proposal_id)
        )

        accept_btn.clicked.connect(
            lambda: self.accept_requested.emit(proposal_id)
        )

        reject_btn.clicked.connect(
            lambda: self.reject_requested.emit(proposal_id)
        )

        buttons.addWidget(modify_btn)
        buttons.addWidget(reject_btn)
        buttons.addWidget(accept_btn)

        layout.addLayout(buttons)


class AISectionsScreen(QWidget):

    back_requested = Signal()
    refresh_requested = Signal()
    accept_requested = Signal(int)
    reject_requested = Signal(int)
    modify_requested = Signal(int)

    def __init__(self, project=None, user=None, parent=None):
        super().__init__(parent)

        self.project = project
        self.user = user
        self.proposals = []

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(18)

        # Header
        header = QHBoxLayout()

        title = QLabel("AI Section Proposals")
        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: 700;
                color: #14171F;
            }
        """)

        header.addWidget(title)
        header.addStretch()

        back_btn = QPushButton("← Back")
        refresh_btn = QPushButton("Refresh")

        for btn in (back_btn, refresh_btn):
            btn.setCursor(Qt.PointingHandCursor)

        back_btn.clicked.connect(
            self.back_requested.emit
        )

        refresh_btn.clicked.connect(
            self.refresh_requested.emit
        )

        header.addWidget(refresh_btn)
        header.addWidget(back_btn)

        root.addLayout(header)

        # Description
        description = QLabel(
            "Review the sections proposed by AI before creating the final project sections."
        )

        description.setStyleSheet("""
            QLabel {
                color: #8A94A6;
                font-size: 13px;
            }
        """)

        description.setWordWrap(True)
        root.addWidget(description)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        container = QWidget()
        self.proposals_layout = QVBoxLayout(container)
        self.proposals_layout.setSpacing(12)
        self.proposals_layout.addStretch()

        scroll.setWidget(container)

        root.addWidget(scroll)

    def load_proposals(self, proposals):
        self.proposals = proposals or []

        while self.proposals_layout.count():
            item = self.proposals_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not self.proposals:
            empty = QLabel(
                "No AI proposals available."
            )

            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("""
                QLabel {
                    color: #8A94A6;
                    font-size: 13px;
                    padding: 40px;
                }
            """)

            self.proposals_layout.addWidget(empty)

        else:
            for proposal in self.proposals:

                card = AIProposalCard(
                    proposal
                )

                card.accept_requested.connect(
                    self.accept_requested.emit
                )

                card.reject_requested.connect(
                    self.reject_requested.emit
                )

                card.modify_requested.connect(
                    self.modify_requested.emit
                )

                self.proposals_layout.addWidget(card)

        self.proposals_layout.addStretch()