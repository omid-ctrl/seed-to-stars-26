#!/usr/bin/env bash
# Daily backup of the world the sts26 server is on: saves are paused while it is copied, 7 kept per world.
set -euo pipefail
S=$HOME/minecraft/sts26; B=$HOME/minecraft/sts26-backups; OPS=$HOME/minecraft/sts26-ops
key=$(grep '^level-name=' "$S/server.properties" | cut -d= -f2)
mkdir -p "$B"
rc() { python3 -I -B -c 'import sys;sys.path.insert(0,sys.argv[1]);from rcon import R;p=dict(l.rstrip("\n").split("=",1) for l in open(sys.argv[2]) if "=" in l and not l.startswith("#"));r=R(p["rcon.password"],int(p["rcon.port"]));[print(r.c(c)) for c in sys.argv[3:]]' "$OPS" "$S/server.properties" "$@" || true; }
rc "save-off" "save-all flush"; sleep 5
tar -I 'zstd -T0 -3' -cf "$B/$key-daily-$(date +%Y%m%d-%H%M%S).tar.zst" -C "$S" "$key" || true
rc "save-on"
ls -1t "$B"/"$key"-daily-*.tar.zst 2>/dev/null | tail -n +8 | xargs -r rm -f
