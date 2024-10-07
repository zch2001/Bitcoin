import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)


MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')
FLASK_PORT = os.getenv('FLASK_PORT', 5000)



def get_db_connection():
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


@app.route('/api/get_data', methods=['GET', 'OPTIONS'])
def get_data():
    if request.method == 'OPTIONS':

        return _build_cors_prelight_response()

    if request.method == 'GET':
        try:

            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = "SELECT * FROM Best_blocks"
                cursor.execute(query)
                results = cursor.fetchall()

            connection.close()

            return jsonify({"data": results}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


def _build_cors_prelight_response():
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response, 200


if __name__ == '__main__':
    hostName = "0.0.0.0"
    app.run(host=hostName, port=FLASK_PORT, debug=True)
