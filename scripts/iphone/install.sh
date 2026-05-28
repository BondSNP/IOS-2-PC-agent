#!/var/jb/usr/bin/sh
set -eu

SERVICE_ID="${SERVICE_ID:-com.example.iphoneagent}"
AGENT_DIR="${AGENT_DIR:-/var/mobile/agent}"
LAUNCHD_DIR="${LAUNCHD_DIR:-/var/jb/Library/LaunchDaemons}"

echo "[1/6] Creating agent directory: $AGENT_DIR"
mkdir -p "$AGENT_DIR"

echo "[2/6] Installing Python virtual environment"
cd "$AGENT_DIR"
python3 -m venv venv
. "$AGENT_DIR/venv/bin/activate"
python3 -m pip install --upgrade pip setuptools wheel

echo "[3/6] Checking required files"
test -f "$AGENT_DIR/server.py" || { echo "Missing $AGENT_DIR/server.py"; exit 1; }
test -f "$AGENT_DIR/env.sh" || { echo "Missing $AGENT_DIR/env.sh"; exit 1; }
test -f "$AGENT_DIR/run.sh" || { echo "Missing $AGENT_DIR/run.sh"; exit 1; }

chmod 600 "$AGENT_DIR/env.sh"
chmod +x "$AGENT_DIR/run.sh"

echo "[4/6] Syntax check"
"$AGENT_DIR/venv/bin/python3" -m py_compile "$AGENT_DIR/server.py"

echo "[5/6] Installing launchd plist"
mkdir -p "$LAUNCHD_DIR"
test -f "$LAUNCHD_DIR/$SERVICE_ID.plist" || {
  echo "Missing $LAUNCHD_DIR/$SERVICE_ID.plist"
  echo "Copy config/com.example.iphoneagent.plist to $LAUNCHD_DIR/$SERVICE_ID.plist first."
  exit 1
}
chown root:wheel "$LAUNCHD_DIR/$SERVICE_ID.plist"
chmod 644 "$LAUNCHD_DIR/$SERVICE_ID.plist"

echo "[6/6] Bootstrap launchd service"
launchctl bootout "system/$SERVICE_ID" 2>/dev/null || true
launchctl bootstrap system "$LAUNCHD_DIR/$SERVICE_ID.plist"
launchctl enable "system/$SERVICE_ID"
launchctl kickstart -k "system/$SERVICE_ID"

echo "Done. Verify with:"
echo "  curl http://127.0.0.1:8787/health"
