from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QDialog,
    QLineEdit,
)

from app.ui.services.section_service import section_service
from app.ui.services.version_service import version_service


class RestoreVersionDialog(QDialog):
    """
    Dialog used to confirm restoration of a version.
    """

    def __init__(self, version_number, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Restore Version")
        self.setModal(True)

        self.setMinimumWidth(420)
        self.setMinimumHeight(220)

        self.setStyleSheet(
            """
            QDialog {
                background-color: #F7F8FA;
            }

            QLabel {
                background-color: transparent;
                border: none;
            }

            QLineEdit {
                color: #374151;
                background-color: white;
                border: 1px solid #D1D5DB;
                border-radius: 7px;
                padding: 9px 10px;
                font-size: 12px;
            }

            QLineEdit:focus {
                border: 1px solid #3E63DD;
            }

            QPushButton {
                border: none;
                border-radius: 7px;
                padding: 9px 16px;
                font-size: 12px;
                font-weight: 600;
            }
            """
        )

        self._build_ui(version_number)

    def _build_ui(self, version_number):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        main_layout.setSpacing(14)

        # ======================================================
        # TITLE
        # ======================================================

        title = QLabel("Restore Version")

        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 18px;
                font-weight: 700;
            }
            """
        )

        main_layout.addWidget(title)

        # ======================================================
        # DESCRIPTION
        # ======================================================

        description = QLabel(
            f"Restore Version {version_number}?"
        )

        description.setStyleSheet(
            """
            QLabel {
                color: #374151;
                font-size: 13px;
            }
            """
        )

        main_layout.addWidget(description)

        information = QLabel(
            "The selected version will become the current "
            "section content."
        )

        information.setWordWrap(True)

        information.setStyleSheet(
            """
            QLabel {
                color: #6B7280;
                font-size: 11px;
            }
            """
        )

        main_layout.addWidget(information)

        # ======================================================
        # COMMENT
        # ======================================================

        comment_label = QLabel("Optional comment")

        comment_label.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 11px;
                font-weight: 600;
            }
            """
        )

        main_layout.addWidget(comment_label)

        self.comment_input = QLineEdit()

        self.comment_input.setPlaceholderText(
            "Enter an optional comment..."
        )

        main_layout.addWidget(self.comment_input)

        # ======================================================
        # BUTTONS
        # ======================================================

        buttons_layout = QHBoxLayout()

        buttons_layout.addStretch()

        cancel_button = QPushButton("Cancel")

        cancel_button.setCursor(
            Qt.PointingHandCursor
        )

        cancel_button.setStyleSheet(
            """
            QPushButton {
                color: #374151;
                background-color: #E5E7EB;
            }

            QPushButton:hover {
                background-color: #D1D5DB;
            }
            """
        )

        cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(cancel_button)

        restore_button = QPushButton("Restore")

        restore_button.setCursor(
            Qt.PointingHandCursor
        )

        restore_button.setStyleSheet(
            """
            QPushButton {
                color: white;
                background-color: #3E63DD;
            }

            QPushButton:hover {
                background-color: #3154C6;
            }
            """
        )

        restore_button.clicked.connect(self.accept)

        buttons_layout.addWidget(restore_button)

        main_layout.addLayout(buttons_layout)

        self.comment_input.setFocus()

    def get_comment(self):
        return self.comment_input.text().strip()


class SectionWorkspaceScreen(QWidget):
    """
    Workspace used by a collaborator to work on a section.

    Responsibilities:
    - Display section information.
    - Edit section content.
    - Save section changes.
    - Display version history.
    - Preview a selected version.
    - Restore a previous version.
    """

    back_requested = Signal()

    def __init__(self, section=None, user=None, parent=None):
        super().__init__(parent)

        self.section = section
        self.user = user

        self.versions = []
        self.selected_version = None

        self.setStyleSheet(
            """
            QWidget {
                background-color: #F7F8FA;
            }
            """
        )

        self._build_ui()

        if self.section is not None:
            self._load_versions()

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def _build_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        main_layout.setSpacing(18)

        # ======================================================
        # HEADER
        # ======================================================

        header_layout = QHBoxLayout()

        back_button = QPushButton(
            "Back to My Sections"
        )

        back_button.setCursor(
            Qt.PointingHandCursor
        )

        back_button.setStyleSheet(
            """
            QPushButton {
                color: #3E63DD;
                background-color: transparent;
                border: none;
                font-size: 12px;
                font-weight: 600;
                padding: 4px;
            }

            QPushButton:hover {
                text-decoration: underline;
            }
            """
        )

        back_button.clicked.connect(
            self.back_requested.emit
        )

        header_layout.addWidget(back_button)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # ======================================================
        # SECTION TITLE
        # ======================================================

        section_title = (
            self.section.title
            if self.section is not None
            else "Section Workspace"
        )

        self.section_title_label = QLabel(
            section_title
        )

        self.section_title_label.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 24px;
                font-weight: 700;
                border: none;
                background-color: transparent;
            }
            """
        )

        main_layout.addWidget(
            self.section_title_label
        )

        # ======================================================
        # INFORMATION CARD
        # ======================================================

        info_card = QFrame()

        info_card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }
            """
        )

        info_layout = QHBoxLayout(info_card)

        info_layout.setContentsMargins(
            18,
            14,
            18,
            14,
        )

        info_layout.setSpacing(12)

        section_id = (
            self.section.id
            if self.section is not None
            else "-"
        )

        document_id = (
            self.section.document_id
            if self.section is not None
            else "-"
        )

        module = (
            self.section.module
            if self.section is not None
            else "-"
        )

        status = (
            self.section.status
            if self.section is not None
            else "-"
        )

        info_layout.addWidget(
            self._create_info_item(
                "Section ID",
                section_id,
            )
        )

        info_layout.addWidget(
            self._create_info_item(
                "Document ID",
                document_id,
            )
        )

        info_layout.addWidget(
            self._create_info_item(
                "Module",
                module,
            )
        )

        info_layout.addWidget(
            self._create_info_item(
                "Status",
                status,
            )
        )

        main_layout.addWidget(info_card)

        # ======================================================
        # WORKSPACE
        # ======================================================

        workspace_layout = QHBoxLayout()

        workspace_layout.setSpacing(15)

        # ======================================================
        # CONTENT AREA
        # ======================================================

        content_container = QFrame()

        content_container.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }
            """
        )

        content_layout = QVBoxLayout(
            content_container
        )

        content_layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        content_layout.setSpacing(10)

        content_label = QLabel(
            "Section Content"
        )

        content_label.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 14px;
                font-weight: 700;
                border: none;
                background-color: transparent;
            }
            """
        )

        content_layout.addWidget(content_label)

        self.content_editor = QTextEdit()

        section_content = (
            self.section.content
            if self.section is not None
            else ""
        )

        self.content_editor.setPlainText(
            section_content
        )

        self.content_editor.setPlaceholderText(
            "Section content..."
        )

        self.content_editor.setStyleSheet(
            """
            QTextEdit {
                color: #374151;
                font-size: 13px;
                padding: 12px;
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
            }

            QTextEdit:focus {
                border: 1px solid #3E63DD;
            }
            """
        )

        content_layout.addWidget(
            self.content_editor,
            1,
        )

        # ======================================================
        # SAVE BUTTON
        # ======================================================

        buttons_layout = QHBoxLayout()

        buttons_layout.addStretch()

        self.save_button = QPushButton(
            "Save Changes"
        )

        self.save_button.setCursor(
            Qt.PointingHandCursor
        )

        self.save_button.setStyleSheet(
            """
            QPushButton {
                color: white;
                background-color: #3E63DD;
                border: none;
                border-radius: 7px;
                padding: 9px 18px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #3154C6;
            }

            QPushButton:disabled {
                background-color: #9CA3AF;
            }
            """
        )

        self.save_button.clicked.connect(
            self._save_changes
        )

        buttons_layout.addWidget(
            self.save_button
        )

        content_layout.addLayout(
            buttons_layout
        )

        workspace_layout.addWidget(
            content_container,
            3,
        )

        # ======================================================
        # VERSION HISTORY
        # ======================================================

        version_container = QFrame()

        version_container.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }
            """
        )

        version_layout = QVBoxLayout(
            version_container
        )

        version_layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        version_layout.setSpacing(10)

        version_title = QLabel(
            "Version History"
        )

        version_title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 14px;
                font-weight: 700;
                border: none;
                background-color: transparent;
            }
            """
        )

        version_layout.addWidget(version_title)

        self.version_list = QListWidget()

        self.version_list.setStyleSheet(
            """
            QListWidget {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                color: #374151;
                font-size: 12px;
            }

            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F0F1F3;
            }

            QListWidget::item:selected {
                background-color: #E8F0FE;
                color: #14171F;
            }
            """
        )

        self.version_list.itemClicked.connect(
            self._handle_version_selected
        )

        version_layout.addWidget(
            self.version_list,
            1,
        )

        # ======================================================
        # RESTORE BUTTON
        # ======================================================

        self.restore_button = QPushButton(
            "Restore Selected Version"
        )

        self.restore_button.setCursor(
            Qt.PointingHandCursor
        )

        self.restore_button.setEnabled(False)

        self.restore_button.setStyleSheet(
            """
            QPushButton {
                color: white;
                background-color: #6B7280;
                border: none;
                border-radius: 7px;
                padding: 9px 12px;
                font-size: 11px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #4B5563;
            }

            QPushButton:disabled {
                background-color: #D1D5DB;
            }
            """
        )

        self.restore_button.clicked.connect(
            self._restore_selected_version
        )

        version_layout.addWidget(
            self.restore_button
        )

        workspace_layout.addWidget(
            version_container,
            1,
        )

        main_layout.addLayout(
            workspace_layout,
            1,
        )

        # ======================================================
        # MESSAGE
        # ======================================================

        self.message_label = QLabel("")

        self.message_label.setAlignment(
            Qt.AlignRight
        )

        self.message_label.setStyleSheet(
            """
            QLabel {
                color: #067647;
                font-size: 12px;
                padding: 2px;
                border: none;
                background-color: transparent;
            }
            """
        )

        main_layout.addWidget(
            self.message_label
        )

    # ==========================================================
    # INFO ITEM
    # ==========================================================

    def _create_info_item(self, label, value):
        container = QFrame()

        container.setStyleSheet(
            """
            QFrame {
                border: none;
                background-color: transparent;
            }
            """
        )

        layout = QVBoxLayout(container)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(3)

        label_widget = QLabel(
            str(label)
        )

        label_widget.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 10px;
                font-weight: 600;
                border: none;
                background-color: transparent;
            }
            """
        )

        value_widget = QLabel(
            str(value)
        )

        value_widget.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 13px;
                font-weight: 600;
                border: none;
                background-color: transparent;
            }
            """
        )

        value_widget.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        layout.addWidget(label_widget)
        layout.addWidget(value_widget)

        return container

    # ==========================================================
    # MESSAGE HELPERS
    # ==========================================================

    def _show_success(self, message):
        self.message_label.setText(message)

        self.message_label.setStyleSheet(
            """
            QLabel {
                color: #067647;
                font-size: 12px;
                border: none;
                background-color: transparent;
            }
            """
        )

    def _show_info(self, message):
        self.message_label.setText(message)

        self.message_label.setStyleSheet(
            """
            QLabel {
                color: #3E63DD;
                font-size: 12px;
                border: none;
                background-color: transparent;
            }
            """
        )

    def _show_error(self, message):
        self.message_label.setText(message)

        self.message_label.setStyleSheet(
            """
            QLabel {
                color: #B42318;
                font-size: 12px;
                border: none;
                background-color: transparent;
            }
            """
        )

    # ==========================================================
    # LOAD VERSIONS
    # ==========================================================

    def _load_versions(self):
        self.version_list.clear()

        self.restore_button.setEnabled(False)
        self.selected_version = None

        if self.section is None:
            return

        try:
            self.versions = version_service.get_history(
                self.section.id
            )

            if not self.versions:
                item = QListWidgetItem(
                    "No versions available"
                )

                item.setFlags(Qt.NoItemFlags)

                self.version_list.addItem(item)

                return

            for version in self.versions:
                current_text = ""

                if version.is_current:
                    current_text = " • CURRENT"

                archived_text = ""

                if version.is_archived:
                    archived_text = " • ARCHIVED"

                item_text = (
                    f"Version {version.version_number}"
                    f"{current_text}"
                    f"{archived_text}"
                )

                item = QListWidgetItem(item_text)

                item.setData(
                    Qt.UserRole,
                    version.id,
                )

                self.version_list.addItem(item)

        except Exception as error:
            self._show_error(str(error))

    # ==========================================================
    # VERSION SELECTED
    # ==========================================================

    def _handle_version_selected(self, item):
        version_id = item.data(Qt.UserRole)

        if version_id is None:
            self.restore_button.setEnabled(False)
            self.selected_version = None
            return

        selected_version = None

        for version in self.versions:
            if version.id == version_id:
                selected_version = version
                break

        if selected_version is None:
            self.restore_button.setEnabled(False)
            self.selected_version = None
            return

        self.selected_version = selected_version

        # Display selected version content
        self.content_editor.setPlainText(
            selected_version.content_snapshot
        )

        # Current version cannot be restored
        self.restore_button.setEnabled(
            not selected_version.is_current
        )

        self._show_info(
            f"Version "
            f"{selected_version.version_number} "
            f"selected."
        )

    # ==========================================================
    # RESTORE VERSION
    # ==========================================================

    def _restore_selected_version(self):
        selected_version = self.selected_version

        if selected_version is None:
            return

        if selected_version.is_current:
            self._show_info(
                "This version is already the current version."
            )
            return

        # ------------------------------------------------------
        # Confirmation dialog
        # ------------------------------------------------------

        dialog = RestoreVersionDialog(
            version_number=selected_version.version_number,
            parent=self,
        )

        result = dialog.exec()

        if result != QDialog.Accepted:
            return

        comment = dialog.get_comment()

        self.restore_button.setEnabled(False)

        try:
            # --------------------------------------------------
            # Restore through frontend service
            # --------------------------------------------------

            restored_version = (
                version_service.restore_version(
                    selected_version.id
                )
            )

            if restored_version is None:
                raise Exception(
                    "Unable to restore the selected version."
                )

            # --------------------------------------------------
            # Update UI with restored content
            # --------------------------------------------------

            restored_content = (
                restored_version.content_snapshot
            )

            self.content_editor.setPlainText(
                restored_content
            )

            self.section.content = restored_content

            # Keep the comment locally available if the
            # returned object exposes it.
            if comment:
                try:
                    restored_version.change_comment = comment
                except Exception:
                    pass

            self._show_success(
                (
                    f"Version "
                    f"{selected_version.version_number} "
                    "restored successfully."
                )
            )

            # Reload version history
            self._load_versions()

        except Exception as error:
            self._show_error(str(error))

        finally:
            self.restore_button.setEnabled(False)

    # ==========================================================
    # SAVE CHANGES
    # ==========================================================

    def _save_changes(self):
        if self.section is None:
            self._show_error(
                "No section selected."
            )
            return

        content = (
            self.content_editor.toPlainText()
        )

        old_content = self.section.content

        # Nothing changed
        if content == old_content:
            self._show_info(
                "No changes to save."
            )
            return

        self.save_button.setEnabled(False)
        self.save_button.setText("Saving...")

        try:
            updated_section = (
                section_service.update_section(
                    section_id=self.section.id,
                    content=content,
                )
            )

            if updated_section is None:
                raise Exception(
                    "Unable to update the section."
                )

            self.section = updated_section

            # --------------------------------------------------
            # Create a version after successful modification
            # --------------------------------------------------

            version_service.create_version(
                section_id=self.section.id,
                title_snapshot=self.section.title,
                content_snapshot=content,
                change_comment="Section content updated",
            )

            self.content_editor.setPlainText(
                updated_section.content
            )

            self._show_success(
                "Section saved successfully."
            )

            self._load_versions()

        except Exception as error:
            self._show_error(str(error))

        finally:
            self.save_button.setEnabled(True)
            self.save_button.setText("Save Changes")