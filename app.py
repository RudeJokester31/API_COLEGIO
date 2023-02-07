from flask import Flask, jsonify , request
from flask_mysqldb import MySQL
from config import config
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
conexion = MySQL(app)

@app.route("/usuarios", methods=['GET'])
def listar_usuarios():
    try:
        #variable de cursor para la bd
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM usuario ORDER BY id"
        cursor.execute(sql)
        datos=cursor.fetchall()
        usuarios=[]
        for fila in datos:
            usuario={"id":fila[0], "username":fila[1], "password":fila[2], "NOMBRES":fila[3], "APELLIDOS":fila[4],
            "EDAD":fila[5], "GRADO":fila[6], "ROL":fila[7], "ID_HUELLA":fila[8]}
            usuarios.append(usuario)
        return jsonify({"Usuarios":usuarios, "mensaje": "Usuarios listados", "Exito":True})
    except Exception as ex:
        return jsonify({"mensaje": "Error", "Exito":False})


@app.route("/usuario/<id>", methods = ['GET'])
def Consultar_usuario(id):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM usuario WHERE id='{0}'".format(id)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            usuario={"id":datos[0], "username":datos[1], "password":datos[2], "NOMBRES":datos[3],
            "APELLIDOS":datos[4], "EDAD":datos[5], "GRADO":datos[6], "ROL":datos[7], "ID_HUELLA":datos[8]}
            return jsonify({"Usuario":usuario, "mensaje": "Usuario encontrado"})
        else:
            return jsonify({"mensaje": "Usuario no encontrado","Exito":True})
    except Exception as ex:
        return jsonify({"mensaje": "Error","Exito":False})



@app.route("/usuarios", methods=["POST"])
def Registrar_usuarios():
    try:
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO usuario (id, username, password, NOMBRES, APELLIDOS, EDAD, GRADO, ROL, ID_HUELLA)
        VALUES ('{0}','{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')""".format(request.json['id'], request.json['username']
        , request.json['password'], request.json['NOMBRES'], request.json['APELLIDOS'], request.json['EDAD'], request.json['GRADO'],
        request.json['ROL'], request.json['ID_HUELLA'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({"mensaje": "Usuario registrado", "Exito":True})
    except Exception as ex:
        return jsonify({"mensaje": "Error", "Exito":False})

@app.route("/login", methods=["POST"])
def login():
        try:
            user=request.json
            print(user)
            cursor=conexion.connection.cursor()
            sql="""SELECT id, username, password FROM
            usuario WHERE username= '{}' AND password ='{}'""".format(user["username"],user["password"])
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                return jsonify({"usuario": row})
            else:
                return jsonify({"mensaje": "Usuario no existe"})
        except Exception as ex:
            raise Exception(ex)

def pagina_no_encontrada(error):
    return "<h1>La Página que intentas buscar no existe...</h1>", 404


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True,host='0.0.0.0')
