
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import redis

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 从环境变量中获取数据库配置
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

# 配置 Redis 连接
redis_client = redis.Redis(
    host='redis-13139.c73.us-east-1-2.ec2.redns.redis-cloud.com',
    port=13139,
    password='gBDV7hVG4HHLbsEi8xd4euZfW0JxLZM8',
    decode_responses=True
)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        # 从 Redis 获取数据
        total_supply = redis_client.get('total_supply')
        blockchain_size = redis_client.get('blockchain_size')
        block_height = redis_client.get('block_height')
        network_hashrate = redis_client.get('network_hashrate')
        mempool_size = redis_client.get('mempool_size')
        difficulty = redis_client.get('difficulty')

        # 构建响应数据
        stats = {
            "total_supply": total_supply,
            "blockchain_size": blockchain_size,
            "block_height": block_height,
            "network_hashrate": network_hashrate,
            "mempool_size": mempool_size,
            "difficulty": difficulty
        }
        return jsonify(stats), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 创建数据库连接
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

