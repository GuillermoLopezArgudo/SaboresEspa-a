from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def inicio():
    data = request.get_json()
    respuesta = data.get('enviar')
    print(respuesta)
    return jsonify(message="Hola desde Flask!")

if __name__ == '__main__':
    app.run(debug=True)