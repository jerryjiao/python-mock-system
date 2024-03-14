import os  # 导入 os 模块
import json
from typing import Any, Dict

def read_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    读取配置文件并以字典形式返回其内容。

    参数:
        config_path (str): 配置文件的路径。

    返回:
        Dict[str, Any]: 配置数据。
    """
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"配置文件 {config_path} 未找到。")
        return {}
    except json.JSONDecodeError:
        print(f"配置文件 {config_path} 格式错误。")
        return {}

def read_response_data(response_file: str, responses_dir: str = "responses/") -> Dict[str, Any]:
    """
    读取响应数据文件并返回其内容。

    参数:
        response_file (str): 响应数据文件的文件名。
        responses_dir (str): 存储响应数据文件的目录。

    返回:
        Dict[str, Any]: 响应数据。
    """
    # 使用 os.path.join 来确保路径分隔符正确处理
    full_path = os.path.join(responses_dir, response_file)
    try:
        with open(full_path, 'r') as file:
            response_data = json.load(file)
        return response_data
    except FileNotFoundError:
        print(f"响应数据文件 {full_path} 未找到。")
        return {}
    except json.JSONDecodeError:
        print(f"响应数据文件 {full_path} 格式错误。")
        return {}

