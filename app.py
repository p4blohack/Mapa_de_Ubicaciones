from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 🔗 Configuración de la base de datos (Render inyecta DATABASE_URL automáticamente)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 📦 Modelo para la tabla "ubicaciones"
class Ubicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ubicacion = db.Column(db.String(100))
    aliado = db.Column(db.String(100))
    carga = db.Column(db.Float)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)

# 🛠️ Crear tablas automáticamente (puedes comentar esto después del primer deploy)
with app.app_context():
    db.create_all()

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/guardar", methods=["POST"])
def guardar():
    # Recoge y transforma los datos del formulario
    data = Ubicacion(
        ubicacion=request.form["Ubicacion"],
        aliado=request.form["Aliado"],
        carga=float(request.form["Carga"]),
        latitud=float(request.form["Latitud"].replace(",", ".")),
        longitud=float(request.form["Longitud"].replace(",", "."))
    )

    # Guarda en la base de datos
    db.session.add(data)
    db.session.commit()

    return redirect("/mapa")

@app.route("/mapa")
def mapa():
    # Consulta todos los datos de la tabla
    ubicaciones_db = Ubicacion.query.all()

    # Los convierte en una lista de diccionarios para enviar al HTML
    ubicaciones = [{
        "Ubicacion": u.ubicacion,
        "Aliado": u.aliado,
        "Carga": u.carga,
        "Latitud": u.latitud,
        "Longitud": u.longitud
    } for u in ubicaciones_db]

    return render_template("mapa.html", ubicaciones=ubicaciones)

if __name__ == "__main__":
    app.run(debug=True)


