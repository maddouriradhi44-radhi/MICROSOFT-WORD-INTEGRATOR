from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QFrame, QPushButton, QScrollArea
)
from PySide6.QtCore import Qt
import qtawesome as qta


# Couleurs Capgemini utilisées dans toute la page
COLOR_PRIMARY = "#0070AD"
COLOR_PRIMARY_LIGHT = "#E6F1FB"
COLOR_TEXT_DARK = "#0C447C"
COLOR_SUCCESS_BG = "#E1F5EE"
COLOR_SUCCESS_TEXT = "#085041"
COLOR_WARNING_BG = "#FAEEDA"
COLOR_WARNING_TEXT = "#633806"
COLOR_BORDER = "#D9E2EC"


class HomePage(QWidget):
    def __init__(self, user_info=None, on_open_document=None):
        super().__init__()
        self.user_info = user_info  # infos de l'utilisateur connecté (nom, rôle)
        self.on_open_document = on_open_document  # callback pour ouvrir document_view.py

        self.setStyleSheet("background-color: #F5F7FA;")
        self._build_ui()

    def _build_ui(self):
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Zone scrollable pour que la page s'adapte si le contenu dépasse
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #F5F7FA;")

        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 24, 30, 30)
        content_layout.setSpacing(18)

        content_layout.addLayout(self._build_header())
        content_layout.addWidget(self._build_search_bar())
        content_layout.addWidget(self._build_alert_banner())
        content_layout.addWidget(self._build_documents_section())

        # Deux colonnes : tâches du jour / activité récente
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(16)
        columns_layout.addWidget(self._build_tasks_column(), stretch=13)
        columns_layout.addWidget(self._build_activity_column(), stretch=10)
        content_layout.addLayout(columns_layout)

        content_layout.addStretch()
        content.setLayout(content_layout)
        scroll.setWidget(content)

        outer_layout.addWidget(scroll)
        self.setLayout(outer_layout)

    # ---------------------------------------------------------------
    # En-tête : bienvenue + avatar
    # ---------------------------------------------------------------
    def _build_header(self):
        layout = QHBoxLayout()

        name = self.user_info.user if self.user_info else "Utilisateur"
        initials = "".join([p[0] for p in name.split()[:2]]).upper() or "U"

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        greeting = QLabel(f"Bonjour, {name}")
        greeting.setStyleSheet(f"font-size: 20px; font-weight: 600; color: {COLOR_PRIMARY};")
        text_layout.addWidget(greeting)

        subtitle = QLabel("2 sections à terminer aujourd'hui")
        subtitle.setStyleSheet("font-size: 13px; color: #555555;")
        text_layout.addWidget(subtitle)

        layout.addLayout(text_layout)
        layout.addStretch()

        avatar = QLabel(initials)
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};
            color: white;
            border-radius: 20px;
            font-weight: bold;
            font-size: 13px;
        """)
        layout.addWidget(avatar)

        return layout

    # ---------------------------------------------------------------
    # Barre de recherche
    # ---------------------------------------------------------------
    def _build_search_bar(self):
        container = QFrame()
        container.setFixedHeight(42)
        container.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {COLOR_BORDER};
                border-radius: 10px;
            }}
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        icon = QLabel()
        icon.setPixmap(qta.icon("fa5s.search", color=COLOR_PRIMARY).pixmap(16, 16))
        layout.addWidget(icon)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Rechercher un document, une section, un utilisateur")
        search_input.setStyleSheet("border: none; font-size: 13px;")
        layout.addWidget(search_input)

        container.setLayout(layout)
        return container

    # ---------------------------------------------------------------
    # Bannière d'alerte IA
    # ---------------------------------------------------------------
    def _build_alert_banner(self):
        banner = QFrame()
        banner.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_PRIMARY_LIGHT};
                border-radius: 12px;
            }}
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(10)

        icon = QLabel()
        icon.setPixmap(qta.icon("fa5s.exclamation-triangle", color=COLOR_PRIMARY).pixmap(18, 18))
        layout.addWidget(icon)

        text = QLabel(
            'La section "Sécurité réseau" a été modifiée '
            'et impacte votre section "Authentification"'
        )
        text.setStyleSheet(f"font-size: 13px; color: {COLOR_TEXT_DARK};")
        text.setWordWrap(True)
        layout.addWidget(text, stretch=1)

        arrow = QLabel()
        arrow.setPixmap(qta.icon("fa5s.chevron-right", color=COLOR_PRIMARY).pixmap(14, 14))
        layout.addWidget(arrow)

        banner.setLayout(layout)
        return banner

    # ---------------------------------------------------------------
    # Section documents (grille d'icônes)
    # ---------------------------------------------------------------
    def _build_documents_section(self):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        header = QHBoxLayout()
        title = QLabel("Mes documents")
        title.setStyleSheet("font-size: 13px; font-weight: 600; color: #555555;")
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        grid = QGridLayout()
        grid.setSpacing(14)

        documents = [
            {"name": "Cahier des charges v2", "status": "Terminé", "status_bg": COLOR_SUCCESS_BG, "status_fg": COLOR_SUCCESS_TEXT},
            {"name": "Spécifications API", "status": "En cours", "status_bg": COLOR_WARNING_BG, "status_fg": COLOR_WARNING_TEXT},
            {"name": "Rapport sécurité", "status": "En attente", "status_bg": COLOR_PRIMARY_LIGHT, "status_fg": COLOR_TEXT_DARK},
        ]

        col = 0
        for doc in documents:
            card = self._build_document_card(doc)
            grid.addWidget(card, 0, col)
            col += 1

        # Carte "Importer" à la fin de la grille
        import_card = self._build_import_card()
        grid.addWidget(import_card, 0, col)

        layout.addLayout(grid)
        container.setLayout(layout)
        return container

    def _build_document_card(self, doc):
        card = QFrame()
        card.setFixedSize(140, 130)
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
            QFrame:hover {{
                border: 1px solid {COLOR_PRIMARY};
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 16, 10, 12)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)

        # Icône dans un cercle bleu clair — même icône pour tous les documents
        icon_bg = QLabel()
        icon_bg.setFixedSize(48, 48)
        icon_bg.setAlignment(Qt.AlignCenter)
        icon_bg.setStyleSheet(f"background-color: {COLOR_PRIMARY_LIGHT}; border-radius: 12px;")
        icon_bg.setPixmap(qta.icon("fa5s.file-alt", color=COLOR_PRIMARY).pixmap(22, 22))
        layout.addWidget(icon_bg, alignment=Qt.AlignCenter)

        name = QLabel(doc["name"])
        name.setAlignment(Qt.AlignCenter)
        name.setWordWrap(True)
        name.setStyleSheet("font-size: 11px;")
        layout.addWidget(name)

        status = QLabel(doc["status"])
        status.setAlignment(Qt.AlignCenter)
        status.setStyleSheet(f"""
            background-color: {doc['status_bg']};
            color: {doc['status_fg']};
            font-size: 10px;
            border-radius: 10px;
            padding: 2px 8px;
        """)
        layout.addWidget(status, alignment=Qt.AlignCenter)

        card.setLayout(layout)

        # Clic sur la carte → ouvre le document
        card.mousePressEvent = lambda event: self._handle_open_document(doc["name"])

        return card

    def _build_import_card(self):
        card = QFrame()
        card.setFixedSize(140, 130)
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px dashed #AABBCC;
                border-radius: 12px;
            }}
            QFrame:hover {{
                border: 1px dashed {COLOR_PRIMARY};
            }}
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)

        icon = QLabel()
        icon.setAlignment(Qt.AlignCenter)
        icon.setPixmap(qta.icon("fa5s.plus", color=COLOR_PRIMARY).pixmap(20, 20))
        layout.addWidget(icon)

        text = QLabel("Importer")
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet(f"font-size: 12px; color: {COLOR_PRIMARY};")
        layout.addWidget(text)

        card.setLayout(layout)
        return card

    def _handle_open_document(self, doc_name):
        if self.on_open_document:
            self.on_open_document(doc_name)

    # ---------------------------------------------------------------
    # Colonne "Mes tâches du jour"
    # ---------------------------------------------------------------
    def _build_tasks_column(self):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        title = QLabel("Mes tâches du jour")
        title.setStyleSheet("font-size: 13px; font-weight: 600; color: #555555;")
        layout.addWidget(title)

        tasks_card = QFrame()
        tasks_card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)
        tasks_layout = QVBoxLayout()
        tasks_layout.setContentsMargins(0, 0, 0, 0)
        tasks_layout.setSpacing(0)

        tasks = [
            {"section": 'Section "Authentification"', "status": "En cours", "bg": COLOR_WARNING_BG, "fg": COLOR_WARNING_TEXT},
            {"section": 'Section "Interface login"', "status": "À commencer", "bg": COLOR_PRIMARY_LIGHT, "fg": COLOR_TEXT_DARK},
        ]

        for i, task in enumerate(tasks):
            row = self._build_task_row(task, is_last=(i == len(tasks) - 1))
            tasks_layout.addWidget(row)

        tasks_card.setLayout(tasks_layout)
        layout.addWidget(tasks_card)

        # Bloc "Reprendre où j'en étais"
        resume_title = QLabel("Reprendre où j'en étais")
        resume_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #555555; margin-top: 8px;")
        layout.addWidget(resume_title)
        layout.addWidget(self._build_resume_card())

        container.setLayout(layout)
        return container

    def _build_task_row(self, task, is_last=False):
        row = QFrame()
        border = "" if is_last else f"border-bottom: 1px solid {COLOR_BORDER};"
        row.setStyleSheet(f"QFrame {{ {border} }}")

        layout = QHBoxLayout()
        layout.setContentsMargins(14, 10, 14, 10)

        icon = QLabel()
        icon.setPixmap(qta.icon("fa5s.file-alt", color=COLOR_PRIMARY).pixmap(14, 14))
        layout.addWidget(icon)

        name = QLabel(task["section"])
        name.setStyleSheet("font-size: 12px;")
        layout.addWidget(name, stretch=1)

        status = QLabel(task["status"])
        status.setStyleSheet(f"""
            background-color: {task['bg']};
            color: {task['fg']};
            font-size: 10px;
            border-radius: 10px;
            padding: 2px 8px;
        """)
        layout.addWidget(status)

        row.setLayout(layout)
        return row

    def _build_resume_card(self):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(14, 12, 14, 12)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        doc_label = QLabel("Cahier des charges v2 — Section Login")
        doc_label.setStyleSheet("font-size: 12px;")
        text_layout.addWidget(doc_label)

        time_label = QLabel("Modifié il y a 20 minutes")
        time_label.setStyleSheet("font-size: 10px; color: #999999;")
        text_layout.addWidget(time_label)

        layout.addLayout(text_layout, stretch=1)

        arrow_btn = QPushButton()
        arrow_btn.setIcon(qta.icon("fa5s.arrow-right", color="white"))
        arrow_btn.setFixedSize(30, 30)
        arrow_btn.setCursor(Qt.PointingHandCursor)
        arrow_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: #6F2DA8;
            }}
        """)
        layout.addWidget(arrow_btn)

        card.setLayout(layout)
        return card

    # ---------------------------------------------------------------
    # Colonne "Activité récente"
    # ---------------------------------------------------------------
    def _build_activity_column(self):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        title = QLabel("Activité récente")
        title.setStyleSheet("font-size: 13px; font-weight: 600; color: #555555;")
        layout.addWidget(title)

        activity_card = QFrame()
        activity_card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)
        activity_layout = QVBoxLayout()
        activity_layout.setContentsMargins(0, 0, 0, 0)
        activity_layout.setSpacing(0)

        activities = [
            {"icon": "fa5s.comment", "text": "Radhi a commenté votre section"},
            {"icon": "fa5s.check", "text": 'Votre section "Login" a été validée'},
            {"icon": "fa5s.lock", "text": 'Nouha a verrouillé "Rapport sécurité"'},
        ]

        for i, act in enumerate(activities):
            row = self._build_activity_row(act, is_last=(i == len(activities) - 1))
            activity_layout.addWidget(row)

        activity_card.setLayout(activity_layout)
        layout.addWidget(activity_card)

        container.setLayout(layout)
        return container

    def _build_activity_row(self, activity, is_last=False):
        row = QFrame()
        border = "" if is_last else f"border-bottom: 1px solid {COLOR_BORDER};"
        row.setStyleSheet(f"QFrame {{ {border} }}")

        layout = QHBoxLayout()
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)

        icon = QLabel()
        icon.setPixmap(qta.icon(activity["icon"], color=COLOR_PRIMARY).pixmap(14, 14))
        layout.addWidget(icon)

        text = QLabel(activity["text"])
        text.setStyleSheet("font-size: 12px;")
        text.setWordWrap(True)
        layout.addWidget(text, stretch=1)

        row.setLayout(layout)
        return row
