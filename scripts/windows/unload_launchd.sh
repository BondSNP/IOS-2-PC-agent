#!/var/jb/usr/bin/sh
set -eu

SERVICE_ID="${SERVICE_ID:-com.example.iphoneagent}"

launchctl bootout "system/$SERVICE_ID" 2>/dev/null || true
