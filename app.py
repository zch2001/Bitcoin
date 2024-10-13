
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import redis
import datetime

app = Flask(__name__)
CORS(app)  

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        total_supply = redis_client.get('total_supply')
        blockchain_size = redis_client.get('blockchain_size')
        block_height = redis_client.get('block_height')
        network_hashrate = redis_client.get('network_hashrate')
        mempool_size = redis_client.get('mempool_size')
        difficulty = redis_client.get('difficulty')
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        stats = {
            "total_supply": total_supply,
            "blockchain_size": blockchain_size,
            "block_height": block_height,
            "network_hashrate": network_hashrate,
            "mempool_size": mempool_size,
            "difficulty": difficulty,
            "timestamp": timestamp
        }
        return jsonify(stats), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    app.run()

