# iPhone 8 Agent Server

把一台已经通过 **palera1n rootless jailbreak** 越狱的 iPhone 8 变成一个低功耗、长期待机、可通过 HTTP 调用的轻量 agent 节点。

本项目不尝试把 iPhone 8 刷成 Linux，也不依赖 iSH 常驻后台。它使用 iOS 越狱环境中的 `launchd` system daemon 托管一个 Python 标准库 HTTP server。

## 架构

```text
Windows / LAN client
    |
    | HTTP POST /ask
    v
iPhone 8:8787
    |
    | Python stdlib HTTPServer
    v
OpenAI Responses API
    |
    v
JSON response
```

## 特点

- 不依赖 iSH
- 不依赖 FastAPI / Pydantic / Uvicorn
- 不依赖 Docker
- 不需要 Linux 内核
- 使用 Python 标准库实现 HTTP server
- 使用 `launchd` 保活
- Windows 端封装成 `ia` 命令

## 目录结构

```text
iphone8-agent-server/
├── src/
│   └── server.py
├── config/
│   ├── env.example.sh
│   └── com.example.iphoneagent.plist
├── scripts/
│   ├── iphone/
│   │   ├── install.sh
│   │   ├── load_launchd.sh
│   │   ├── unload_launchd.sh
│   │   ├── restart.sh
│   │   ├── status.sh
│   │   └── run.sh
│   └── windows/
│       ├── install-client.ps1
│       ├── iphone-agent.ps1
│       └── ia.bat
├── docs/
│   ├── DEPLOYMENT.md
│   ├── DEVELOPMENT.md
│   ├── TROUBLESHOOTING.md
│   └── SECURITY.md
├── examples/
│   └── curl.md
├── .gitignore
├── LICENSE
└── README.md
```

## 快速部署

### 1. iPhone 端

在 iPhone 越狱 SSH 终端中执行：

```sh
mkdir -p /var/mobile/agent
```

把项目中的以下文件复制到 iPhone：

```text
src/server.py                  -> /var/mobile/agent/server.py
config/env.example.sh          -> /var/mobile/agent/env.sh
scripts/iphone/run.sh          -> /var/mobile/agent/run.sh
config/com.example.iphoneagent.plist -> /var/jb/Library/LaunchDaemons/com.example.iphoneagent.plist
```

编辑 `/var/mobile/agent/env.sh`：

```sh
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
export AGENT_TOKEN="YOUR_LONG_RANDOM_AGENT_TOKEN_HERE"
export OPENAI_MODEL="gpt-4o"
```

然后加载服务：

```sh
sudo launchctl bootstrap system /var/jb/Library/LaunchDaemons/com.example.iphoneagent.plist
sudo launchctl enable system/com.example.iphoneagent
sudo launchctl kickstart -k system/com.example.iphoneagent
```

验证：

```sh
curl http://127.0.0.1:8787/health
```

### 2. Windows 端

在 PowerShell 中执行：

```powershell
cd path\to\iphone8-agent-server\scripts\windows
.\install-client.ps1 -InstallDir "D:\Tools\iPhoneAgent" -AgentUrl "http://<IPHONE_IP>:8787/ask" -AgentToken "YOUR_LONG_RANDOM_AGENT_TOKEN_HERE"
```

重新打开终端后：

```cmd
ia /health
ia 请用一句话说明你现在运行在哪台设备上
```

## 服务标识符说明

本项目默认使用：

```text
com.example.iphoneagent
```

这是 launchd 服务标识符，不是用户名。你可以自定义，例如：

```text
com.local.iphoneagent
com.lab.iphone8agent
```

如果修改，必须同步修改：

```text
/var/jb/Library/LaunchDaemons/<SERVICE_ID>.plist
plist 内的 Label
launchctl 命令中的 system/<SERVICE_ID>
```

## 文档

- [部署指南](docs/DEPLOYMENT.md)
- [后期修改与扩展](docs/DEVELOPMENT.md)
- [故障排查](docs/TROUBLESHOOTING.md)
- [安全注意事项](docs/SECURITY.md)

## License

MIT
