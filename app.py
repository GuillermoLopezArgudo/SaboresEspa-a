from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_mysqldb import MySQL
import hashlib
import json
import base64
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER_IMAGES'] = 'static/images'
app.config['UPLOAD_FOLDER_VIDEOS'] = 'static/videos'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
    favs = data.get("favs",[])
    token = create_access_token(identity=email)
    cur = mysql.connection.cursor()
    try:
        
        cur.execute('SELECT email FROM Users WHERE email = %s', (email,))
        existing_user = cur.fetchone()
        if not existing_user:
            favs_json = json.dumps(favs)
            query = "INSERT INTO Users (nombre, email, password, idFav, type, token) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(query, (name, email, hashlib.sha256(password.encode('utf-8')).hexdigest(), favs_json, type, token))
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
            cur.execute('SELECT idFav FROM Users Where id = %s', (iduser))
            idFavs = cur.fetchone()
            mysql.connection.commit()
            return jsonify(usertoken=token, iduser=iduser, idFavs=idFavs)

@app.route('/create', methods=['POST'])
def create():

    titulo = request.form.get("titulo")
    descripcion = request.form.get("descripcion")
    imagen = request.files.get('imagen')
    img_url = None
    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        img_url = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], filename)
        imagen.save(img_url)
    video = request.files.get('video')
    video_url = None
    if video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        video_url = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], filename)
        video.save(video_url)
    ingredientes_json = request.form.get("ingredientes") 
    cantidades_json = request.form.get("cantidades")
    idUser = request.form.get("idUser")
    comentarios = request.form.get("opcion")
    token = request.form.get("userToken")

    cur = mysql.connection.cursor()

    cur.execute('SELECT token FROM Users WHERE token = %s', (token,))
    token = cur.fetchone()
    if token:
        imagen = request.files.get('imagen')
        query = "INSERT INTO Receta (titulo,  descripcion, img, ingredientes, cantidades, idUser, comentarios, video) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        cur.execute(query, (titulo,descripcion,img_url,ingredientes_json,cantidades_json,idUser,comentarios,video_url))
        mysql.connection.commit()
        cur.close()
        return jsonify(message="Receta registrada")
    return jsonify(menssage="Error no registrado")
    
@app.route('/viewRecipes' , methods=["POST"])
def viewAllHome():
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
            img_url = recipe[3]
            video_url = recipe[8] if recipe[8] else None

            recipe_dict = {
                'id': recipe[0],
                'titulo': recipe[1],
                'descripcion': recipe[2],
                'img': img_url,
                'ingredientes':ingredients_list,
                'cantidades': quantities_list,
                'idUser': recipe[6],
                'comentarios': recipe[7],
                'video': video_url,
            }
            recipe_list.append(recipe_dict)
        cur.close()
        return jsonify(message=recipe_list)

@app.route('/viewRecipe', methods=["POST"])
def viewOneHome():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Receta WHERE id = %s", (idrecipe,))
    recipe = cur.fetchone()

    img_url = recipe[3]
    video_url = recipe[8] if recipe[8] else None

    ingredients_list = recipe[4].split(",") 
    quantities_list = recipe[5].split(",") 
    
    recipe_dict = {
        'id': recipe[0],
        'titulo': recipe[1],
        'descripcion': recipe[2],
        'img': img_url,
        'ingredientes': ingredients_list,
        'cantidades': quantities_list,
        'idUser': recipe[6],
        'comentarios': recipe[7],
        'video': video_url,
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
        cur.execute("DELETE FROM Receta WHERE id = %s", (idrecipe,))
        mysql.connection.commit()
        return jsonify(message="Receta Eliminada")
    
@app.route("/editeRecipe", methods=["POST"])
def editeOne():

    data = request.form
    recipe_id = data.get('idrecipe')
    title = data.get('titulo')
    description = data.get('descripcion')
    ingredients = json.loads(data.get('ingredientes'))
    quantities = json.loads(data.get('cantidades'))
    user_token = data.get('userToken') 


    imagen = request.files.get('imagen')
    img_url = None
    if imagen != None:
        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            img_url = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], filename)
            imagen.save(img_url)
    else:
        img_url = data.get('imagen')
    video = request.files.get('video')
    video_url = None
    if video != None:
        if video and allowed_file(video.filename):
            filename = secure_filename(video.filename)
            video_url = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], filename)
            video.save(video_url)
    else:
        video_url = data.get('video')
    
    ingredients_json = json.dumps(ingredients)
    quantities_json = json.dumps(quantities)

    if user_token:
        cur = mysql.connection.cursor()
        cur.execute("SELECT comentarios FROM Receta WHERE id = %s", (recipe_id,))
        comments = cur.fetchone()
        cur.execute("""
            UPDATE Receta 
            SET 
                titulo = %s, 
                descripcion = %s, 
                ingredientes = %s, 
                cantidades = %s, 
                comentarios = %s, 
                video = %s,
                img = %s
            WHERE id = %s;
        """, (title, description, ingredients_json, quantities_json, comments, video_url, img_url, recipe_id))

        mysql.connection.commit()
        cur.close()

        return jsonify(message="Receta actualizada correctamente")

@app.route("/viewAll", methods=["POST"])
def viewAllIndex():
    data = request.get_json()
    idUser = data.get("iduser")
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Receta')
    recipes = cur.fetchall()
    recipe_list = []
    for recipe in recipes:
        ingredients = recipe[4]
        quantities = recipe[5]
        ingredients_list = ingredients.split(",")
        quantities_list = quantities.split(",")
        img_url = recipe[3]
        video_url = recipe[8] if recipe[8] else None
        recipe_dict = {
            'id': recipe[0],
            'titulo': recipe[1],
            'descripcion': recipe[2],
            'img': img_url,
            'ingredientes':ingredients_list,
            'cantidades': quantities_list,
            'idUser': recipe[6],
            'comentarios': recipe[7],
            'video': video_url,
        }
        recipe_list.append(recipe_dict)
    cur.execute("SELECT idrecipe,valoracion FROM Valoracion WHERE iduser = %s",(idUser,))
    stars = cur.fetchall()
    cur.close()
    return jsonify(message=recipe_list,stars=stars)

@app.route("/createComment", methods=["POST"])
def createComment():
    data = request.get_json()
    comment = data.get("comment")
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    userToken = data.get("userToken")
    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM Users WHERE token = %s', (userToken,))
    token = cur.fetchone()
    if token:
        query = "INSERT INTO Comentarios (texto,  idreceta, iduser) VALUES (%s, %s, %s)"
        cur.execute(query, (comment,idrecipe,iduser))
        mysql.connection.commit()
        comment_id = cur.lastrowid
        cur.execute('SELECT nombre FROM Users WHERE id = %s', (iduser,))
        user = cur.fetchone()
        query_update = "UPDATE Receta SET comentarios = JSON_ARRAY_APPEND(comentarios, '$', %s) WHERE id = %s"
        cur.execute(query_update, (comment_id, idrecipe))  
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Comentario Subido","idcomment": comment_id,"username": user[0] })

@app.route("/viewComment", methods=["POST"])
def viewComments():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    userToken = data.get("userToken")
    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM Users WHERE token = %s', (userToken,))
    token = cur.fetchone()
    
    cur.execute('SELECT * FROM Comentarios WHERE idreceta = %s', (idrecipe,))
    comments = cur.fetchall()
    comments_with_names = []

    for comment in comments:
        iduser = comment[3]
        cur.execute('SELECT nombre FROM Users WHERE id = %s', (iduser,))
        user = cur.fetchone()
        comment_data = {
            'idcomment': comment[0],
            'comment': comment[1],
            'idrecipe': comment[2],
            'iduser': comment[3],
            'username': user[0]
        }

        comments_with_names.append(comment_data)

    return jsonify(message=comments_with_names)

@app.route("/deleteComment", methods=["POST"])
def deleteComments():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    tokenUser = data.get("userToken")
    idcomment=data.get("idcomment")
    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM Users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("SELECT comentarios FROM Receta WHERE id = %s", (idrecipe,))
        recipe = cur.fetchone()
        comentarios_json = recipe[0]
        comentarios = json.loads(comentarios_json)

        comentarios = [comentario for comentario in comentarios if comentario != idcomment]
        updated_comentarios_json = json.dumps(comentarios)
        cur.execute("UPDATE Receta SET comentarios = %s WHERE id = %s", (updated_comentarios_json, idrecipe))
        mysql.connection.commit()
        cur.execute("DELETE FROM Comentarios WHERE id = %s", (idcomment,))
        mysql.connection.commit()
        return jsonify(message="Comentario Eliminado")

@app.route("/editeComment", methods=["POST"])
def editeComment():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    tokenUser = data.get("userToken")
    idcomment = data.get("idcomment")
    iduser = data.get("iduser")
    new_comment = data.get("comment")

    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM Users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()

    if tokenUser:
        cur.execute("SELECT * FROM Comentarios WHERE id = %s AND iduser = %s", (idcomment, iduser))
        comment = cur.fetchone()

        if comment:
            cur.execute("UPDATE Comentarios SET texto = %s WHERE id = %s", (new_comment, idcomment))
            mysql.connection.commit()

            cur.execute("SELECT comentarios FROM Receta WHERE id = %s", (idrecipe,))
            recipe = cur.fetchone()
            comentarios_json = recipe[0]
            comentarios = json.loads(comentarios_json)

            updated_comentarios_json = json.dumps(comentarios)
            cur.execute("UPDATE Receta SET comentarios = %s WHERE id = %s", (updated_comentarios_json, idrecipe))
            mysql.connection.commit()

            return jsonify(message="Comentario actualizado exitosamente")

    return jsonify(message="No autorizado o comentario no encontrado"), 403

@app.route("/updateFavs", methods=['POST'])
def updateFavs():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    tokenUser = data.get("userToken")
    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM Users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("SELECT idFav FROM Users WHERE id = %s", (iduser,))
        favs = cur.fetchone()
        if favs:
            favs_json = favs[0]
            favs = json.loads(favs_json)
        else:
            favs = []
        if idrecipe not in favs:
            favs.append(idrecipe)
        updated_favs_json = json.dumps(favs)
        cur.execute("UPDATE Users SET idFav = %s WHERE id = %s", (updated_favs_json, iduser))
        mysql.connection.commit()
        
        return jsonify(message="Fav Añadido",idFavs=updated_favs_json)

@app.route('/deleteFavs', methods=['POST'])
def deleteFavs():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    tokenUser = data.get("userToken")
    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM Users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("SELECT idFav FROM Users WHERE id = %s", (iduser,))
        favs = cur.fetchone()  
        if favs:
            favs_json = favs[0]
            favs = json.loads(favs_json)
        else:
            favs = []
        favs = [fav for fav in favs if fav != idrecipe]
        updated_favs_json = json.dumps(favs)
        cur.execute("UPDATE Users SET idFav = %s WHERE id = %s", (updated_favs_json, iduser))
        mysql.connection.commit()
        
        return jsonify(message="Fav Eliminado",idFavs=updated_favs_json)

@app.route('/viewFavs', methods=["POST"])
def viewFavs():
    data = request.get_json()
    idFavs = data.get("idFavs")
    
    if not idFavs:
        return jsonify(message="No hay favoritos"), 400
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Receta WHERE id IN (%s)" % ','.join(['%s'] * len(idFavs)), tuple(idFavs))
    recetas = cur.fetchall()
    recetas_json = []
    
    for receta in recetas:
        img_url = receta[3]
        recetas_json.append({
            'id':receta[0],
            'titulo': receta[1],  
            'descripcion': receta[2],
            'imagen': img_url
        })
    return jsonify(message=recetas_json)

@app.route('/updateRating', methods=["POST"])
def updateReting():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    rating = data.get("rating")
    iduser = data.get("iduser")
    tokenUser = data.get("userToken")
    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM Users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("SELECT * FROM Valoracion WHERE iduser = %s AND idrecipe = %s", (iduser,idrecipe,))
        exist = cur.fetchone()
        if exist:
            query_update = "UPDATE Valoracion SET valoracion = %s WHERE iduser = %s AND idrecipe = %s"
            cur.execute(query_update, (rating, iduser, idrecipe))  
            mysql.connection.commit()
            cur.close()
            return jsonify(message="Valoracion añadida")
        else:
            query = "INSERT INTO Valoracion (idrecipe, iduser, valoracion) VALUES (%s, %s, %s)"
            cur.execute(query, (idrecipe,iduser,rating)) 
            mysql.connection.commit()
            cur.close()
            return jsonify(message="Valoracion actualizada")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    idFav VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    token VARCHAR(459) NOT NULL
);
CREATE TABLE Receta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    img VARCHAR(255) NOT NULL,
    ingredientes VARCHAR(255) NOT NULL,
    cantidades VARCHAR(255) NOT NULL,
    iduser INT NOT NULL,
    comentarios VARCHAR(255) DEFAULT NULL,
    video VARCHAR(255) DEFAULT NULL
);
CREATE TABLE Comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    texto VARCHAR(255) NOT NULL,
    idreceta INT NOT NULL,
    iduser INT NOT NULL
);

CREATE TABLE Valoracion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idrecipe INT NOT NULL,
    iduser INT NOT NULL,
    valoracion INT NOT NULL
);

"""
