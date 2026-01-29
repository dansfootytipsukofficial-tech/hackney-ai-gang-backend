#!/usr/bin/env bash
# Restart the Hackney backend and run a quick test against the grok model.
# Usage: ./restart_and_test.sh

set -e
cd "$(dirname "$0")"

# Kill any running uvicorn instances for this app (best-effort)
pkill -f 'uvicorn app.main:app' || true

# Start the server in background using the venv python
if [ -x ./venv/bin/python ]; then
  ./venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8002 &
else
  python -m uvicorn app.main:app --host 127.0.0.1 --port 8002 &
fi

VPID=$!
# give it a couple seconds to start
sleep 2

echo "Server started (PID=$VPID). Testing /chat with grok-code-fast-1..."

# Do a quick curl test
curl -s -X POST http://127.0.0.1:8002/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Write a short Hackney boss-style greeting","model":"grok-code-fast-1"}'

echo

echo "If you get a response, Grok is working. If you see an error about missing XAI_API_KEY, run ./set_xai_key.py to set it first." 
