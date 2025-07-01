# Importa las librerías necesarias de Flask y otras utilidades
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# 🔧 Configuración de la base de datos (Render proporciona la variable DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")  # Conexión desde variable de entorno
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el seguimiento innecesario de cambios

# Inicializa SQLAlchemy con la app Flask
db = SQLAlchemy(app)

# 📦 Modelo para la tabla "ubicaciones"
class Ubicacion(db.Model):
    """
    Modelo que representa una ubicación en la base de datos.
    Cada instancia será un registro con los siguientes campos:
    """
    id = db.Column(db.Integer, primary_key=True)  # ID único
    ubicacion = db.Column(db.String(100))         # Nombre o referencia de la ubicación
    aliado = db.Column(db.String(100))            # Nombre del aliado encargado
    carga = db.Column(db.Float)                   # Potencia de carga en watts
    latitud = db.Column(db.Float)                 # Coordenada de latitud
    longitud = db.Column(db.Float)                # Coordenada de longitud

# 🛠️ Crear las tablas automáticamente al iniciar (solo necesario la primera vez)
with app.app_context():
    db.create_all()  # Crea las tablas si no existen

# 📄 Ruta raíz: muestra el formulario HTML
@app.route("/")
def form():
    """
    Renderiza la página del formulario (form.html) para agregar una nueva ubicación.
    """
    return render_template("form.html")  # El archivo HTML debe estar en la carpeta 'templates/'

# 💾 Ruta para guardar la ubicación enviada desde el formulario
@app.route("/guardar", methods=["POST"])
def guardar():
    """
    Recibe los datos del formulario, los convierte en una instancia del modelo Ubicacion,
    y los guarda en la base de datos.
    """
    # Crea una nueva instancia de Ubicacion con los datos del formulario
    data = Ubicacion(
        ubicacion=request.form["Ubicacion"],  # Lee el valor del campo 'Ubicacion'
        aliado=request.form["Aliado"],        # Lee el valor del campo 'Aliado'
        carga=float(request.form["Carga"]),   # Convierte el campo 'Carga' a número
        latitud=float(request.form["Latitud"].replace(",", ".")),   # Reemplaza coma por punto y convierte
        longitud=float(request.form["Longitud"].replace(",", "."))  # Reemplaza coma por punto y convierte
    )

    # Guarda la instancia en la base de datos
    db.session.add(data)
    db.session.commit()

    # Redirige al usuario a la ruta "/mapa" después de guardar
    return redirect("/mapa")

# 🗺️ Ruta que muestra el mapa con todas las ubicaciones registradas
@app.route("/mapa")
def mapa():
    """
    Consulta todos los registros de ubicaciones y los envía al archivo mapa.html para mostrarlos.
    """
    # Consulta todos los registros de la tabla Ubicacion
    ubicaciones_db = Ubicacion.query.all()

    # Convierte los registros en una lista de diccionarios para pasarlos al HTML
    ubicaciones = [{
        "Ubicacion": u.ubicacion,
        "Aliado": u.aliado,
        "Carga": u.carga,
        "Latitud": u.latitud,
        "Longitud": u.longitud
    } for u in ubicaciones_db]

    # Renderiza el mapa y le pasa las ubicaciones
    return render_template("mapa.html", ubicaciones=ubicaciones)

# 🚀 Ejecuta la app si se corre directamente el archivo (no en producción con Gunicorn)
if __name__ == "__main__":
    app.run(debug=True)  # 'debug=True' permite recargar automáticamente y ver errores en desarrollo

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    ubicacion = Ubicacion.query.get_or_404(id)
    db.session.delete(ubicacion)
    db.session.commit()
    return redirect("/mapa")

