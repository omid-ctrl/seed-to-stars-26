#!/usr/bin/env python3
"""Find a good snow seed with the pack's real world generation (Terralith etc.), on the sts26 server.

For each candidate seed: start the server on a throwaway world 'seedtest', find the nearest snowy village, then measure
from that village how far ice spikes, frozen peaks, snowy taiga and an igloo are. Lower total = better snow start.
Usage (on deemo, with sts26.service and sts26-worlds.service stopped): python3 seed_search.py N
"""
import os
import random
import re
import shutil
import subprocess
import sys
import time

HOME = os.path.expanduser("~")
SERVER = os.path.join(HOME, "minecraft/sts26")
PROPS = os.path.join(SERVER, "server.properties")
sys.path.insert(0, os.path.join(HOME, "minecraft/sts26-ops"))
from rcon import R  # noqa: E402

LOC = re.compile(r"at \[(-?\d+), (?:~|-?\d+), (-?\d+)\] \((\d+) blocks")


def setprops(**kv):
    lines = [l for l in open(PROPS).read().splitlines() if l.split("=", 1)[0] not in kv]
    lines += [f"{k}={v}" for k, v in kv.items()]
    open(PROPS, "w").write("\n".join(lines) + "\n")


def props():
    return dict(l.split("=", 1) for l in open(PROPS).read().splitlines() if "=" in l and not l.startswith("#"))


def sysd(*a):
    subprocess.run(["systemctl", "--user", *a], check=False)


def wait_rcon(timeout=240):
    log = os.path.join(SERVER, "logs/latest.log")
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(3)
        try:
            p = props()
            r = R(p["rcon.password"], int(p["rcon.port"]))
            r.c("list")
            return r
        except OSError:
            continue
    raise RuntimeError("server did not come up; see " + log)


def score(r):
    out = {}
    v = LOC.search(r.c("locate structure minecraft:village_snowy"))
    if not v:
        return None, {"village": "none"}
    vx, vz, vd = map(int, v.groups())
    out["village"] = (vx, vz, vd)
    total = vd * 0.25
    for name, cmd, weight in [("ice_spikes", "locate biome minecraft:ice_spikes", 1.0),
                              ("frozen_peaks", "locate biome minecraft:frozen_peaks", 0.8),
                              ("snowy_taiga", "locate biome minecraft:snowy_taiga", 1.0),
                              ("igloo", "locate structure minecraft:igloo", 0.5)]:
        m = LOC.search(r.c(f"execute in minecraft:overworld positioned {vx} 80 {vz} run {cmd}"))
        d = int(m.group(3)) if m else 4000
        out[name] = d
        total += d * weight
    return round(total), out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    seeds = [random.randint(-2**62, 2**62) for _ in range(n)]
    results = []
    for seed in seeds:
        shutil.rmtree(os.path.join(SERVER, "seedtest"), ignore_errors=True)
        os.makedirs(os.path.join(SERVER, "seedtest"))
        setprops(**{"level-name": "seedtest", "level-seed": str(seed)})
        sysd("start", "sts26.service")
        try:
            r = wait_rcon()
            s, detail = score(r)
        except Exception as e:  # noqa: BLE001
            s, detail = None, {"error": str(e)}
        sysd("stop", "sts26.service")
        print(f"seed {seed}: score {s} {detail}", flush=True)
        if s is not None:
            results.append((s, seed, detail))
    shutil.rmtree(os.path.join(SERVER, "seedtest"), ignore_errors=True)
    results.sort()
    print("BEST", results[0] if results else None)


if __name__ == "__main__":
    main()
