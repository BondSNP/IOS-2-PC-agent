# Security Notes

## 1. 不要暴露到公网

本服务只建议在局域网或 USB 端口转发中使用。不要直接把 `8787` 暴露到公网。

## 2. 使用强 token

生成 token：

```sh
python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
```

不要使用生日、纪念日、简单单词或短 token。

## 3. 保护 env.sh

```sh
chmod 600 /var/mobile/agent/env.sh
```

不要把以下内容提交到 Git：

```text
OPENAI_API_KEY
AGENT_TOKEN
SSH 密码
真实内网 IP
```

## 4. 谨慎开放 /exec

如果实现 `/exec`：

```text
必须 token 验证
必须命令白名单
不能 shell=True
必须 timeout
必须限制输出长度
```

不要把任意命令执行暴露为 HTTP API。
