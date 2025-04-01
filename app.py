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
        
        cur.execute('SELECT email FROM users WHERE email = %s', (email,))
        existing_user = cur.fetchone()
        if not existing_user:
            favs_json = json.dumps(favs)
            query = "INSERT INTO users (name, email, password, id_fav, type, token) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(query, (name, email, hashlib.sha256(password.encode('utf-8')).hexdigest(), favs_json, type, token))
            cur.execute('SELECT id FROM users WHERE email = %s', (email,))
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
    cur.execute('SELECT email FROM users WHERE email = %s', (email,))
    existing_email = cur.fetchone()
    if existing_email:
        cur.execute('SELECT password FROM users WHERE password = %s', (hashlib.sha256(password.encode('utf-8')).hexdigest(),))
        existing_password = cur.fetchone()
        if existing_password:
            cur.execute('SELECT id FROM users WHERE email = %s', (email,))
            iduser = cur.fetchone()
            cur.execute('UPDATE users SET token = %s WHERE email = %s', (token, email))
            cur.execute('SELECT id_fav FROM users WHERE id = %s', (iduser))
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

    cur.execute('SELECT token FROM users WHERE token = %s', (token,))
    token = cur.fetchone()
    if token:
        imagen = request.files.get('imagen')
        query = "INSERT INTO recipe (title,  description, image, ingredients, quatities, id_user, comments, video) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
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
    cur.execute('SELECT token FROM users WHERE token = %s', (token,))
    token = cur.fetchone()
    cur.execute('SELECT id FROM users WHERE token = %s', (token,))
    iduser = cur.fetchone()
    if token:
        cur.execute('SELECT * FROM recipe WHERE id_user = %s', (iduser,))
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
                'title': recipe[1],
                'description': recipe[2],
                'image': img_url,
                'ingredients':ingredients_list,
                'quatities': quantities_list,
                'id_user': recipe[6],
                'comments': recipe[7],
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
    cur.execute("SELECT * FROM recipe WHERE id = %s", (idrecipe,))
    recipe = cur.fetchone()

    img_url = recipe[3]
    video_url = recipe[8] if recipe[8] else None

    ingredients_list = recipe[4].split(",") 
    quantities_list = recipe[5].split(",") 
    
    recipe_dict = {
        'id': recipe[0],
        'title': recipe[1],
        'description': recipe[2],
        'image': img_url,
        'ingredients': ingredients_list,
        'quatities': quantities_list,
        'id_user': recipe[6],
        'comments': recipe[7],
        'video': video_url,
    }

    return jsonify(message=recipe_dict)

@app.route('/deleteRecipe', methods=["POST"])
def deleteOne():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    tokenUser = data.get("userToken")
    cur = mysql.connection.cursor()

    cur.execute('SELECT token FROM users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("DELETE FROM recipe WHERE id = %s", (idrecipe,))
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
        cur.execute("SELECT comments FROM recipe WHERE id = %s", (recipe_id,))
        comments = cur.fetchone()
        cur.execute("""
            UPDATE recipe 
            SET 
                title = %s, 
                description = %s, 
                ingredients = %s, 
                quatities = %s, 
                comments = %s, 
                video = %s,
                image = %s
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
    cur.execute('SELECT * FROM recipe')
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
            'title': recipe[1],
            'description': recipe[2],
            'image': img_url,
            'ingredients':ingredients_list,
            'quatities': quantities_list,
            'id_user': recipe[6],
            'comments': recipe[7],
            'video': video_url,
        }
        recipe_list.append(recipe_dict)
    cur.execute("SELECT id_recipe,assessment FROM assessment WHERE id_user = %s",(idUser,))
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
    cur.execute('SELECT token FROM users WHERE token = %s', (userToken,))
    token = cur.fetchone()
    if token:
        query = "INSERT INTO comment (comment,  id_recipe, id_user) VALUES (%s, %s, %s)"
        cur.execute(query, (comment,idrecipe,iduser))
        mysql.connection.commit()
        comment_id = cur.lastrowid
        cur.execute('SELECT name FROM users WHERE id = %s', (iduser,))
        user = cur.fetchone()
        query_update = "UPDATE recipe SET comments = JSON_ARRAY_APPEND(comments, '$', %s) WHERE id = %s"
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
    cur.execute('SELECT token FROM users WHERE token = %s', (userToken,))
    token = cur.fetchone()
    
    cur.execute('SELECT * FROM comment WHERE id_recipe = %s', (idrecipe,))
    comments = cur.fetchall()
    comments_with_names = []

    for comment in comments:
        iduser = comment[3]
        cur.execute('SELECT name FROM users WHERE id = %s', (iduser,))
        user = cur.fetchone()
        comment_data = {
            'id_comment': comment[0],
            'comment': comment[1],
            'id_recipe': comment[2],
            'id_user': comment[3],
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
    cur.execute('SELECT token FROM users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("SELECT comments FROM recipe WHERE id = %s", (idrecipe,))
        recipe = cur.fetchone()
        comentarios_json = recipe[0]
        comentarios = json.loads(comentarios_json)

        comentarios = [comentario for comentario in comentarios if comentario != idcomment]
        updated_comentarios_json = json.dumps(comentarios)
        cur.execute("UPDATE recipe SET comments = %s WHERE id = %s", (updated_comentarios_json, idrecipe))
        mysql.connection.commit()
        cur.execute("DELETE FROM comment WHERE id = %s", (idcomment,))
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
    cur.execute('SELECT token FROM users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()

    if tokenUser:
        cur.execute("SELECT * FROM comment WHERE id = %s AND id_user = %s", (idcomment, iduser))
        comment = cur.fetchone()

        if comment:
            cur.execute("UPDATE comment SET comment = %s WHERE id = %s", (new_comment, idcomment))
            mysql.connection.commit()

            cur.execute("SELECT comments FROM recipe WHERE id = %s", (idrecipe,))
            recipe = cur.fetchone()
            comentarios_json = recipe[0]
            comentarios = json.loads(comentarios_json)

            updated_comentarios_json = json.dumps(comentarios)
            cur.execute("UPDATE recipe SET comments = %s WHERE id = %s", (updated_comentarios_json, idrecipe))
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
    cur.execute('SELECT token FROM users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("SELECT id_fav FROM users WHERE id = %s", (iduser,))
        favs = cur.fetchone()
        if favs:
            favs_json = favs[0]
            favs = json.loads(favs_json)
        else:
            favs = []
        if idrecipe not in favs:
            favs.append(idrecipe)
        updated_favs_json = json.dumps(favs)
        cur.execute("UPDATE users SET id_fav = %s WHERE id = %s", (updated_favs_json, iduser))
        mysql.connection.commit()
        
        return jsonify(message="Fav Añadido",idFavs=updated_favs_json)

@app.route('/deleteFavs', methods=['POST'])
def deleteFavs():
    data = request.get_json()
    idrecipe = data.get("idrecipe")
    iduser = data.get("iduser")
    tokenUser = data.get("userToken")
    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("SELECT id_fav FROM users WHERE id = %s", (iduser,))
        favs = cur.fetchone()  
        if favs:
            favs_json = favs[0]
            favs = json.loads(favs_json)
        else:
            favs = []
        favs = [fav for fav in favs if fav != idrecipe]
        updated_favs_json = json.dumps(favs)
        cur.execute("UPDATE users SET id_fav = %s WHERE id = %s", (updated_favs_json, iduser))
        mysql.connection.commit()
        
        return jsonify(message="Fav Eliminado",idFavs=updated_favs_json)

@app.route('/viewFavs', methods=["POST"])
def viewFavs():
    data = request.get_json()
    idFavs = data.get("idFavs")
    
    if not idFavs:
        return jsonify(message="No hay favoritos"), 400
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM recipe WHERE id IN (%s)" % ','.join(['%s'] * len(idFavs)), tuple(idFavs))
    recetas = cur.fetchall()
    recetas_json = []
    
    for receta in recetas:
        img_url = receta[3]
        recetas_json.append({
            'id':receta[0],
            'title': receta[1],  
            'description': receta[2],
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
    cur.execute('SELECT token FROM users WHERE token = %s', (tokenUser,))
    tokenUser = cur.fetchone()
    if tokenUser:
        cur.execute("SELECT * FROM assessment WHERE id_user = %s AND id_recipe = %s", (iduser,idrecipe,))
        exist = cur.fetchone()
        if exist:
            query_update = "UPDATE assessment SET assessment = %s WHERE id_user = %s AND id_recipe = %s"
            cur.execute(query_update, (rating, iduser, idrecipe))  
            mysql.connection.commit()
            cur.close()
            return jsonify(message="Valoracion añadida")
        else:
            query = "INSERT INTO assessment (id_recipe, id_user, assessment) VALUES (%s, %s, %s)"
            cur.execute(query, (idrecipe,iduser,rating)) 
            mysql.connection.commit()
            cur.close()
            return jsonify(message="Valoracion actualizada")

@app.route('/viewProfile', methods=["POST"])
def viewProfiles():
    return jsonify(message="hola")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
RecetasEspanyolas
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

"""
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    id_fav VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    token VARCHAR(459) NOT NULL
);
CREATE TABLE recipe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    image VARCHAR(255) NOT NULL,
    ingredients VARCHAR(255) NOT NULL,
    quatities VARCHAR(255) NOT NULL,
    id_user INT NOT NULL,
    comments VARCHAR(255) DEFAULT NULL,
    video VARCHAR(255) DEFAULT NULL
);
CREATE TABLE comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comment VARCHAR(255) NOT NULL,
    id_recipe INT NOT NULL,
    id_user INT NOT NULL
);

CREATE TABLE assessment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_recipe INT NOT NULL,
    id_user INT NOT NULL,
    assessment INT NOT NULL
);

"""
