from flask import Flask, request, render_template, redirect
import csv
import os

app = Flask(__name__)
CSV_PATH = "ubicaciones.csv"
ubicaciones = []  # Para almacenamiento temporal en memoria

@app.route("/")
def formulario():
    return render_template("form.html")

@app.route("/guardar", methods=["POST"])
def guardar():
    data = {
        "Ubicacion": request.form["Ubicacion"],
        "Aliado": request.form["Aliado"],
        "Carga": request.form["Carga"],
        "Latitud": float(request.form["Latitud"].replace(",", ".")),
        "Longitud": float(request.form["Longitud"].replace(",", "."))
    }

    # Guardar en memoria
    ubicaciones.append(data)

    # Guardar en archivo CSV
    archivo_existe = os.path.isfile(CSV_PATH)
    with open(CSV_PATH, mode="a", newline='', encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=data.keys(), delimiter=';')
        if not archivo_existe:
            writer.writeheader()
        writer.writerow(data)

    return redirect("/mapa")

@app.route("/mapa")
def mapa():
    datos = []
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline='', encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo, delimiter=';')
            for fila in reader:
                # Asegurar que Lat y Lon sean flotantes si es necesario para el mapa
                fila["Latitud"] = float(fila["Latitud"])
                fila["Longitud"] = float(fila["Longitud"])
                datos.append(fila)
    else:
        datos = ubicaciones  # si el archivo aún no existe

    return render_template("mapa.html", ubicaciones=datos)

if __name__ == "__main__":
    app.run(debug=True)

