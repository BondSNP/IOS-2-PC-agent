#!/var/jb/usr/bin/sh
set -eu

SERVICE_ID="${SERVICE_ID:-com.example.iphoneagent}"

launchctl kickstart -k "system/$SERVICE_ID"
curl http://127.0.0.1:8787/health
