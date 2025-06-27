# env_service

Ce dépôt est dédié à la **création** et la **configuration** des environnements par l’administrateur, ainsi qu’à l’**affectation des utilisateurs** aux environnements.

## Fonctionnalités principales

- Création, modification, suppression d’environnements
- Affectation/désaffectation d’utilisateurs à un environnement
- Gestion des profils utilisateurs
- API REST pour l’administration des environnements et des utilisateurs
- Intégration de modèles d’IA pour la détection de plans (YOLO)

## Technologies utilisées

- **Python 3.13**
- **FastAPI** : Framework web pour API rapides et documentées
- **SQLAlchemy** : ORM pour PostgreSQL
- **Uvicorn** : Serveur ASGI pour FastAPI
- **Ultralytics YOLO** : Détection d’objets sur plans
- **Pydantic** : Validation des schémas de données
- **dotenv** : Gestion des variables d’environnement

## Prérequis

- Python 3.13
- PostgreSQL
- [uv](https://github.com/astral-sh/uv) ou pip pour la gestion des dépendances

## Installation

1. **Cloner le dépôt :**

   ```bash
   git clone <url_du_repo>
   cd env_service

   ```

2. **Créer et activer un environnement virtuel : :**

   ```bash
   uv venv
   source .venv/bin/activate

   ```

3. **Installer les dépendances : : :**

   ```bash
   uv sync

   ```

4. **Configurer la base de données :**
   - opier .env.example en .env et renseigner la variable DATABASE_URL.

## Lancement du projet

```bash
uvicorn app.main:app --reload


env_service/
├── app/
│   ├── api/           # Routes FastAPI
│   ├── core/          # Modèles, config, DB
│   ├── models/        # Modèles IA (YOLO)
│   ├── schemas/       # Schémas Pydantic
│   └── services/      # Logique métier
├── sql/               # Scripts SQL de seed
├── .env               # Variables d’environnement
├── requirements.txt
├── pyproject.toml
└── README.md
```
