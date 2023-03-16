from flask import Flask, jsonify, request, url_for
from flask_mysqldb import MySQL
from config import config
from flask_cors import CORS
import utils
from datetime import datetime
import requests
import json


app = Flask(__name__)
CORS(app)
conexion = MySQL(app)


@app.route("/ingresos")
def get_ingresos():
    try:
        cursor = conexion.connection.cursor()
        fecha_actual = datetime.now().date()
        sql = "SELECT COUNT(FECHA) AS INGRESOS FROM ingresos WHERE DATE(FECHA) = '{0}' AND TIPO_INGRESO = 1".format(
            fecha_actual)
        print(fecha_actual)
        cursor.execute(sql)
        data = cursor.fetchone()
        return jsonify({"ingresos": data[0]})
    except:
        return jsonify({"mensaje": "No se completó la consulta", "Codigo": False})

# @app.route("/registar_ingresos", methods="POST")
# def get_registro_ingresos():
#     try:
#         if request.method == "POST":
#             data = request.get_json()
#             datos = request.post(json=data)
#             datos = json.loads(datos.text)
#             cursor = conexion.conecction.cursor()
#             sql = """INSERT INTO ingresos (ID_USUARIO, ESTADO)
#             VALUES ('{0}')""".format(int(request.json['ID_USUARIO']))
#             print(sql)
#             cursor.execute(sql)
#             conexion.connection.commit()
#         # Aquí puede procesar los datos como lo desee
#         return {'message': 'Datos procesados correctamente.'}, 200
#     except:
#         return jsonify({"message": "Error"}), 400

    # try:
    #     if request.method == "POST":
    #     url = 
    #     data = request.form.to_dict()
    #     datos = requests.post(url, json=data)
    #     datos = json.loads(datos.text)
    #     cursor = conexion.connection.cursor()
    #     sql = """INSERT INTO ingresos (ID_USUARIO, ESTADO)
    #     VALUES ('{0}','{1}')""".format(int(request.json['ID_USUARIO']), int(request.json['ESTADO']))
    #     print(sql)
    #     cursor.execute(sql)
    #     conexion.connection.commit()
    #     return jsonify({"mensaje": "Usuario registrado Correctamente", "Codigo": True})
    # except Exception as ex:
    #     return jsonify({"mensaje": ex, "Codigo": False})


@app.route("/total_estudiantes")
def get_total_estudiantes():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT COUNT(*) AS TOTAL_ESTUDIANTES FROM usuario WHERE ROL = 'estudiante'"
        cursor.execute(sql)
        count1 = cursor.fetchone()[0]
        data1 = []
        data1.append(count1)
        print(data1)
        return jsonify({"total_estudiantes": data1[0]})
    except:
        return jsonify({"mensaje": "No se completó la consulta", "Codigo": False})


@app.route("/inasistencia")
def get_inasistencia():
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT (SELECT COUNT(*) AS TOTAL_ESTUDIANTES FROM usuario WHERE ROL = 'estudiante') - (SELECT COUNT(FECHA) FROM ingresos WHERE DATE(FECHA) = CURDATE() AND TIPO_INGRESO = 1) AS INASISTENCIA"""
        cursor.execute(sql)
        count2 = cursor.fetchone()[0]
        data2 = []
        data2.append(count2)
        print(data2)
        return jsonify({"inasistencias": data2[0]})
    except:
        return jsonify({"mensaje": "No se completó la consulta", "Codigo": False})


@app.route("/promedio")
def get_promedio():
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT DATE_FORMAT(fecha, '%Y-%m') AS mes, AVG(cantidad_ingresos) AS PROMEDIO FROM (SELECT DATE(fecha) AS fecha, COUNT(*) AS cantidad_ingresos FROM ingresos GROUP BY DATE(fecha)) AS ingresos_por_fecha GROUP BY mes"""
        cursor.execute(sql)
        count3 = float(cursor.fetchone()[1])
        data3 = []
        data3.append(count3)
        print(data3)
        return jsonify({"promedio":data3[0]})
    except:
        return jsonify({"mensaje": "No se completó la consulta", "Codigo": False})


@app.route("/estadisticas")
def get_estadisticas():
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT DATE_FORMAT(FECHA, '%Y-%m-%d') AS FECHA, SUM(CANTIDAD_INGRESOS) AS TOTAL_INGRESOS FROM (
        SELECT DATE(FECHA) AS FECHA, COUNT(*) AS CANTIDAD_INGRESOS FROM ingresos GROUP BY DATE(FECHA)) AS INGRESOS_POR_FECHA
        GROUP BY DATE(FECHA)"""
        cursor.execute(sql)
        estadisticas = cursor.fetchall()
        resultados = []
        print(estadisticas)
        for fecha, total_ingresos in estadisticas:
            resultado = {"fecha": fecha, "total_ingresos": total_ingresos}
            resultados.append(resultado)
        return jsonify(resultados)
    except:
        return jsonify({"mensaje": "No se completó la consulta", "Codigo": False})


@app.route("/l_ingresos", methods=['GET'])
def listar_ingresos():
    try:
        # variable de cursor para la bd
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM ingresos ORDER BY ID_INGRESO"
        cursor.execute(sql)
        datos = cursor.fetchall()
        ingresos = []
        for fila in datos:
            ingreso = {"ID_USUARIO": fila[1],
                       "FECHA": fila[2], "ESTADO": fila[3]}
            ingresos.append(ingreso)
        return jsonify(ingresos)
    except Exception as ex:
        return jsonify({"mensaje": ex, "Codigo": False})


@app.route("/estadisticas_grafico")
def get_estadisticas_grafico():
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT DATE_FORMAT(FECHA, '%Y-%m-%d') AS FECHA, SUM(CANTIDAD_INGRESOS) AS TOTAL_INGRESOS FROM (
        SELECT DATE(FECHA) AS FECHA, COUNT(*) AS CANTIDAD_INGRESOS FROM ingresos GROUP BY DATE(FECHA)) AS INGRESOS_POR_FECHA
        GROUP BY DATE(FECHA) DESC LIMIT 5"""
        cursor.execute(sql)
        estadisticas = cursor.fetchall()
        resultados = []
        print(estadisticas)
        for x in estadisticas:
            resultado = {"fecha": x[0], "cantidad": x[1]}
            resultados.append(resultado)
        return jsonify(resultados)
    except:
        return jsonify({"mensaje": "No se completó la consulta", "Codigo": False})


@app.route("/usuarios", methods=['GET'])
def listar_usuarios():
    try:
        # variable de cursor para la bd
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuario ORDER BY id"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        print(datos)
        for fila in datos:
            usuario = {"id": fila[0], "username": fila[1], "password": fila[2], "NOMBRES": fila[3],
                       "APELLIDOS": fila[4], "EDAD": fila[5], "GRADO": fila[6], "ROL": fila[7], "ID_HUELLA": fila[8]}
            usuarios.append(usuario)
        return jsonify(usuarios)
    except Exception as ex:
        return jsonify({"mensaje": ex, "Codigo": False})


@app.route("/un_usuario/", methods=['POST'])
def consultar_Un_Usuario(id):
    try:
        one_User = request.json
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuario WHERE id='{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            usuario = {"id": datos[0], "username": datos[1], "password": datos[2], "NOMBRES": datos[3],
                       "APELLIDOS": datos[4], "EDAD": datos[5], "GRADO": datos[6], "ROL": datos[7], "ID_HUELLA": datos[8]}
            return jsonify({"Usuario": usuario, "mensaje": "Usuario encontrado"})
        else:
            return jsonify({"mensaje": "Usuario no encontrado", "Exito": True})
    except Exception as ex:
        return jsonify({"mensaje": "Error", "Codigo": False})


@app.route("/registrar_Usuario", methods=["POST"])
def Registrar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO usuario (username, password, NOMBRES, APELLIDOS, EDAD, GRADO, ROL)
        VALUES ('{0}','{1}', '{2}', '{3}', '{4}', '{5}', '{6}')""".format(request.json['username'], utils.encryp_Password(request.json['password']), request.json['NOMBRES'], request.json['APELLIDOS'], int(request.json['EDAD']), int(request.json['GRADO']), request.json['ROL'])
        print(sql)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({"mensaje": "Usuario registrado Correctamente", "Codigo": True})
    except Exception as ex:
        return jsonify({"mensaje": ex, "Codigo": False})


@app.route("/login", methods=["POST"])
def login():
    try:
        user = request.json
        cursor = conexion.connection.cursor()
        sql = """SELECT id, username, password FROM
            usuario WHERE username= '{}'""".format(user["username"])
        cursor.execute(sql)
        row = cursor.fetchone()
        password_Bd = utils.return_Password(row[2])
        if password_Bd == user["password"]:
            return jsonify({"mensaje": "ok", "codigo": "True", "id": row[0], "usuario": row[1], "password": password_Bd})
        else:
            return jsonify({"mensaje": "Usuario no existe o datos incorrectos", "codigo": "False"})
    except Exception as ex:
        return jsonify({"mensaje": ex, "codigo": False})


@app.route("/get_by_id", methods=["POST"])
def get_by_id():
    try:
        data = request.json
        print(data)
        id = data["id"]
        print(id)
        cursor = conexion.connection.cursor()
        sql = """SELECT id, username, password, NOMBRES FROM
        usuario WHERE id= '{}'""".format(id)
        cursor.execute(sql)
        row = cursor.fetchone()
        data = row[0], row[1], None, row[3]
        if row != None:
            return jsonify({'id': row[0], 'usuario': row[1], 'password': None, 'nombres': row[3]})
        else:
            return None
    except Exception as ex:
        return jsonify({"mensaje": ex, "codigo": False})


def pagina_no_encontrada(error):
    return "<h1>La Página que intentas buscar no existe...</h1>", 404


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, host='0.0.0.0')
