#!/usr/bin/env python3
"""Seed to Stars 26.3 world switcher on deemo (systemd user unit sts26-worlds.service).

Tails ~/minecraft/sts26/logs/latest.log. When the server itself logs "[Server] STSWORLD|switch|<key>" (written by the
sts_server datapack after an op's 30 s countdown), it stops sts26.service, backs up the world it was on, sets
level-name and starts the server on the new world. Ops: /function sts_server:world/list in game.
Also tells the game which world is loaded (shown by world/list) and starts a one-time Chunky pregeneration per world.
"""
import os
import re
import subprocess
import sys
import time

HOME = os.path.expanduser("~")
SERVER = os.path.join(HOME, "minecraft/sts26")
OPS = os.path.join(HOME, "minecraft/sts26-ops")
BACKUPS = os.path.join(HOME, "minecraft/sts26-backups")
PROPS = os.path.join(SERVER, "server.properties")
LOG = os.path.join(SERVER, "logs/latest.log")
WORLDS = {"crash": "The Crash (Island)", "winter": "Eternal Winter (Snow)", "islands": "Tiny Islands (Ocean)",
          "wasteland": "Wasteland (Desert)", "amplified": "Amplified Snow (fresh world)",
          "standard": "Standard BOP, snow start (fresh world)"}
KEEP_BACKUPS = 5
PREGEN_RADIUS = 1500
MARK = re.compile(r"^\[[0-9:]+\] \[Server thread/INFO\]: \[Server\] STSWORLD\|switch\|([a-z]+)$")
READY = re.compile(r"^\[[0-9:]+\] \[Server thread/INFO\]: Done \(")


def log(msg):
    print(time.strftime("%F %T ") + msg, flush=True)


def props():
    out = {}
    for line in open(PROPS, encoding="utf-8"):
        if "=" in line and not line.startswith("#"):
            k, v = line.rstrip("\n").split("=", 1)
            out[k] = v
    return out


def set_level(key):
    lines = [l for l in open(PROPS, encoding="utf-8").read().splitlines() if not l.startswith("level-name=")]
    lines.append(f"level-name={key}")
    open(PROPS, "w", encoding="utf-8").write("\n".join(lines) + "\n")


def rcon(*cmds):
    sys.path.insert(0, OPS)
    from rcon import R  # noqa: E402
    p = props()
    try:
        r = R(p["rcon.password"], int(p.get("rcon.port", "25576")))
        return [r.c(c) for c in cmds]
    except OSError:
        return None


def systemctl(*args):
    return subprocess.run(["systemctl", "--user", *args], capture_output=True, text=True, timeout=300).returncode


def backup(key):
    src = os.path.join(SERVER, key)
    if not os.path.isfile(os.path.join(src, "level.dat")):
        return
    os.makedirs(BACKUPS, exist_ok=True)
    dst = os.path.join(BACKUPS, f"{key}-{time.strftime('%Y%m%d-%H%M%S')}.tar.zst")
    subprocess.run(["tar", "-I", "zstd -T0 -3", "-cf", dst, "-C", SERVER, key], check=False)
    old = sorted(f for f in os.listdir(BACKUPS) if f.startswith(key + "-"))
    for f in old[:-KEEP_BACKUPS]:
        os.remove(os.path.join(BACKUPS, f))
    log(f"backed up {key} -> {dst}")


SNOW_START = {"amplified", "standard"}   # fresh worlds whose spawn is moved into the nearest snowy biome on first boot


def snow_spawn(key):
    marker = os.path.join(SERVER, key, ".sts26-snowspawn")
    if os.path.exists(marker):
        return
    for target in ("#c:is_snowy", "#minecraft:spawns_snow_foxes", "minecraft:snowy_slopes"):
        out = rcon(f"locate biome {target}") or [""]
        m = re.search(r"at \[(-?\d+), (?:~|-?\d+), (-?\d+)\]", out[0])
        if m:
            x, z = m.groups()
            res = rcon(f"forceload add {x} {z}",
                       f"execute in minecraft:overworld positioned {x} 0 {z} positioned over motion_blocking_no_leaves "
                       f"run setworldspawn ~ ~ ~", "gamerule respawn_radius 0", f"forceload remove {x} {z}")
            if not any("Set the world spawn" in (s or "") for s in (res or [])):
                log(f"snow spawn for {key}: setworldspawn failed: {res}")
                return
            log(f"snow spawn for {key}: {target} at {x},{z}: {res}")
            open(marker, "w").write(f"{x} {z}\n")
            return
    log(f"no snowy biome found near spawn of {key}")


def after_boot():
    """Tell the game which world is on; start a one-time pregeneration for a world that has not had one."""
    key = props().get("level-name", "")
    name = WORLDS.get(key, key)
    rcon(f'data modify storage sts_server:world current set value "{name}"')
    if key in SNOW_START:
        snow_spawn(key)
    marker = os.path.join(SERVER, key, ".sts26-pregen")
    if not os.path.exists(marker):
        rcon("chunky world minecraft:overworld", "chunky shape circle", "chunky spawn", f"chunky radius {PREGEN_RADIUS}",
             "chunky start")
        open(marker, "w").write(time.strftime("%F %T") + "\n")
        log(f"started chunky pregeneration of {key}, radius {PREGEN_RADIUS}")


def switch(key):
    cur = props().get("level-name")
    if key not in WORLDS or key == cur:
        rcon(f'tellraw @a {{"text":"[World] Already on {WORLDS.get(key, key)}.","color":"gray"}}')
        return
    log(f"switching {cur} -> {key}")
    rcon("save-all flush")
    time.sleep(2)
    systemctl("stop", "sts26.service")
    backup(cur)
    set_level(key)
    systemctl("start", "sts26.service")


def follow(path):
    fh, inode, pos, first = None, None, 0, True
    while True:
        try:
            st = os.stat(path)
        except OSError:
            st = None
        if st is not None and (fh is None or st.st_ino != inode or st.st_size < pos):
            if fh:
                fh.close()
            fh = open(path, "rb")
            inode, pos = st.st_ino, (st.st_size if first else 0)
            fh.seek(pos)
            first = False
        line = fh.readline() if fh else b""
        if not line:
            time.sleep(1)
            continue
        pos = fh.tell()
        yield line.decode("utf-8", "replace").rstrip("\r\n")


def main():
    log("watching " + LOG)
    if rcon("list") is not None:
        after_boot()
    last = 0.0
    for line in follow(LOG):
        if READY.match(line):
            time.sleep(3)
            after_boot()
            continue
        m = MARK.match(line)
        if m and time.time() - last > 60:
            last = time.time()
            switch(m.group(1))


if __name__ == "__main__":
    main()
