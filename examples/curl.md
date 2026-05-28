# curl Examples

## Health

```cmd
curl.exe http://<IPHONE_IP>:8787/health
```

## Ask from Windows cmd.exe

```cmd
curl.exe -X POST "http://<IPHONE_IP>:8787/ask" ^
  -H "Authorization: Bearer YOUR_LONG_RANDOM_AGENT_TOKEN_HERE" ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"Say hello in one sentence.\"}"
```

## Ask from PowerShell

```powershell
curl.exe -X POST "http://<IPHONE_IP>:8787/ask" `
  -H "Authorization: Bearer YOUR_LONG_RANDOM_AGENT_TOKEN_HERE" `
  -H "Content-Type: application/json" `
  -d "{\"prompt\":\"Say hello in one sentence.\"}"
```

## Logs

```cmd
curl.exe -X GET "http://<IPHONE_IP>:8787/logs" -H "Authorization: Bearer YOUR_LONG_RANDOM_AGENT_TOKEN_HERE"
```
