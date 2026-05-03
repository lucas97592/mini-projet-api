#  Mini Projet API — Flask + GCP + Docker


Projet réalisé en groupe dans le cadre du cours, avec pour objectif de mettre en pratique la création d’une API simple en Python, l’utilisation de Docker, et le déploiement sur Google Cloud.

L’API permet de manipuler des données stockées sur Google Cloud Storage et d’expérimenter la génération de texte avec Vertex AI.

---

##  Objectif

Le but du projet est de comprendre comment :

- créer une API avec Flask  
- stocker des données sur GCS  
- utiliser un service cloud (Vertex AI)  
- dockeriser une application  
- déployer sur Cloud Run  

Le projet reste volontairement simple pour se concentrer sur ces aspects.

---

## ⚙️ Fonctionnalités

- `GET /hello` → message de bienvenue  
- `GET /status` → heure du serveur  
- `GET /data` → lecture des données depuis GCS  
- `POST /data` → ajout d’une entrée  
- `GET /poem` → génération d’un poème (si Vertex AI activé)  

---

##  Structure du projet

```
mini_projet/
├── api/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   └── Dockerfile
└── README.md
```

---

##  Lancer en local

### 1. Se placer dans l’API

```
cd api
```

### 2. Installer les dépendances

```
pip install -r requirements.txt
```

### 3. Lancer l’API

```
python main.py
```

Accessible sur :

```
http://localhost:8080
```

---

##  Frontend

Un petit frontend HTML permet de tester les endpoints.

```
cd frontend
python -m http.server 3000
```

Puis ouvrir :

```
http://localhost:3000
```

---

## ☁️ Utilisation de GCP

Le projet utilise :

- **Google Cloud Storage** pour stocker les données  
- **Vertex AI** pour générer du texte  

 Remarque :  
La génération de poème peut ne pas fonctionner si la facturation GCP n’est pas activée.

---

## 🐳 Docker

Build de l’API :

```
cd api
docker build -t mini-api .
```

Lancement :

```
docker run -p 8080:8080 mini-api
```

---

## ⚠️ Limites

- pas de gestion avancée des erreurs  
- pas de système d’authentification  
- stockage simple dans un fichier JSON  
- dépendance à GCP pour certaines fonctionnalités  

---
