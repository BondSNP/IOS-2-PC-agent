# Troubleshooting

## 1. 查看服务状态

```sh
sudo launchctl print system/com.example.iphoneagent
ps aux | grep '[s]erver.py'
curl http://127.0.0.1:8787/health
tail -n 100 /var/mobile/agent/agent.log
tail -n 100 /var/mobile/agent/agent.err
```

## 2. system 服务找不到

如果：

```text
Could not find service "com.example.iphoneagent" in domain for system
```

说明服务没有加载到 system 域。执行：

```sh
sudo launchctl bootstrap system /var/jb/Library/LaunchDaemons/com.example.iphoneagent.plist
```

不要加 `2>/dev/null`，观察真实错误。

## 3. last exit code = 78: EX_CONFIG

通常是配置错误。检查：

```sh
cat /var/mobile/agent/run.sh
cat /var/mobile/agent/env.sh
cat /var/jb/Library/LaunchDaemons/com.example.iphoneagent.plist
tail -n 100 /var/mobile/agent/agent.err
```

常见原因：

```text
/ bin/sh 路径错误，应使用 /var/jb/usr/bin/sh
env.sh 不存在
env.sh 缺少 OPENAI_API_KEY 或 AGENT_TOKEN
server.py 路径错误
venv 路径错误
plist 中残留 UserName=mobile
```

## 4. 服务进入 user/501

如果 `launchctl print` 显示：

```text
domain = user/501
username = mobile
jetsam memory limit = 6 MB
```

说明 plist 中设置了：

```xml
<key>UserName</key>
<string>mobile</string>
```

删除 `UserName` 字段，重新加载到 system 域。

## 5. Windows 连不上 8787

先在 iPhone 本机确认：

```sh
curl http://127.0.0.1:8787/health
```

再确认监听：

```sh
netstat -an | grep 8787
```

理想结果：

```text
tcp4       0      0  *.8787                 *.*                    LISTEN
```

如果 iPhone 本机通但 Windows 不通：

```text
检查 IP 是否正确
检查是否在同一网络
改用 iproxy 8787 8787
```

## 6. pydantic-core 错误

如果出现：

```text
ValueError: Unknown macOS machine: iPhone10,1
```

不要继续安装 FastAPI / Pydantic v2。本项目不需要这些依赖。
