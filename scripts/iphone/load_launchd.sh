#!/var/jb/usr/bin/sh
set -eu

SERVICE_ID="${SERVICE_ID:-com.example.iphoneagent}"
PLIST="${PLIST:-/var/jb/Library/LaunchDaemons/$SERVICE_ID.plist}"

chown root:wheel "$PLIST"
chmod 644 "$PLIST"

launchctl bootout "system/$SERVICE_ID" 2>/dev/null || true
launchctl bootstrap system "$PLIST"
launchctl enable "system/$SERVICE_ID"
launchctl kickstart -k "system/$SERVICE_ID"

launchctl print "system/$SERVICE_ID"
