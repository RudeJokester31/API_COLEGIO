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
        cursor.execute(sql)
        data = cursor.fetchone()
        cursor.close()
        return jsonify({"ingresos": data[0]})
    except Exception as e:
        return jsonify({"mensaje": "No se completó la consulta", "Codigo": e})


@app.route('/ingresos_unUsuario', methods=['POST'])
def ingresos_unUsuario():
    try:
        cursor = conexion.connection.cursor()
        usuario = request.json
        sql = "SELECT U.id, U.nombres, U.apellidos, U.rol, I.fecha, T.total_registros FROM usuario U INNER JOIN ingresos I ON U.id = I.id_usuario INNER JOIN (SELECT id_usuario, COUNT(*) AS total_registros FROM ingresos GROUP BY id_usuario) T ON U.id = T.id_usuario WHERE U.id = '{0}';".format(
            usuario["id_usuario"])
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        if not data:
            return jsonify({"mensaje": "No se encontraron resultados para el ID de usuario proporcionado", "Codigo": "False"})
        json_dict = {}
        for i in range(len(data)):
            json_dict[i] = {'id': data[i][0], 'nombre': data[i][1],
                            'apellido': data[i][2], 'tipo': data[i][3], 'fecha': str(data[i][4])}
            json_str = json.dumps(json_dict)
        return jsonify((json.loads(json_str)))

    except Exception as e:
        return jsonify({"mensaje": "error al insertar el ingreso", "Codigo": e})


@app.route('/Inasistencia_Detallada', methods=['POST'])
def Inasistencia_Detallada():
    try:
        cursor = conexion.connection.cursor()
        fecha = request.json
        sql = "SET @fecha = '{0}';".format(fecha["fecha"])
        cursor.execute(sql)
        sql = "SELECT usuario.ID, usuario.NOMBRES, usuario.APELLIDOS FROM usuario LEFT JOIN ingresos ON usuario.ID = ingresos.ID_USUARIO AND DATE(ingresos.FECHA) = @fecha WHERE ingresos.ID_INGRESO IS NULL ORDER BY usuario.ID;"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        json_dict = {}
        for i in range(len(data)):
            json_dict[i] = {'id': data[i][0], 'nombre': data[i][1],
                            'apellido': data[i][2]}
            json_str = json.dumps(json_dict)
        return jsonify((json.loads(json_str)))
    except Exception as e:
        return jsonify({"mensaje": "No se completó la consulta", "Codigo": e})


@app.route("/insert_Ingreso", methods=["POST"])
def insert_Ingreso():
    try:
        cursor = conexion.connection.cursor()
        ingreso = request.json
        sql = "INSERT INTO ingresos (ID_USUARIO, TIPO_INGRESO) VALUES ('{0}', '{1}')".format(
            ingreso["ID_USUARIO"], ingreso["TIPO_INGRESO"])
        cursor.execute(sql)
        conexion.connection.commit()
        cursor.close()
        return jsonify({"mensaje": "ingreso insertado correctamente"})
    except Exception as ex:
        return jsonify({"mensaje": "error al insertar el ingreso"})


@app.route("/total_estudiantes")
def get_total_estudiantes():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT COUNT(*) AS TOTAL_ESTUDIANTES FROM usuario WHERE ROL = 'estudiante'"
        cursor.execute(sql)
        count1 = cursor.fetchone()[0]
        data1 = []
        data1.append(count1)
        cursor.close()
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
        cursor.close()
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
        cursor.close()
        return jsonify({"promedio": data3[0]})
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
        cursor.close()
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
        cursor.close()
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
        cursor.close()
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
        cursor.close()
        for fila in datos:
            usuario = {"id": fila[0], "username": fila[1], "password": fila[2], "NOMBRES": fila[3],
                       "APELLIDOS": fila[4], "EDAD": fila[5], "GRADO": fila[6], "ROL": fila[7], "ID_HUELLA": fila[8]}
            usuarios.append(usuario)
        return jsonify(usuarios)
    except Exception as ex:
        return jsonify({"mensaje": ex, "Codigo": False})


@app.route("/registrar_Usuario", methods=["POST"])
def Registrar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO usuario (username, password, NOMBRES, APELLIDOS, EDAD, GRADO, ROL)
        VALUES ('{0}','{1}', '{2}', '{3}', '{4}', '{5}', '{6}')""".format(request.json['username'], utils.encryp_Password(request.json['password']), request.json['NOMBRES'], request.json['APELLIDOS'], int(request.json['EDAD']), int(request.json['GRADO']), request.json['ROL'])
        cursor.execute(sql)
        conexion.connection.commit()
        cursor.close()
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
        cursor.close()
        if row is None:
            return jsonify({"mensaje": "Usuario no existe o datos incorrectos", "codigo": "False"})
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
        id = data["id"]
        cursor = conexion.connection.cursor()
        sql = """SELECT id, username, password, NOMBRES FROM
        usuario WHERE id= '{}'""".format(id)
        cursor.execute(sql)
        row = cursor.fetchone()
        data = row[0], row[1], None, row[3]
        cursor.close()
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
