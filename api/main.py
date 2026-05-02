import os
import json
import csv
import io
from datetime import datetime

from flask import Flask, jsonify, request
from google.cloud import storage
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import vertexai

app = Flask(__name__)

BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "mon-bucket-api")
FILE_PATH = os.environ.get("GCS_FILE_PATH", "data/entries.json")
GCP_PROJECT = os.environ.get("GCP_PROJECT_ID", "mon-projet-gcp")
GCP_REGION = os.environ.get("GCP_REGION", "europe-west1")


def get_storage_client():
    """Retourne un client Google Cloud Storage authentifié."""
    return storage.Client()


def get_bucket():
    """Retourne le bucket GCS configuré."""
    client = get_storage_client()
    return client.bucket(BUCKET_NAME)



@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({
        "message": "Bienvenue sur notre Mini API ! 🎉",
        "version": "1.0.0",
        "endpoints": ["/hello", "/status", "/data", "/poem"]
    })


@app.route("/status", methods=["GET"])
def status():
    now = datetime.utcnow()
    return jsonify({
        "status": "ok",
        "server_time_utc": now.isoformat(),
        "timestamp": int(now.timestamp())
    })



@app.route("/data", methods=["GET"])
def get_data():
    try:
        bucket = get_bucket()
        blob = bucket.blob(FILE_PATH)

       
        if not blob.exists():
            return jsonify({"entries": [], "count": 0})

        content = blob.download_as_text()
        entries = json.loads(content)

        return jsonify({
            "entries": entries,
            "count": len(entries)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data", methods=["POST"])
def post_data():
    try:

        new_entry = request.get_json()
        if not new_entry:
            return jsonify({"error": "Corps JSON manquant"}), 400


        new_entry["created_at"] = datetime.utcnow().isoformat()

        bucket = get_bucket()
        blob = bucket.blob(FILE_PATH)

        if blob.exists():
            content = blob.download_as_text()
            entries = json.loads(content)
        else:
            entries = []

        entries.append(new_entry)

     
        blob.upload_from_string(
            json.dumps(entries, indent=2, ensure_ascii=False),
            content_type="application/json"
        )

        return jsonify({
            "message": "Entrée ajoutée avec succès",
            "entry": new_entry,
            "total_entries": len(entries)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/poem", methods=["GET"])
def get_poem():
    try:

        theme = request.args.get("theme", "la nature et le code informatique")

        vertexai.init(project=GCP_PROJECT, location=GCP_REGION)
        model = GenerativeModel("gemini-2.5-flash")

        prompt = f"""Écris un poème court et créatif (4 à 8 vers) sur le thème suivant : {theme}.
        Le poème doit être en français, poétique et inspirant."""

        response = model.generate_content(prompt)
        poem_text = response.text

        return jsonify({
            "poem": poem_text,
            "theme": theme,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
