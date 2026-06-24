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


@app.route("/animales", methods=["GET"])
def obtener_animales():
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM animales")
    datos = cursor.fetchall()

    animales = []

    for animal in datos:
        animales.append({
            "id": animal[0],
            "nombre": animal[1]
        })

    cursor.close()

    return jsonify(animales)


@app.route("/animales/<int:id>", methods=["GET"])
def obtener_animal(id):
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        "SELECT * FROM animales WHERE id = %s",
        (id,)
    )

    datos = cursor.fetchone()

    cursor.close()

    return jsonify(datos)


@app.route("/animales", methods=["POST"])
def crear_animal():
    datos = request.get_json()

    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO animales(nombre) VALUES(%s) RETURNING id",
        (datos["nombre"],)
    )

    nuevo_id = cursor.fetchone()[0]

    conexion.commit()
    cursor.close()

    return jsonify({
        "id": nuevo_id,
        "nombre": datos["nombre"]
    }), 201


@app.route("/animales/<int:id>", methods=["DELETE"])
def eliminar_animal(id):
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM animales WHERE id = %s",
        (id,)
    )

    conexion.commit()
    cursor.close()

    return jsonify({
        "mensaje": "Animal eliminado correctamente"
    })


if __name__ == "__main__":
    app.run(debug=True)