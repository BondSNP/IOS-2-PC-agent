#!/var/jb/usr/bin/sh
cd /var/mobile/agent || exit 10
. /var/mobile/agent/env.sh || exit 11
exec /var/mobile/agent/venv/bin/python3 -u /var/mobile/agent/server.py
