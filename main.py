import sys
from src.data_manager import DataManager

# 新增导入
from src.proxy_server import app

def run_proxy_server():
    """运行代理服务器"""
    data_manager = DataManager()
    port = data_manager.config.get('proxy_port', 8080)
    app.run(debug=True, port=port)

def show_mock_data(request_identifier):
    """显示指定请求标识符的Mock数据"""
    data_manager = DataManager()
    print(f"加载的Mock数据 ({request_identifier}):")
    mock_data = data_manager.get_mock_data(request_identifier)
    if mock_data:
        for key, value in mock_data.items():
            print(f"{key}: {value}")
    else:
        print("未找到Mock数据.")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        show_mock_data(sys.argv[1])
    else:
        run_proxy_server()
