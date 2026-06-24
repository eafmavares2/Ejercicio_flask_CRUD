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


@app.route("/estudiantes", methods=["GET"])
def obtener_estudiantes():
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM estudiantes")
    datos = cursor.fetchall()

    estudiantes = []

    for estudiante in datos:
        estudiantes.append({
            "id": estudiante[0],
            "nombre": estudiante[1]
        })

    cursor.close()

    return jsonify(estudiantes)


@app.route("/estudiantes/<int:id>", methods=["GET"])
def obtener_estudiante(id):
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        "SELECT * FROM estudiantes WHERE id = %s",
        (id,)
    )

    datos = cursor.fetchone()

    cursor.close()

    return jsonify(datos)


@app.route("/estudiantes", methods=["POST"])
def crear_estudiante():
    datos = request.get_json()

    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO estudiantes(nombre) VALUES(%s) RETURNING id",
        (datos["nombre"],)
    )

    nuevo_id = cursor.fetchone()[0]

    conexion.commit()
    cursor.close()

    return jsonify({
        "id": nuevo_id,
        "nombre": datos["nombre"]
    }), 201


@app.route("/estudiantes/<int:id>", methods=["DELETE"])
def eliminar_estudiante(id):
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM estudiantes WHERE id = %s",
        (id,)
    )

    conexion.commit()
    cursor.close()

    return jsonify({
        "mensaje": "Estudiante eliminado correctamente"
    })


if __name__ == "__main__":
    app.run(debug=True)