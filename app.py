from flask import Flask, request, render_template, redirect
import pandas as pd
import os

app = Flask(__name__)
CSV_PATH = "ubicaciones.csv"
ubicaciones = []  # También usaremos memoria para mostrar en el mapa

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

    # Guardar en CSV
    df_nuevo = pd.DataFrame([data])
    archivo_existe = os.path.isfile(CSV_PATH)
    df_nuevo.to_csv(CSV_PATH, mode="a", header=not archivo_existe, index=False, sep=";", encoding="utf-8")

    return redirect("/mapa")

@app.route("/mapa")
def mapa():
    # Leer desde el archivo CSV para asegurar persistencia
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")
        datos = df.to_dict(orient="records")
    else:
        datos = ubicaciones  # en caso de que el archivo no exista aún

    return render_template("mapa.html", ubicaciones=datos)

if __name__ == "__main__":
    app.run(debug=True)
