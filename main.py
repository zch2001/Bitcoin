import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 从环境变量中获取数据库配置
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')


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


@app.route('/api/get_data', methods=['POST', 'OPTIONS'])
def get_data():
    if request.method == 'OPTIONS':
        # 处理预检请求
        return _build_cors_prelight_response()

    if request.method == 'POST':
        try:
            # 获取数据库连接
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = "SELECT * FROM Best_blocks"
                cursor.execute(query)
                results = cursor.fetchall()  # 获取所有数据

            connection.close()

            # 返回 JSON 数据给前端
            return jsonify({"data": results}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


def _build_cors_prelight_response():
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response, 200


if __name__ == '__main__':
    # 主机名和端口
    hostName = "localhost"
    hostPort = 5000
    print(f"Server started at http://{hostName}:{hostPort}")
    app.run(host=hostName, port=hostPort, debug=True)
