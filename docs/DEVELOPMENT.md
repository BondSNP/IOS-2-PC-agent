# Development Guide

本文档说明如何修改和扩展 `server.py`。

## 1. 修改 server.py 的标准流程

### 1.1 备份当前版本

```sh
cd /var/mobile/agent
cp server.py "server.py.bak.$(date +%Y%m%d_%H%M%S)"
```

### 1.2 修改代码

```sh
nano /var/mobile/agent/server.py
```

或从 Windows 上传：

```cmd
scp C:\Path\To\server.py mobile@<IPHONE_IP>:/var/mobile/agent/server.py
```

### 1.3 语法检查

```sh
/var/mobile/agent/venv/bin/python3 -m py_compile /var/mobile/agent/server.py
```

没有输出表示语法通过。

### 1.4 重启服务

```sh
sudo launchctl kickstart -k system/com.example.iphoneagent
```

### 1.5 验证

```sh
curl http://127.0.0.1:8787/health
curl http://127.0.0.1:8787/status
tail -n 80 /var/mobile/agent/agent.err
```

## 2. 修改 env.sh 后如何生效

如果修改了：

```text
OPENAI_API_KEY
AGENT_TOKEN
OPENAI_MODEL
AGENT_SERVER_VERSION
```

执行：

```sh
chmod 600 /var/mobile/agent/env.sh
sudo launchctl kickstart -k system/com.example.iphoneagent
```

## 3. 修改 plist 后如何生效

如果修改了 plist，不能只用 `kickstart`，应重新加载：

```sh
sudo launchctl bootout system/com.example.iphoneagent 2>/dev/null
sudo launchctl bootstrap system /var/jb/Library/LaunchDaemons/com.example.iphoneagent.plist
sudo launchctl enable system/com.example.iphoneagent
sudo launchctl kickstart -k system/com.example.iphoneagent
```

## 4. 自定义服务标识符

默认服务标识符：

```text
com.example.iphoneagent
```

可以自定义，例如：

```text
com.local.iphoneagent
```

如果修改，必须同步修改：

```text
plist 文件名
plist 内 Label
launchctl system/<SERVICE_ID>
```

## 5. 扩展接口

当前已有接口：

```text
GET  /health
GET  /status
GET  /logs
POST /ask
```

### 5.1 推荐扩展顺序

优先扩展只读接口：

```text
/status
/logs
/version
```

谨慎扩展高风险接口：

```text
/exec
/file
/task
```

### 5.2 /exec 安全原则

如果加入 `/exec`，不要允许任意 shell 命令。必须使用：

```text
token 验证
命令白名单
subprocess.run([...], shell=False)
timeout
输出长度限制
```

### 5.3 回归测试清单

每次修改后执行：

```sh
/var/mobile/agent/venv/bin/python3 -m py_compile /var/mobile/agent/server.py
sudo launchctl kickstart -k system/com.example.iphoneagent
curl http://127.0.0.1:8787/health
curl http://127.0.0.1:8787/status
tail -n 80 /var/mobile/agent/agent.err
```

Windows 端：

```cmd
ia /health
ia /status
ia Say hello in one sentence.
```
