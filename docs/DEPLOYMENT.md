# Deployment Guide

本指南描述如何从越狱后的 iPhone 8 开始部署 agent server。

## 1. 前提

- iPhone 8 已通过 palera1n rootless 越狱
- 已安装 Sileo / Procursus
- 可以通过 SSH 进入 iPhone
- iPhone 中存在 `/var/jb/usr/bin/sh`
- 电脑端可以访问 iPhone 的局域网 IP，或使用 `iproxy`

## 2. 安装基础依赖

在 iPhone SSH 中执行：

```sh
sudo apt update
sudo apt install python3 python3-pip curl ca-certificates openssh bash dash
```

确认 shell 路径：

```sh
command -v sh
```

应返回：

```text
/var/jb/usr/bin/sh
```

## 3. 复制项目文件到 iPhone

目标路径：

```text
/var/mobile/agent
```

需要复制：

```text
src/server.py                  -> /var/mobile/agent/server.py
config/env.example.sh          -> /var/mobile/agent/env.sh
scripts/iphone/run.sh          -> /var/mobile/agent/run.sh
config/com.example.iphoneagent.plist -> /var/jb/Library/LaunchDaemons/com.example.iphoneagent.plist
```

## 4. 创建 venv

```sh
mkdir -p /var/mobile/agent
cd /var/mobile/agent
python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
```

本项目不需要安装 FastAPI、Pydantic、Uvicorn 或 OpenAI Python SDK。

## 5. 配置 env.sh

```sh
cat > /var/mobile/agent/env.sh <<'EOF'
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
export AGENT_TOKEN="YOUR_LONG_RANDOM_AGENT_TOKEN_HERE"
export OPENAI_MODEL="gpt-4o"
export AGENT_SERVER_VERSION="0.1.0"
EOF

chmod 600 /var/mobile/agent/env.sh
```

生成随机 token：

```sh
python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
```

## 6. 手动测试

```sh
cd /var/mobile/agent
. /var/mobile/agent/env.sh
/var/mobile/agent/venv/bin/python3 -m py_compile /var/mobile/agent/server.py
/var/mobile/agent/venv/bin/python3 -u /var/mobile/agent/server.py
```

另开一个 SSH 窗口：

```sh
curl http://127.0.0.1:8787/health
```

## 7. 加载 launchd

```sh
sudo chown root:wheel /var/jb/Library/LaunchDaemons/com.example.iphoneagent.plist
sudo chmod 644 /var/jb/Library/LaunchDaemons/com.example.iphoneagent.plist
chmod +x /var/mobile/agent/run.sh

sudo launchctl bootstrap system /var/jb/Library/LaunchDaemons/com.example.iphoneagent.plist
sudo launchctl enable system/com.example.iphoneagent
sudo launchctl kickstart -k system/com.example.iphoneagent
```

## 8. 验证

```sh
sudo launchctl print system/com.example.iphoneagent
ps aux | grep '[s]erver.py'
curl http://127.0.0.1:8787/health
```

Windows 端：

```cmd
curl.exe http://<IPHONE_IP>:8787/health
```
