# ── Étape 1 : image de base légère Python 3.11 ──────────────────────────────
FROM python:3.11-slim

# ── Étape 2 : répertoire de travail dans le conteneur ───────────────────────
WORKDIR /app

# ── Étape 3 : copie et installation des dépendances ─────────────────────────
# On copie d'abord requirements.txt seul pour profiter du cache Docker :
# si le code change mais pas les deps, cette couche n'est pas reconstruite.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Étape 4 : copie du code source ──────────────────────────────────────────
COPY main.py .

# ── Étape 5 : variables d'environnement par défaut ──────────────────────────
# Ces valeurs sont écrasées au déploiement Cloud Run via --set-env-vars
ENV PORT=8080
ENV GCS_BUCKET_NAME=mon-bucket-api
ENV GCS_FILE_PATH=data/entries.json
ENV GCP_PROJECT_ID=mon-projet-gcp
ENV GCP_REGION=us-central1

# ── Étape 6 : exposition du port ─────────────────────────────────────────────
EXPOSE 8080

# ── Étape 7 : démarrage avec Gunicorn (serveur WSGI production) ──────────────
# 1 worker suffit pour Cloud Run (il scale horizontalement)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "main:app"]
