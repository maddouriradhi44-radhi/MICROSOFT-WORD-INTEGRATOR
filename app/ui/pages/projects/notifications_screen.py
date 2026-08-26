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

from models.notification import Notification
from services.notification_service import notification_service
class NotificationRow(QFrame):
    """
    Represents one notification in the notifications list.
    """

    read_requested = Signal(int)

    def __init__(self, notification: Notification, parent=None):
        super().__init__(parent)

        self.notification = notification

        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #ECEEF2;
                border-radius: 10px;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(6)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel(notification.title)
        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 14px;
                font-weight: 700;
                border: none;
            }
            """
        )

        header_layout.addWidget(title)
        header_layout.addStretch()

        if not notification.is_read:
            unread_label = QLabel("NEW")
            unread_label.setStyleSheet(
                """
                QLabel {
                    background-color: #E8F0FE;
                    color: #3E63DD;
                    border-radius: 8px;
                    padding: 3px 8px;
                    font-size: 10px;
                    font-weight: 700;
                    border: none;
                }
                """
            )

            header_layout.addWidget(unread_label)

        layout.addLayout(header_layout)

        # Message
        message = QLabel(notification.message)
        message.setWordWrap(True)
        message.setStyleSheet(
            """
            QLabel {
                color: #4B5563;
                font-size: 13px;
                border: none;
            }
            """
        )

        layout.addWidget(message)

        # Footer
        footer_layout = QHBoxLayout()

        type_label = QLabel(
            f"{notification.type} · {notification.level}"
        )

        type_label.setStyleSheet(
            """
            QLabel {
                color: #8A94A6;
                font-size: 11px;
                border: none;
            }
            """
        )

        footer_layout.addWidget(type_label)
        footer_layout.addStretch()

        if not notification.is_read:
            read_button = QPushButton("Mark as read")
            read_button.setCursor(Qt.PointingHandCursor)

            read_button.setStyleSheet(
                """
                QPushButton {
                    color: #3E63DD;
                    background-color: transparent;
                    border: none;
                    font-size: 11px;
                    font-weight: 600;
                }

                QPushButton:hover {
                    text-decoration: underline;
                }
                """
            )

            read_button.clicked.connect(
                lambda: self.read_requested.emit(
                    notification.id
                )
            )

            footer_layout.addWidget(read_button)

        layout.addLayout(footer_layout)


class NotificationsScreen(QWidget):
    """
    Displays the notifications of the current user.
    """

    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.notifications = []

        # Pagination
        self.current_page = 1
        self.page_size = 5
        self.total_pages = 1
        self.has_next = False
        self.has_previous = False
        self.setStyleSheet(
            """
            QWidget {
                background-color: #F7F8FA;
            }
            """
        )

        self._build_ui()
        self.load_notifications()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        header_layout = QHBoxLayout()
        back_button = QPushButton("← Back")
        back_button.setCursor(Qt.PointingHandCursor)

        back_button.setStyleSheet(
            """
            QPushButton {
                color: #3E63DD;
                background-color: transparent;
                border: none;
                font-size: 12px;
                font-weight: 600;
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
        title = QLabel("Notifications")
        title.setStyleSheet(
            """
            QLabel {
                color: #14171F;
                font-size: 24px;
                font-weight: 700;
            }
            """
        )

        header_layout.addWidget(title)
        header_layout.addStretch()

        mark_all_button = QPushButton("Mark all as read")
        mark_all_button.setCursor(Qt.PointingHandCursor)

        mark_all_button.setStyleSheet(
            """
            QPushButton {
                color: #3E63DD;
                background-color: white;
                border: 1px solid #D8DCE5;
                border-radius: 7px;
                padding: 7px 12px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #F5F6F9;
            }
            """
        )

        mark_all_button.clicked.connect(
            self._mark_all_as_read
        )

        header_layout.addWidget(mark_all_button)

        main_layout.addLayout(header_layout)

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            """
        )

        self.container = QWidget()
        self.notifications_layout = QVBoxLayout(
            self.container
        )

        self.notifications_layout.setContentsMargins(
            0, 0, 0, 0
        )

        self.notifications_layout.setSpacing(10)

        self.scroll.setWidget(self.container)

        main_layout.addWidget(self.scroll)
        # ==========================================================
        # PAGINATION
        # ==========================================================

        pagination_layout = QHBoxLayout()

        self.previous_button = QPushButton("← Previous")
        self.previous_button.setCursor(Qt.PointingHandCursor)

        self.previous_button.setStyleSheet(
            """
            QPushButton {
                color: #3E63DD;
                background-color: white;
                border: 1px solid #D8DCE5;
                border-radius: 7px;
                padding: 7px 12px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:disabled {
                color: #A0A6B1;
                background-color: #F2F3F5;
            }

            QPushButton:hover:enabled {
                background-color: #F5F6F9;
            }
            """
        )

        self.previous_button.clicked.connect(
            self._previous_page
        )

        self.page_label = QLabel("Page 1 / 1")
        self.page_label.setAlignment(Qt.AlignCenter)

        self.page_label.setStyleSheet(
            """
            QLabel {
                color: #4B5563;
                font-size: 12px;
                font-weight: 600;
            }
            """
        )

        self.next_button = QPushButton("Next →")
        self.next_button.setCursor(Qt.PointingHandCursor)

        self.next_button.setStyleSheet(
            """
            QPushButton {
                color: #3E63DD;
                background-color: white;
                border: 1px solid #D8DCE5;
                border-radius: 7px;
                padding: 7px 12px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:disabled {
                color: #A0A6B1;
                background-color: #F2F3F5;
            }

            QPushButton:hover:enabled {
                background-color: #F5F6F9;
            }
            """
        )

        self.next_button.clicked.connect(
            self._next_page
        )

        pagination_layout.addStretch()
        pagination_layout.addWidget(self.previous_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addStretch()

        main_layout.addLayout(pagination_layout)

    def load_notifications(self):
        try:
            data = notification_service.get_notifications(
                page=self.current_page,
                page_size=self.page_size,
            )

            self.notifications = [
                Notification.from_dict(item)
                for item in data["items"]
            ]

            # Pagination metadata
            self.total_pages = data["total_pages"]
            self.has_next = data["has_next"]
            self.has_previous = data["has_previous"]

            self._display_notifications()

        except Exception as exc:
            self._show_error(str(exc))

    def _display_notifications(self):
        self._clear_notifications()

        self._update_pagination()

        if not self.notifications:
            empty_label = QLabel(
                "You don't have any notifications."
            )

            empty_label.setAlignment(Qt.AlignCenter)

            empty_label.setStyleSheet(
                """
                QLabel {
                    color: #8A94A6;
                    font-size: 13px;
                    padding: 40px;
                }
                """
            )

            self.notifications_layout.addWidget(
                empty_label
            )

            self.notifications_layout.addStretch()
            return

        for notification in self.notifications:
            row = NotificationRow(notification)

            row.read_requested.connect(
                self._mark_as_read
            )

            self.notifications_layout.addWidget(row)

        self.notifications_layout.addStretch()

    def _update_pagination(self):
        self.page_label.setText(
            f"Page {self.current_page} / {self.total_pages}"
        )

        self.previous_button.setEnabled(
            self.has_previous
        )

        self.next_button.setEnabled(
            self.has_next
        )

    def _previous_page(self):
        if self.has_previous:
            self.current_page -= 1
            self.load_notifications()


    def _next_page(self):
        if self.has_next:
            self.current_page += 1
            self.load_notifications()

    def _mark_as_read(self, notification_id: int):
        try:
            response = notification_service.mark_as_read(
                notification_id
            )

            if response:
                self.load_notifications()

        except Exception as exc:
            self._show_error(str(exc))

    def _mark_all_as_read(self):
        try:
            response = notification_service.mark_all_as_read()

            if response:
                self.load_notifications()

        except Exception as exc:
            self._show_error(str(exc))

    def _clear_notifications(self):
        while self.notifications_layout.count():
            item = self.notifications_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _show_error(self, message: str):
        print("NOTIFICATION ERROR:", message)

        self._clear_notifications()

        error_label = QLabel(
            f"Unable to load notifications.\n\n{message}"
        )    
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setWordWrap(True)

        error_label.setStyleSheet(
            """
            QLabel {
                color: #B42318;
                font-size: 13px;
                padding: 40px;
            }
            """
        )

        self.notifications_layout.addWidget(
            error_label
        )

        self.notifications_layout.addStretch()