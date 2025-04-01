from flask import Flask, render_template, redirect
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("agg")
URLs = [
    "https://api.thingspeak.com/channels/12397/feeds.csv",
    "https://api.thingspeak.com/channels/306267/feeds.csv",
]

app = Flask(__name__)


def descargar(url):
    # Leer el CSV desde la URL
    df = pd.read_csv(url)
    # Parsear la fecha y hora
    df["created_at"] = pd.to_datetime(df["created_at"])
    # borrar columnas innecesarias
    if "field6" in df.columns:
        df.drop(
            ["entry_id", "field5", "field6", "field7", "field8"], axis=1, inplace=True
        )
    else:
        df.drop(["entry_id"], axis=1, inplace=True)
    # Renombrar columnas
    df.columns = [
        "Fecha",
        "Temperatura Exterior (°C)",
        "Temperatura Interior (°C)",
        "Presion Atmosferica",
        "Humedad Exterior (%)",
    ]
    return df


def graficar(i, df):
    # Graficar los datos
    lista = []
    for column in df.columns[1:]:
        plt.figure(figsize=(8, 5))
        plt.plot(df["Fecha"], df[column], label=column)
        plt.title(f"Historico de {column} de la estación {i+1}")
        # grabar la imagen
        plt.savefig(f"static/{column}.png")
        lista.append(f"{column}.png")
        plt.close()
    return lista


@app.route("/")
def index():
    for i, url in enumerate(URLs):
        nombres = []
        df = descargar(url)
        nombres.extend(graficar(i, df))
        
    # Descargar los datos de las estaciones meteorológicas
    # Renderizar la plantilla index.html
    return render_template("index.html", nombres=nombres)


# Programa Principal
if __name__ == "__main__":
    # Ejecuta la app
    app.run(host="0.0.0.0", debug=True)
