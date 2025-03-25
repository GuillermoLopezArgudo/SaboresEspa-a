from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
app.config.from_object('config.Config')


mysql = MySQL(app)

@app.route('/', methods=['POST'])
def inicio():
    
    try:
        # Intentamos hacer una consulta simple para verificar la conexión
        cur = mysql.connection.cursor()
        cur.execute("SELECT DATABASE();")
        current_db = cur.fetchone()
        print(f"Conectado a la base de datos: {current_db}")
        
        # Luego buscamos las tablas
        cur.execute("SHOW TABLES;")
        tables = cur.fetchall()
        cur.close()
        
        # Si no se han encontrado tablas, es un indicio de que no se ha creado ninguna tabla
        table_names = [table[0] for table in tables]
        print(f"Tablas encontradas: {table_names}")
        return jsonify(tables=table_names)
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return jsonify(error=str(e)), 500
    # data = request.get_json()
    # respuesta = data.get('enviar')

    #return jsonify(message="Hola desde Flask!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
