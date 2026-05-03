import os
import json
import csv
import io
from datetime import datetime
from flask_cors import CORS

from flask import Flask, jsonify, request
from google.cloud import storage
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import vertexai

app = Flask(__name__)
CORS(app)

bucket_name = os.environ.get("GCS_BUCKET_NAME", "mon-bucket-api")
file_path = os.environ.get("GCS_FILE_PATH", "data/entries.json")
project_id = os.environ.get("GCP_PROJECT_ID", "mon-projet-gcp")
region = os.environ.get("GCP_REGION", "europe-west1")


def get_storage_client():
    """Retourne un client Google Cloud Storage authentifié."""
    return storage.Client()


def get_bucket():
    """Retourne le bucket GCS configuré."""
    client = get_storage_client()
    return client.bucket(bucket_name)



@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({
        "message": "Bienvenue sur notre Mini API ! 🎉",
        "version": "1.0.0",
        "endpoints": ["/hello", "/status", "/health", "/data", "/poem"]
    })


@app.route("/status", methods=["GET"])
def status():
    t = datetime.utcnow()
    return jsonify({
        "status": "ok",
        "server_time_utc": t.isoformat(),
        "timestamp": int(t.timestamp())
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "API disponible"
    })

@app.route("/data", methods=["GET"])
def get_data():
    try:
        bucket = get_bucket()
        blob = bucket.blob(file_path)

       
        if not blob.exists():
            return jsonify({"entries": [], "count": 0})

        txt = blob.download_as_text()
        data = json.loads(txt)

        return jsonify({
            "entries": data,
            "count": len(data)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data", methods=["POST"])
def post_data():
    try:

        new_entry = request.get_json()

        if not new_entry:
            return jsonify({"error": "Aucune donnée reçue"}), 400

        if "name" not in new_entry or "message" not in new_entry:
            return jsonify({"error": "Les champs name et message sont obligatoires"}), 400

        new_entry["created_at"] = datetime.utcnow().isoformat()

        bucket = get_bucket()
        blob = bucket.blob(file_path)

        if blob.exists():
            txt = blob.download_as_text()
            data = json.loads(txt)
        else:
            data = []

        data.append(new_entry)

     
        blob.upload_from_string(
            json.dumps(data, indent=2, ensure_ascii=False),
            content_type="application/json"
        )

        return jsonify({
            "message": "Entrée ajoutée avec succès",
            "entry": new_entry,
            "total_entries": len(data)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/poem", methods=["GET"])
def get_poem():
    try:

        langue = request.args.get("langue", "français")
        theme = request.args.get("theme", "la nature")

        prompt = f"Écris un poème court en {langue} sur le thème : {theme}."

        vertexai.init(project=project_id, location=region)
        m = GenerativeModel("gemini-2.5-flash")

        res = m.generate_content(prompt)
        poem_text = res.text

        return jsonify({
            "poem": poem_text,
            "theme": theme,
            "langue": langue,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
