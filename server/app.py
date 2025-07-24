from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import os

app = Flask(__name__)
CORS(app)

# Load or train model placeholder
MODEL_PATH = "traffic_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"{MODEL_PATH} not found. Run train_model.py first.")
model = pickle.load(open(MODEL_PATH, "rb"))

@app.route("/")
def home():
    return "✅ SmartFlow API is running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    loc     = len(data.get("location", "")) % 3
    hour    = int(data.get("time", "00:00").split(":")[0])
    weather = 1 if data.get("weather") == "Rainy" else 0

    features = np.array([[loc, hour, weather]])
    pred     = model.predict(features)[0]
    levels   = ["Low", "Moderate", "High"]
    return jsonify({"congestion": levels[pred]})

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    os.makedirs("uploads", exist_ok=True)
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)
    return jsonify({"message": f"'{file.filename}' uploaded successfully."})

@app.route("/current", methods=["GET"])
def current():
    AREAS = [
      "Garki","Wuse","Maitama","Asokoro","Utako",
      "Jabi","Gwarimpa","Kubwa","Lugbe"
    ]
    results = []
    for a in AREAS:
        loc     = len(a) % 3
        hour    = int(request.args.get("time", "00:00").split(":")[0])
        weather = 0
        pred    = model.predict([[loc, hour, weather]])[0]
        levels  = ["Low", "Moderate", "High"]
        results.append({"area": a, "congestion": levels[pred]})
    return jsonify(results)

@app.route("/trends", methods=["GET"])
def trends():
    area = request.args.get("area", "Unknown")
    timestamps = [f"{h:02d}:00" for h in range(6, 19)]
    numeric   = [int(np.random.choice([0, 1, 2])) for _ in timestamps]
    levels_map = ["Low", "Moderate", "High"]
    return jsonify({
        "timestamps": timestamps,
        "levels": [levels_map[n] for n in numeric]
    })

# ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
