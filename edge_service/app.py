import os
import sys
import json
import shutil
import warnings
import numpy as np
import cv2
from flask import Flask, request, jsonify, send_from_directory, render_template

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from common.audit import log_action

from deepface import DeepFace
import tensorflow as tf

warnings.filterwarnings("ignore", category=FutureWarning)
tf.get_logger().setLevel('ERROR')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['RECOGNIZED_FOLDER'] = "static/recognized"
app.config['REGISTERED_JSON'] = "data/registered.json"
app.config['RECOGNIZED_JSON'] = "data/recognized.json"

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RECOGNIZED_FOLDER'], exist_ok=True)
os.makedirs("data", exist_ok=True)

LOCAL_TOLERANCE = 0.3

try:
    with open(app.config['REGISTERED_JSON'], "r") as f:
        registered_faces = json.load(f)
except Exception:
    registered_faces = []

try:
    with open(app.config['RECOGNIZED_JSON'], "r") as f:
        recognized_faces = json.load(f)
except Exception:
    recognized_faces = []

@app.route("/")
def index():
    return render_template("index.html", registered=registered_faces, recognized=recognized_faces)

@app.route("/register", methods=["POST"])
def register_face():
    name = request.form.get("name")
    file = request.files.get("image")
    if not name or not file:
        return jsonify({"error": "Missing name or image"}), 400

    filename = f"{name}_{file.filename}"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    registered_faces.append({"name": name, "filename": filename})
    with open(app.config['REGISTERED_JSON'], "w") as f:
        json.dump(registered_faces, f)

    log_action("register", user=name, filename=filename)
    return jsonify({"name": name, "filename": filename})

@app.route("/recognize", methods=["POST"])
def recognize_face():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "Missing image"}), 400

    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    try:
        embedding = np.array(DeepFace.represent(img_path=img, model_name="Facenet")[0]["embedding"])
    except Exception as e:
        print("DeepFace error:", e)
        return jsonify({"error": "No face detected"}), 400

    best_match = None
    best_dist = 1.0
    for face in registered_faces:
        try:
            reg_img_path = os.path.join(app.config['UPLOAD_FOLDER'], face["filename"])
            reg_img = cv2.imread(reg_img_path)
            reg_emb = np.array(DeepFace.represent(img_path=reg_img, model_name="Facenet")[0]["embedding"])
            dist = np.linalg.norm(reg_emb - embedding)
            if dist < best_dist:
                best_dist = dist
                best_match = face
        except Exception as e:
            print(f"Skipping {face['filename']} due to error: {e}")

    if best_match and best_dist < LOCAL_TOLERANCE:
        name = best_match["name"]
        recognition_type = "Cloud"
    else:
        name = "Unknown"
        recognition_type = "Cloud"

    rec_filename = f"{name}_{file.filename}"
    save_path = os.path.join(app.config['RECOGNIZED_FOLDER'], rec_filename)
    file.seek(0)
    file.save(save_path)

    recognized_faces.append({
        "name": name,
        "filename": rec_filename,
        "confidence": float(1 - best_dist),
        "recognition_type": recognition_type
    })
    with open(app.config['RECOGNIZED_JSON'], "w") as f:
        json.dump(recognized_faces, f)

    log_action("recognize", user=name, filename=rec_filename,
               recognition_type=recognition_type, confidence=float(1 - best_dist))

    return jsonify({
        "name": name,
        "filename": rec_filename,
        "confidence": float(1 - best_dist),
        "recognition_type": recognition_type
    })

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/recognized/<filename>")
def recognized_file(filename):
    return send_from_directory(app.config['RECOGNIZED_FOLDER'], filename)

@app.route("/registered")
def get_registered():
    return jsonify(registered_faces)

@app.route("/recognized")
def get_recognized():
    return jsonify(recognized_faces)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
