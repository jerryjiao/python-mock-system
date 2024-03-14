## MITMProxy 拦截系统使用文档

### 介绍

本文档旨在指导用户如何使用MITMProxy作为中间人代理，用于拦截和修改HTTP/HTTPS请求和响应，特别适用于测试和开发环境中模拟后端服务。

### 准备

确保安装有Python 3和mitmproxy。可以通过运行以下命令安装mitmproxy：

```bash
pip install -r requirements.txt
```

### 项目结构

- **src/config.json**：定义拦截规则的配置文件。
- **src/interceptor.py**：拦截脚本，用于处理请求和修改响应。
- **responses/**：存放响应模板的目录。

### 设置拦截规则

编辑`src/config.json`来定义你的拦截规则。示例如下：

```json
{
    "interceptions": [
      {
        "url": "/mock",
        "response_file": "test_response.json"
      }
    ]
}
```

此配置指示拦截对`/mock`的请求，并返回`responses/test_response.json`中定义的响应。

### 响应数据定义

在`responses/`目录下创建响应数据文件。示例`test_response.json`内容如下：

```json
{
  "status_code": 200,
  "headers": {"Content-Type": "application/json"},
  "body": {"message": "This is a mock response"}
}
```

### 运行MITMProxy

使用`mitmweb`以图形界面方式运行：

```bash
mitmweb -s src/interceptor.py
```

### Chrome浏览器配置

使用`SwitchyOmega`插件快速切换Chrome的代理设置。

1. **安装SwitchyOmega**：
   - 从Chrome网上应用店安装`SwitchyOmega`扩展。

2. **配置SwitchyOmega**：
   - 打开SwitchyOmega的选项，创建新的情景模式，命名为“mitmproxy”。
   - 设置代理服务器（协议：HTTP，服务器：localhost，端口：8080）。
   - 保存配置。

3. **使用SwitchyOmega**：
   - 点击浏览器右上角SwitchyOmega图标，选择“mitmproxy”模式以启用代理。

### 获取MITMProxy证书

1. 在Chrome中配置好代理后，访问[http://mitm.it](http://mitm.it)下载mitmproxy的根证书。
2. 在Chrome的设置中导入并信任下载的证书。

### 注意事项

- 确保MITMProxy正在运行，并且系统或浏览器已经安装并信任了MITMProxy的根证书。
- 代理使用可能会影响网络性能，建议仅在需要时启用。

### 完成

至此，你已成功设置了MITMProxy拦截系统，并通过Chrome浏览器配合SwitchyOmega插件使用。这套系统可以帮助你在开发和测试过程中轻松模拟后端服务的响应。
