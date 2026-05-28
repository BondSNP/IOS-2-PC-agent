#!/var/jb/usr/bin/sh
set -eu

SERVICE_ID="${SERVICE_ID:-com.example.iphoneagent}"

echo "== launchd =="
launchctl print "system/$SERVICE_ID" || true

echo
echo "== process =="
ps aux | grep '[s]erver.py' || true

echo
echo "== health =="
curl http://127.0.0.1:8787/health || true

echo
echo "== logs =="
tail -n 80 /var/mobile/agent/agent.log 2>/dev/null || true

echo
echo "== errors =="
tail -n 80 /var/mobile/agent/agent.err 2>/dev/null || true
