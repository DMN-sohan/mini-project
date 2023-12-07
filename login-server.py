from flask import Flask, request, jsonify, send_file
from flask_mysqldb import MySQL
from flask_cors import CORS
import random
import string
from PIL import Image
from io import BytesIO
# import make_image

app = Flask(__name__)
CORS(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mini_project'
app.config['CORS_HEADERS'] = 'Content-Type'
mysql = MySQL(app)

def generate_random_alphanumeric():
    characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
    random_sequence = ''.join(random.choice(characters) for _ in range(7))

    return random_sequence



@app.route("/login", methods=['POST'])
async def login():

    try:
        
        data = request.get_json()

        # Access parameters from the JSON data
        username = data.get('username')
        password = data.get('password')

        cur = mysql.connection.cursor()
        users = cur.execute("SELECT * FROM CLIENT_CREDENTIALS WHERE email = %s", (username,))
        if users < 1 :
            return jsonify({"error" : True, "message" : "Invalid username"})
        else : 
            users = cur.execute("SELECT * FROM CLIENT_CREDENTIALS WHERE email = %s AND password = %s", (username,password))
            if users < 1:
                return jsonify({"error" : True, "message" : "Invalid password"})
            return jsonify({"error" : False, "message" : "Login Successful", "response" : cur.fetchall()})
        
    except Exception as e:
        # Handle exceptions, e.g., invalid JSON format
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)