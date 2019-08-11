# realXiaoice
真正唯一可用的微软小冰API

来源为新浪微博

# 环境
Python 3

# 依赖
* tornado
* requests

# 使用方法
## 1. 领养小冰 
注册一个新浪微博账号，领养小冰，确保与小冰的私信是正常的
## 2. 登录微博账号
使用Chrome或者Firefox，建议开启隐身模式，打开 [https://m.weibo.cn](https://m.weibo.cn)， 登录你的微博账号
## 3. 获取headers
打开和小冰的私信页面，按F12打开控制台，切换到Network，并选中XHR，然后和小冰说句话，点开名为send的请求

复制全部Request Headers中**除了Content-Length以外所有行**，粘贴到headers.txt中

![](assets/182123.png)

## 4. 安装Python 3与依赖
安装适合自己平台的Python，然后
```bash
pip install tornado requests
``` 

## 5. 运行
```bash
python ice_server.py
```
## 6. systemd
```unit file (systemd)
[Unit]
Description=xiaoice API by Benny
After=network.target network-online.target nss-lookup.target

[Service]
User=nobody
Restart=on-failure
Type=simple

WorkingDirectory=/path/to/realXiaoice
ExecStart=/usr/bin/python3 /path/to/realXiaoice/ice_server.py

[Install]
WantedBy=multi-user.target

```

# API
## 请求格式
接受GET、POST url-encoded-data和POST json，示例如下：
```http request

# curl http://127.0.0.1:6789/chat?text=hello
GET http://127.0.0.1:6789/chat?text=hello

###


POST http://127.0.0.1:6789/chat
Content-Type: application/json

{
  "text": "what"
}


###


# curl -d "text=hi" http://127.0.0.1:6789/chat
POST http://127.0.0.1:6789/chat
Content-Type: application/x-www-form-urlencoded

text=hi

###



```

更多详情请参考 [api.http](api.http)


## 响应格式
### 成功
HTTP 200
```json
{
    "text": "想我干嘛",
    "debug": ""
}
```
### 参数错误
HTTP 400
```json
{
    "text": "",
    "debug": "client wrong reason"
}
```
### 服务端错误
HTTP 500
```json
{
    "text": "",
    "debug": "server wrong reason"
}
```


# 效果图

![](assets/183303.png)


# TODO
- [ ] 增加访问限制

# Credits
https://github.com/yanwii/msxiaoiceapi


# License
MIT