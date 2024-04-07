from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Replace with your database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'ultra',
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)

@app.route('/data', methods=['GET'])
def get_data():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM parking_slots")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/change-state', methods=['POST'])
def change_state():
    try:
        data = request.json
        slot_id = data.get('slot_id')
        new_state = data.get('new_state')
        cursor = conn.cursor()
        cursor.execute("UPDATE parking_slots SET state = %s WHERE id = %s", (new_state, slot_id))
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Slot state changed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
