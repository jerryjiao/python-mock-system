from mitmproxy import http
import os
import sys
import json

# 基于脚本的位置确定项目根目录
script_dir = os.path.dirname(__file__)
project_root = os.path.dirname(script_dir)

# 将 src 目录添加到 sys.path
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

from utils import read_config, read_response_data

# 更新配置文件和响应目录的路径
config_path = os.path.join(src_dir, "config.json")
responses_dir = os.path.join(project_root, "responses")

config = read_config(config_path)

def request(flow: http.HTTPFlow) -> None:
    """
    拦截请求并根据配置修改响应。
    """
    for interception in config.get("interceptions", []):
        if flow.request.pretty_url == interception["url"]:
            response_file = interception.get("response_file")
            if response_file:
                response_data = read_response_data(response_file, responses_dir)
                if response_data:
                  body = response_data["body"]
                  # 序列化 body 为JSON格式的字符串
                  json_body = json.dumps(body)
                  # 然后将序列化后的JSON字符串编码为字节串
                  content = json_body.encode("utf-8")
                  flow.response = http.Response.make(
                      status_code=response_data["status_code"],
                      headers=response_data["headers"],
                      content=content
                  )
