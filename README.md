# 🚀 Mini Projet API — Flask + GCP + Docker

Mini API Python déployée sur **Google Cloud Run**, avec lecture/écriture sur **GCS** et génération de poèmes via **Vertex AI (Gemini)**.

---

## 📁 Structure du projet

```
mini_projet/
├── api/
│   ├── main.py            # Code Flask de l'API
│   ├── requirements.txt   # Dépendances Python
│   └── Dockerfile         # Image Docker de l'API
├── frontend/
│   ├── index.html         # Dashboard HTML/JS
│   └── Dockerfile         # Image Docker Nginx
└── README.md
```

---

## ⚙️ Variables d'environnement

| Variable | Description | Exemple |
|---|---|---|
| `GCS_BUCKET_NAME` | Nom de votre bucket GCS | `mon-bucket-api` |
| `GCS_FILE_PATH` | Chemin du fichier JSON dans le bucket | `data/entries.json` |
| `GCP_PROJECT_ID` | ID de votre projet GCP | `mon-projet-12345` |
| `GCP_REGION` | Région GCP | `us-central1` |

---

## 🖥️ Exécution en local

### Prérequis
- Python 3.11+
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installé et configuré
- Un projet GCP avec un bucket GCS et Vertex AI activé

### 1. Cloner le repo
```bash
git clone https://github.com/VOTRE_USER/mini-projet-api.git
cd mini-projet-api/api
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Authentification GCP en local
```bash
# Authentification avec votre compte utilisateur
gcloud auth application-default login

# OU via compte de service (fichier JSON)
export GOOGLE_APPLICATION_CREDENTIALS="/chemin/vers/service-account.json"
```

### 5. Définir les variables d'environnement
```bash
export GCS_BUCKET_NAME="mon-bucket-api"
export GCS_FILE_PATH="data/entries.json"
export GCP_PROJECT_ID="mon-projet-12345"
export GCP_REGION="us-central1"
```

### 6. Lancer l'API
```bash
python main.py
```

L'API est disponible sur : `http://localhost:8080`

### 7. Tester les endpoints
```bash
curl http://localhost:8080/hello
curl http://localhost:8080/status
curl http://localhost:8080/data
curl -X POST http://localhost:8080/data \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "message": "Test depuis local"}'
curl http://localhost:8080/poem?theme=le+cloud
```

---

## 🐳 Build Docker

### API
```bash
cd api/

# Build de l'image
docker build -t mini-api .

# Lancer le conteneur en local
docker run -p 8080:8080 \
  -e GCS_BUCKET_NAME="mon-bucket-api" \
  -e GCS_FILE_PATH="data/entries.json" \
  -e GCP_PROJECT_ID="mon-projet-12345" \
  -e GCP_REGION="us-central1" \
  -e GOOGLE_APPLICATION_CREDENTIALS="/app/service-account.json" \
  -v /chemin/local/service-account.json:/app/service-account.json \
  mini-api
```

### Frontend
```bash
cd frontend/

docker build -t mini-frontend .
docker run -p 3000:80 mini-frontend
# Frontend disponible sur http://localhost:3000
```

---

## ☁️ Déploiement sur Google Cloud Run

### Étape 1 — Préparer GCP

```bash
# Définir votre projet
export PROJECT_ID="mon-projet-12345"
gcloud config set project $PROJECT_ID

# Activer les APIs nécessaires
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Étape 2 — Créer un compte de service

```bash
# Créer le compte de service
gcloud iam service-accounts create mini-api-sa \
  --display-name="Mini API Service Account"

# Lui donner les permissions nécessaires
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:mini-api-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:mini-api-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### Étape 3 — Créer le bucket GCS

```bash
gsutil mb -p $PROJECT_ID gs://mon-bucket-api
```

### Étape 4 — Pousser l'image sur Docker Hub

```bash
# Connexion Docker Hub
docker login

# API
cd api/
docker build -t VOTRE_USER_DOCKERHUB/mini-api:latest .
docker push VOTRE_USER_DOCKERHUB/mini-api:latest

# Frontend
cd ../frontend/
docker build -t VOTRE_USER_DOCKERHUB/mini-frontend:latest .
docker push VOTRE_USER_DOCKERHUB/mini-frontend:latest
```

### Étape 5 — Déployer l'API sur Cloud Run

```bash
gcloud run deploy mini-api \
  --image VOTRE_USER_DOCKERHUB/mini-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account mini-api-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars GCS_BUCKET_NAME=mon-bucket-api,GCS_FILE_PATH=data/entries.json,GCP_PROJECT_ID=$PROJECT_ID,GCP_REGION=us-central1
```

Notez l'URL retournée : `https://mini-api-xxxx-uc.a.run.app`

### Étape 6 — Déployer le Frontend sur Cloud Run

```bash
gcloud run deploy mini-frontend \
  --image VOTRE_USER_DOCKERHUB/mini-frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 80
```

---

## 📡 Endpoints de l'API

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/hello` | Message de bienvenue |
| GET | `/status` | Date et heure du serveur |
| GET | `/data` | Lit les entrées depuis GCS |
| POST | `/data` | Ajoute une entrée dans GCS |
| GET | `/poem?theme=xxx` | Génère un poème via Vertex AI |

---

## 👥 Répartition des tâches

| Membre | Contribution |
|---|---|
| **Prénom Nom 1** | Endpoints `/hello`, `/status` · Configuration Docker API |
| **Prénom Nom 2** | Endpoints `/data` (GET + POST) · Intégration GCS |
| **Prénom Nom 3** | Endpoint `/poem` · Intégration Vertex AI |
| **Prénom Nom 4** | Frontend HTML/JS · Docker Frontend · Déploiement Cloud Run |

---

## 🔗 Liens

- **API Cloud Run** : https://mini-api-19533580976.us-central1.run.app
- **Frontend Cloud Run** : `https://mini-frontend-xxxx-uc.a.run.app`
- **Image Docker API** : https://hub.docker.com/r/lucas97592/mini-api
- **Image Docker Frontend** : `https://hub.docker.com/r/VOTRE_USER/mini-frontend`
