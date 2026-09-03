Backend
│
├── Auth
│   ├── Register utilisateur
│   ├── Login JWT
│   ├── Refresh Token
│   ├── Vérification Email
│   ├── Reset Password
│   ├── Gestion des rôles
│   └── Sécurité
│       ├── Hash password
│       └── Permissions
│
├── Users
│   ├── Création utilisateur
│   ├── Modification profil
│   ├── Suppression utilisateur
│   ├── Recherche utilisateur
│   ├── Gestion informations personnelles
│   └── Permissions globales
│
├── Projects
│   ├── Création projet
│   ├── Modification projet
│   ├── Suppression projet
│   ├── Ajout membres
│   ├── Suppression membres
│   ├── Gestion rôles projet
│   │   ├── Project Manager
│   │   ├── Collaborateur
│   │   └── Lecteur
│   └── Liste projets utilisateur
│
├── Documents
│   ├── Import DOCX
│   ├── Stockage fichier
│   ├── Association au projet
│   ├── Informations document
│   ├── Statut document
│   ├── Suppression document
│   ├── Téléchargement document
│   └── Intégration DocumentBlocks
│
├── Sections
│   ├── Création sections
│   ├── Découpage logique document
│   ├── Affectation collaborateur
│   ├── Modification section
│   ├── Suppression section
│   ├── Gestion statut
│   ├── Permissions par section
│   ├── Suivi progression
│   └── Intégration DocumentBlocks
│
├── DocumentBlocks
│   ├── Modèle DocumentBlock
│   ├── Repository DocumentBlock
│   ├── Schémas DocumentBlock
│   ├── Service DocumentBlock
│   ├── API DocumentBlock
│   │   ├── Création block
│   │   ├── Récupération block
│   │   ├── Récupération blocks d'une section
│   │   ├── Modification block
│   │   └── Suppression block
│   │
│   ├── Extraction paragraphes Word
│   ├── Extraction titres
│   ├── Extraction tableaux
│   ├── Extraction images
│   ├── Conservation format OOXML
│   ├── Reconstruction document
│   ├── Gestion ordre des blocs
│   ├── Association Block → Section
│   ├── Conservation content_xml
│   └── Gestion section_break
│
├── Versioning
│   ├── Création nouvelle version
│   ├── Historique modifications
│   ├── Comparaison versions
│   ├── Retour version précédente
│   ├── Stockage anciennes versions
│   └── Traçabilité modifications
│
├── Validation
│   ├── Envoi section pour validation
│   ├── Validation chef projet
│   ├── Refus modification
│   ├── Commentaire validation
│   ├── Changement statut section
│   └── Historique validation
│
├── Comments
│   ├── Création commentaire
│   ├── Modification commentaire
│   ├── Suppression commentaire
│   ├── Commentaire sur section
│   ├── Statut commentaire
│   │   ├── OPEN
│   │   └── RESOLVED
│   ├── Commentaires parents
│   ├── Réponses
│   ├── Gestion discussions
│   └── Mentions utilisateurs
│       ├── Détection @username
│       ├── Recherche utilisateur
│       ├── Création CommentMention
│       └── Association commentaire ↔ utilisateur
│
├── Notifications
│   ├── Création notification
│   ├── Consultation notifications
│   ├── Notifications non lues
│   ├── Compteur notifications non lues
│   ├── Marquer comme lue
│   ├── Marquer toutes comme lues
│   ├── Suppression notification
│   │
│   ├── Types
│   │   ├── SECURITY
│   │   ├── PROJECT
│   │   ├── DOCUMENT
│   │   ├── SECTION
│   │   ├── COMMENT
│   │   ├── MENTION
│   │   ├── VALIDATION
│   │   ├── VERSION
│   │   ├── LOCK
│   │   ├── SCHEDULER
│   │   └── AI
│   │
│   └── Intégrations
│       ├── Auth
│       ├── Projects
│       ├── Sections
│       ├── Versioning
│       ├── Comments
│       ├── Mentions
│       ├── Validation
│       ├── Lock
│       ├── Scheduler
│       └── AI
│
├── Audit
│   ├── Enregistrement actions utilisateur
│   ├── Login utilisateur
│   ├── Import document
│   ├── Modification section
│   ├── Création commentaire
│   ├── Mention utilisateur
│   ├── Validation
│   ├── Export
│   └── Historique sécurité
│
├── Lock
│   ├── Verrouillage document
│   ├── Verrouillage section
│   ├── Libération verrou
│   ├── Empêcher conflits édition
│   └── Gestion accès simultané
│
├── Scheduler
│   ├── Vérification verrous expirés
│   ├── Nettoyage automatique
│   ├── Tâches programmées
│   └── Maintenance automatique
│
├── Storage
│   ├── Sauvegarde fichiers
│   ├── Gestion chemins fichiers
│   ├── UUID fichiers
│   ├── Suppression fichiers inutiles
│   └── Sécurité stockage
│
├── Export DOCX
│   ├── Reconstruction document final
│   ├── Fusion sections
│   ├── Reconstruction blocs
│   ├── Conservation format Word
│   ├── Génération fichier final
│   └── Téléchargement
│
└── AI
│
├── 1. Analyse du document
│   ├── Détection de structure
│   ├── Détection des sections
│   ├── Décomposition logique
│   ├── Hiérarchie
│   ├── Ordre
│   ├── Catégorie
│   ├── Rôle suggéré
│   ├── Mots-clés
│   ├── Complexité
│   ├── Justification
│   └── Score de confiance
│
├── 2. Proposition au Chef de Projet
│   ├── Sections proposées
│   ├── Sous-sections proposées
│   ├── Modification de la proposition
│   ├── Acceptation
│   └── Refus
│
├── 3. Comparaison des versions
│   ├── Ancienne version / nouvelle version
│   ├── Ajouts
│   ├── Suppressions
│   ├── Modifications
│   └── Localisation des changements
│
├── 4. Résumé des modifications
│   ├── Résumé automatique
│   ├── Changements importants
│   ├── Impact de la modification
│   └── Génération du rapport
│
├── 5. Analyse de cohérence
│   ├── Contradiction
│   ├── Incohérence
│   ├── Informations manquantes
│   ├── Cohérence avec le document
│   └── Cohérence avec les sections liées
│
├── 6. Détection des risques
│   ├── Suppression importante
│   ├── Contradiction
│   ├── Incohérence
│   ├── Contenu suspect
│   └── Niveau de risque
│       ├── Faible
│       ├── Moyen
│       └── Critique
│
├── 7. Score de confiance
│   ├── Score numérique
│   ├── Faible
│   ├── Moyen
│   └── Élevé
│
├── 8. Recommandation
│   ├── Accepter modification
│   ├── Vérifier modification
│   ├── Refuser modification
│   └── Justification
│
├── 9. Gestion de l'analyse
│   ├── En attente
│   ├── En cours
│   ├── Terminée
│   └── Échec
│
├── 10. Historique IA
│   ├── Analyse par version
│   ├── Résultat
│   ├── Risques
│   ├── Score
│   ├── Recommandation
│   └── Date
│
└── 11. Rapport pour Chef de Projet
    ├── Dashboard IA
    ├── Résumé section
    ├── Changements détectés
    ├── Changements importants
    ├── Risques
    ├── Score de confiance
    ├── Recommandation
    ├── Justification
    └── Décision finale du Chef de Projet