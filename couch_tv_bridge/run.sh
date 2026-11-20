#!/bin/sh
# Writes /data/config.json from the add-on's options, builds the Samsung app for this bridge
# (downloadable from the bridge at /CouchTV.wgt), then starts the bridge.
set -e
export COUCH_CONFIG=/data/config.json
export COUCH_DATA=/data/bridge-data
mkdir -p "$COUCH_DATA"
BRIDGE_URL=$(/venv/bin/python /make_config.py /data/options.json "$COUCH_CONFIG")
echo "couch-tv: bridge address $BRIDGE_URL"
if /venv/bin/python /app/samsung/build.py --bridge "$BRIDGE_URL" >/tmp/build.log 2>&1; then
  cp /app/build/samsung/CouchTV.wgt /app/remote/dist/CouchTV.wgt
  echo "couch-tv: Samsung app ready at $BRIDGE_URL/CouchTV.wgt"
else
  echo "couch-tv: building the Samsung app failed:"; cat /tmp/build.log
fi
exec /venv/bin/python /app/bridge/server.py
