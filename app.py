#on importe les outils Flask dont on a besoin.
from flask import Flask, render_template, request, jsonify

#JSON c'est un format de fichier pour stocker des données.
# os bibliotheque python permet d'interagir avec mon ordinateur
import json     
import os

#On crée l'application Flask qu'on met dans une variable app
app = Flask(__name__)

#variable qui contient le nom du fichier où on va stocker les courses
DATA_FILE = "courses.json"

def charger_courses():
    if os.path.exists(DATA_FILE): #est-ce que le fichier courses.json existe sur le disque ?
        with open(DATA_FILE, "r") as f: #ouvre le fichier en lecture "r"
            return json.load(f) #lit le contenu JSON du fichier et le transforme en liste Python. Tes courses deviennent une liste de dictionnaires Python utilisables dans le code.
    return [] # si le fichier n'existe pas, on retourne une liste vide

def sauvegarder_courses(courses):
    with open(DATA_FILE, "w") as f: #mode écriture écrase le contenu existant et réécrit tout.
        json.dump(courses, f, indent=2) #transforme la liste Python en texte JSON et l'écrit dans le fichier

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/courses", methods=["GET"])
def get_courses():
    return jsonify(charger_courses())

@app.route("/api/courses", methods=["POST"])
def add_course():
    data = request.json
    courses = charger_courses()
    courses.append({
        "date": data["date"],
        "distance": float(data["distance"]),
        "duration": float(data["duration"])
    })
    sauvegarder_courses(courses)
    return jsonify({"success": True, "total": len(courses)})

if __name__ == "__main__":
    print("Serveur démarré sur http://localhost:5000")
    app.run(debug=True)
