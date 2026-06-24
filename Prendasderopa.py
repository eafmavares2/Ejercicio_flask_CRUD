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


@app.route("/prendasderopa", methods=["GET"])
def obtener_prendas():
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM prendasderopa")
    datos = cursor.fetchall()

    prendas = []

    for prenda in datos:
        prendas.append({
            "id": prenda[0],
            "nombre": prenda[1]
        })

    cursor.close()

    return jsonify(prendas)


@app.route("/prendasderopa/<int:id>", methods=["GET"])
def obtener_prenda(id):
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        "SELECT * FROM prendasderopa WHERE id = %s",
        (id,)
    )

    datos = cursor.fetchone()

    cursor.close()

    return jsonify(datos)


@app.route("/prendasderopa", methods=["POST"])
def crear_prenda():
    datos = request.get_json()

    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO prendasderopa(nombre) VALUES(%s) RETURNING id",
        (datos["nombre"],)
    )

    nuevo_id = cursor.fetchone()[0]

    conexion.commit()
    cursor.close()

    return jsonify({
        "id": nuevo_id,
        "nombre": datos["nombre"]
    }), 201


@app.route("/prendasderopa/<int:id>", methods=["DELETE"])
def eliminar_prenda(id):
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM prendasderopa WHERE id = %s",
        (id,)
    )

    conexion.commit()
    cursor.close()

    return jsonify({
        "mensaje": "Prenda eliminada correctamente"
    })


if __name__ == "__main__":
    app.run(debug=True)