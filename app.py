from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
app.config.from_object('config.Config')
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
jwt = JWTManager(app)
mysql = MySQL(app)

@app.route('/', methods=['POST'])
def inicio():
    
    return jsonify(error=str(e)), 500


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    type = data.get("type")
    token = create_access_token(identity=email)
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT email FROM Users WHERE email = %s', (email,))
        existing_user = cur.fetchone()
        if not existing_user:
            query = "INSERT INTO Users (nombre, email, password, idFav, type, token) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(query, (name, email, hashlib.sha256(password.encode('utf-8')).hexdigest(), '0', type, token))
            cur.execute('SELECT id FROM Users WHERE email = %s', (email,))
            iduser = cur.fetchone()
            mysql.connection.commit()
            return jsonify(usertoken=token,iduser=iduser)
        else:
            return jsonify(message="El email ya está registrado") 
    except Exception as e:
        return jsonify(message="Error interno en el servidor")
    finally:
        cur.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    

    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM Users WHERE email = %s', (email,))
    token = cur.fetchone()
    cur.execute('SELECT email FROM Users WHERE email = %s', (email,))
    existing_email = cur.fetchone()
    if existing_email:
        cur.execute('SELECT password FROM Users WHERE password = %s', (hashlib.sha256(password.encode('utf-8')).hexdigest(),))
        existing_password = cur.fetchone()
        if existing_password:
            cur.execute('SELECT id FROM Users WHERE email = %s', (email,))
            iduser = cur.fetchone()
            return jsonify(usertoken=token, iduser=iduser)

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    titulo = data.get("titulo")
    imagen = data.get("imagen")
    video = ""
    descripcion=data.get("descripcion")
    ingredientes=data.get("ingredientes")
    cantidades = data.get("cantidades")
    idUser = data.get("idUser")
    comentarios = ""

    cur = mysql.connection.cursor()
    query = "INSERT INTO Receta (titulo,  descripcion, img, ingredientes, cantidades, idUser, comentarios, video, valoraciones) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(query, (titulo,descripcion,imagen,ingredientes,cantidades,idUser,comentarios,video,0))
    mysql.connection.commit()
    cur.close()
    return jsonify(message=imagen)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
