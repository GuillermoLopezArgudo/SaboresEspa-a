from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config.Config')
mysql = MySQL(app)

CORS(app)

@app.route('/', methods=['POST'])
def inicio():
    cur = mysql.connection.cursor()
    print(cur)
    data = request.get_json()
    respuesta = data.get('enviar')
    print(respuesta)
    return jsonify(message="Hola desde Flask!")

if __name__ == '__main__':
    app.run(debug=True)