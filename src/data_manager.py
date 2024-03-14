import json
import os
import logging
from typing import Any, Dict, Optional

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self, config_path: str = 'config.json'):
        """初始化DataManager，加载配置。

        Args:
            config_path: 配置文件的路径。
        """
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件。

        Returns:
            配置字典。如果加载失败，返回空字典。
        """
        try:
            with open(self.config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"配置文件{self.config_path}未找到。")
            return {}
        except json.JSONDecodeError:
            logger.error(f"配置文件{self.config_path}格式错误。")
            return {}

    def get_mock_data(self, request_path: str) -> Optional[Dict[str, Any]]:
        """根据请求路径获取Mock数据。
        Args:
            request_path: 请求的路径。
        Returns:
            Mock数据字典，如果加载失败，返回None。
        """
        # 构造完整的文件路径
        mock_data_file_path = os.path.join(self.config.get('mock_data_path', '.'), request_path.lstrip('/') + '.json')
        return self.get_mock_data_from_file(mock_data_file_path)

    def get_mock_data_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """直接从给定的文件路径加载Mock数据"""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"Mock数据文件{file_path}未找到。")
            return None
        except json.JSONDecodeError:
            logger.error(f"Mock数据文件{file_path}格式错误。")
            return None

    def save_mock_data(self, request_path: str, data: Dict[str, Any]) -> bool:
        """保存或更新Mock数据到文件。

        Args:
            request_path: 请求的路径。
            data: 要保存的数据。

        Returns:
            成功保存返回True，失败返回False。
        """
        mock_data_path = os.path.join(self.config.get('mock_data_path', '.'), request_path + '.json')
        try:
            with open(mock_data_path, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            logger.error(f"保存Mock数据到文件{mock_data_path}失败：{e}")
            return False
