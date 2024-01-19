from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode
import ssl

app = Flask(__name__)

# Define the database connection parameters
config = {
    'host': 'matinacrossing.mysql.database.azure.com',
    'user': 'admindb',
    'password': '@Qwerty123',
    'database': 'brgy_informationdb',
    'client_flags': [mysql.connector.ClientFlag.SSL],
    'ssl_ca': r'C:\Users\User\Downloads\DigiCertGlobalRootCA.crt.pem',  # Update with the correct SSL certificate path
}

try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

# Create 'users' table if not exists
with conn.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL
        );
    """)
    print("Table 'users' created")

# Close the connection when the application exits
@app.teardown_appcontext
def close_connection(exception=None):
    if conn is not None and conn.is_connected():
        conn.close()
        print("Database connection closed")

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not all([name, password]):
        return jsonify({"message": "Incomplete data"}), 400

    with conn.cursor() as cursor:
        # Check if the user already exists
        cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"message": "User already exists"}), 409

        # Insert the user data into the database
        cursor.execute("INSERT INTO users (name, password) VALUES (%s, %s)", (name, password))
        conn.commit()

    return jsonify({"message": "Registration successful"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
