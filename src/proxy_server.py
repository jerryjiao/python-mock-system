import sys
import logging
from flask import Flask, request, jsonify, Response
import requests
from src.data_manager import DataManager
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
data_manager = DataManager()

# 假设后端服务的基础URL在配置文件中定义为real_backend_url
backend_url = data_manager.config.get('real_backend_url', 'http://localhost:5000')

def forward_request(path):
    """转发请求到实际的后端服务"""
    response = requests.request(
        method=request.method,
        url=backend_url + '/' + path,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mock_or_forward(path):
    """根据配置决定是返回Mock数据还是转发请求"""
    mock_data = data_manager.get_mock_data(path)
    if mock_data and 'response' in mock_data:
        response_data = mock_data['response']
        return (jsonify(response_data.get('body', {})), 
                response_data.get('status_code', 200), 
                response_data.get('headers', {}))
    else:
        logger.info(f"转发请求到后端服务: {path}")
        return forward_request(path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 允许通过命令行参数指定代理端口
        port = int(sys.argv[1])
    else:
        port = data_manager.config.get('proxy_port', 8080)
    app.run(debug=True, port=port, ssl_context=('certs/cert.pem', 'certs/key.pem'))
