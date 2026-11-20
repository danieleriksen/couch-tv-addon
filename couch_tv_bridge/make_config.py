"""Turn the add-on options into couch-tv's config.json. Prints the bridge's address.

Keeps anything else already in config.json (edits made by the bridge, extra settings), and only
sets the bridge address, the country and this one Samsung TV from the options."""
import json
import os
import socket
import sys

opts_path, cfg_path = sys.argv[1], sys.argv[2]
with open(opts_path) as f:
    o = json.load(f)


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.0.2.1", 9))   # nothing is sent: this only picks the outgoing interface
        return s.getsockname()[0]
    finally:
        s.close()


ip = (o.get("bridge_ip") or "").strip() or lan_ip()
cfg = {}
if os.path.exists(cfg_path):
    try:
        with open(cfg_path) as f:
            cfg = json.load(f)
    except ValueError:
        cfg = {}
bridge = cfg.get("bridge") or {}
bridge.update({"host": ip, "port": 5400})
if o.get("pairing_key"):
    bridge["pairing_key"] = o["pairing_key"]
else:
    bridge.pop("pairing_key", None)
cfg["bridge"] = bridge
cfg["country"] = o.get("country") or "DK"
tv_ip = (o.get("tv_ip") or "").strip()
if not tv_ip:
    sys.exit("Set tv_ip (the TV's address) in the add-on's Configuration tab.")
tvs = [t for t in (cfg.get("tvs") or []) if t.get("id") != "stue"]
old = next((t for t in (cfg.get("tvs") or []) if t.get("id") == "stue"), {})
old.update({"id": "stue", "name": o.get("tv_name") or "Stue", "kind": "samsung", "ip": tv_ip,
            "open_on_power_on": bool(o.get("open_on_power_on", True))})
cfg["tvs"] = [old] + tvs
cfg.setdefault("default_tv", "stue")
tmp = cfg_path + ".tmp"
with open(tmp, "w") as f:
    json.dump(cfg, f, indent=2)
os.replace(tmp, cfg_path)
print("http://%s:5400" % ip)
