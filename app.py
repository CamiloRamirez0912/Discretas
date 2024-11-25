from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Ruta para cargar los datos de los hospitales
@app.route("/api/hospitals", methods=["GET"])
def get_hospitals():
    with open("data/hospitals.json", encoding="utf-8") as f:
        hospitals = json.load(f)
    return jsonify(hospitals)

# Ruta principal para renderizar el mapa
@app.route("/")
def index():
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)
