from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

conexion = psycopg2.connect(
    host="localhost",
    database="crud",
    user="postgres",
    password="12345",
    port=5432
)

print("Conexión exitosa")


@app.route("/comida", methods=["GET"])
def obtener_comidas():
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM comida")
    datos = cursor.fetchall()

    comidas = []

    for comida in datos:
        comidas.append({
            "id": comida[0],
            "nombre": comida[1]
        })

    cursor.close()

    return jsonify(comidas)


@app.route("/comida/<int:id>", methods=["GET"])
def obtener_comida(id):
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        "SELECT * FROM comida WHERE id = %s",
        (id,)
    )

    datos = cursor.fetchone()

    cursor.close()

    return jsonify(datos)


@app.route("/comida", methods=["POST"])
def crear_comida():
    datos = request.get_json()

    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO comida(nombre) VALUES(%s) RETURNING id",
        (datos["nombre"],)
    )

    nuevo_id = cursor.fetchone()[0]

    conexion.commit()
    cursor.close()

    return jsonify({
        "id": nuevo_id,
        "nombre": datos["nombre"]
    }), 201


@app.route("/comida/<int:id>", methods=["DELETE"])
def eliminar_comida(id):
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM comida WHERE id = %s",
        (id,)
    )

    conexion.commit()
    cursor.close()

    return jsonify({
        "mensaje": "Comida eliminada correctamente"
    })


if __name__ == "__main__":
    app.run(debug=True)