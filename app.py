from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from flask_mysqldb import MySQL
import hashlib
import json
import base64

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
app.config.from_object('config.Config')
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
jwt = JWTManager(app)
mysql = MySQL(app)

@app.route('/', methods=['POST'])
def inicio():
    return jsonify(message=""), 500


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    type = data.get("type")
    token = create_access_token(identity=email)
    cur = mysql.connection.cursor()
    try:
        
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
            return jsonify(message="El email ya está registrado"), 400
    except Exception as e:
        return jsonify(message="Error interno en el servidor", error=str(e)), 500
    finally:
        cur.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    cur = mysql.connection.cursor()
    token = create_access_token(identity=email)
    cur.execute('SELECT email FROM Users WHERE email = %s', (email,))
    existing_email = cur.fetchone()
    if existing_email:
        cur.execute('SELECT password FROM Users WHERE password = %s', (hashlib.sha256(password.encode('utf-8')).hexdigest(),))
        existing_password = cur.fetchone()
        if existing_password:
            cur.execute('SELECT id FROM Users WHERE email = %s', (email,))
            iduser = cur.fetchone()
            cur.execute('UPDATE Users SET token = %s WHERE email = %s', (token, email))
            mysql.connection.commit()
            return jsonify(usertoken=token, iduser=iduser)

@app.route('/create', methods=['POST'])
def create():

    titulo = request.form.get("titulo")
    descripcion = request.form.get("descripcion")
    imagen = request.files.get('imagen')
    img_bin = imagen.read()
    video = request.files.get('video')
    if video:
        video_bin = video.read()
    else:
        video_bin = None
    ingredientes_json = request.form.get("ingredientes") 
    cantidades_json = request.form.get("cantidades")
    idUser = request.form.get("idUser")
    comentarios = ""
    token = request.form.get("userToken")

    cur = mysql.connection.cursor()

    cur.execute('SELECT token FROM Users WHERE token = %s', (token,))
    token = cur.fetchone()
    
    if token:
        imagen = request.files.get('imagen')
        query = "INSERT INTO Receta (titulo,  descripcion, img, ingredientes, cantidades, idUser, comentarios, video, valoraciones) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (titulo,descripcion,img_bin,ingredientes_json,cantidades_json,idUser,comentarios,video_bin,0))
        mysql.connection.commit()
        cur.close()
        return jsonify(message="Receta registrada",isLoggin=True)
    return jsonify(menssage="Error no registrado",isLoggin=False)
    
@app.route('/viewRecipes' , methods=["POST"])
def viewAll():
    data = request.get_json()
    token = data.get("userToken")
    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM Users WHERE token = %s', (token,))
    token = cur.fetchone()
    cur.execute('SELECT id FROM Users WHERE token = %s', (token,))
    iduser = cur.fetchone()
    if token:
        cur.execute('SELECT * FROM Receta WHERE iduser = %s', (iduser,))
        recipes = cur.fetchall()
        recipe_list = []
        for recipe in recipes:
            ingredients = recipe[4]
            quantities = recipe[5]
            ingredients_list = ingredients.split(",")
            quantities_list = quantities.split(",")
            img_base64 = base64.b64encode(recipe[3]).decode('utf-8')
            if recipe[8]:
                video_base64 = base64.b64encode(recipe[8]).decode('utf-8')
            else:
                video_base64 = None
            recipe_dict = {
                'id': recipe[0],
                'titulo': recipe[1],
                'descripcion': recipe[2],
                'img': img_base64,
                'ingredientes':ingredients_list,
                'cantidades': quantities_list,
                'idUser': recipe[6],
                'comentarios': recipe[7],
                'video': video_base64,
                'valoraciones': recipe[9]
            }
            recipe_list.append(recipe_dict)
        cur.close()
        return jsonify(message=recipe_list)

@app.route('/viewRecipe', methods=["POST"])
def viewOne():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    tokenUser = data.get("userToken")
    cur = mysql.connection.cursor()

    cur.execute('SELECT token FROM Users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("SELECT * FROM Receta WHERE id = %s", (idrecipe,))
        recipe = cur.fetchone()

        img_base64 = base64.b64encode(recipe[3]).decode('utf-8')
        if recipe[8]:
            video_base64 = base64.b64encode(recipe[8]).decode('utf-8')
        else:
            video_base64 = None

        ingredients_list = recipe[4].split(",") 
        quantities_list = recipe[5].split(",") 

        recipe_dict = {
            'id': recipe[0],
            'titulo': recipe[1],
            'descripcion': recipe[2],
            'img': img_base64,
            'ingredientes': ingredients_list,
            'cantidades': quantities_list,
            'idUser': recipe[6],
            'comentarios': recipe[7],
            'video': video_base64,
            'valoraciones': recipe[9]
        }

        return jsonify(message=recipe_dict)

@app.route('/deleteRecipe', methods=["POST"])
def deleteOne():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    tokenUser = data.get("userToken")
    cur = mysql.connection.cursor()

    cur.execute('SELECT token FROM Users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("DELETE * FROM Receta WHERE id = %s", (idrecipe,))
        return jsonify(message="Receta Eliminada")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
