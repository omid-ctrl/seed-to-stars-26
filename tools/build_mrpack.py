#!/usr/bin/env python3
"""Build dist/SeedToStars-26.3.mrpack from the Prism instance: every Modrinth file by hash, the rest as overrides.

Mods, resource packs and shader packs that Modrinth knows (looked up by sha1) become download entries; anything else
in mods/ (the custom sts_keys jar) goes into overrides. Also ships the challenge datapack (loaded into every new world
by Global Packs), the Vitrail shader choice, starting video settings and the deemo server in the multiplayer list.
"""
import hashlib
import os
import json
import struct
import sys
import urllib.request
import zipfile
from pathlib import Path

INSTANCE = Path.home() / "Library/Application Support/PrismLauncher/instances/Seed to Stars 26.3/.minecraft"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "SeedToStars-26.3.mrpack"
SERVER = (os.environ.get("STS_SERVER_NAME", "Seed to Stars 26.3"), os.environ.get("STS_SERVER_ADDRESS", ""))  # set to pre-add a server
UA = {"User-Agent": "modpack-check/1.0", "Content-Type": "application/json"}
CLIENT_ONLY = ("sodium", "iris", "vitrail", "immersive-storms", "yacl", "sts_keys", "modmenu", "entityculling",
               "moreculling", "immediatelyfast", "macos", "dynamic-fps", "lambdynamiclights", "particlerain",
               "subtle", "ambientsounds", "xaero", "betteradvancements", "advancementplaques", "iceberg", "badoptim",
               "controlling", "searchables", "mousetweaks", "shulkerboxtooltip", "enchdesc", "language-reload",
               "fastquit", "entity_model_features", "entity_texture_features", "fusion", "sodium-extra")


def nbt_servers(entries):
    """servers.dat: an uncompressed NBT compound {servers:[{name,ip}]}."""
    def s(name, value):
        nb, vb = name.encode(), value.encode()
        return b"\x08" + struct.pack(">H", len(nb)) + nb + struct.pack(">H", len(vb)) + vb
    body = b"".join(s("name", n) + s("ip", ip) + b"\x00" for n, ip in entries)
    lst = b"\x09" + struct.pack(">H", 7) + b"servers" + b"\x0a" + struct.pack(">i", len(entries)) + body
    return b"\x0a" + struct.pack(">H", 0) + lst + b"\x00"


def main():
    candidates = []
    for folder in ("mods", "resourcepacks", "shaderpacks"):
        for f in sorted((INSTANCE / folder).iterdir()):
            if f.is_file() and f.suffix in (".jar", ".zip"):
                candidates.append((folder, f))
    sha1 = {str(f): hashlib.sha1(f.read_bytes()).hexdigest() for _, f in candidates}
    req = urllib.request.Request("https://api.modrinth.com/v2/version_files", headers=UA, method="POST",
                                 data=json.dumps({"hashes": list(sha1.values()), "algorithm": "sha1"}).encode())
    known = json.load(urllib.request.urlopen(req))
    files, overrides = [], []
    for folder, f in candidates:
        h = sha1[str(f)]
        ver = known.get(h)
        if not ver:
            overrides.append((folder, f))
            continue
        meta = next(x for x in ver["files"] if x["hashes"]["sha1"] == h)
        low = f.name.lower()
        client_only = folder != "mods" or any(k in low for k in CLIENT_ONLY)
        files.append({"path": f"{folder}/{f.name}", "hashes": {"sha1": h, "sha512": meta["hashes"]["sha512"]},
                      "env": {"client": "required", "server": "unsupported" if client_only else "required"},
                      "downloads": [meta["url"]], "fileSize": meta["size"]})
    index = {"formatVersion": 1, "game": "minecraft", "versionId": "1.0.0", "name": "Seed to Stars 26.3",
             "summary": "Vanilla-plus on 26.3: Create, farming, quarries, the Harvest Silo and Great Vault goals.",
             "files": files, "dependencies": {"minecraft": "26.3", "fabric-loader": "0.20.1"}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    options = "\n".join(['preferredGraphicsBackend:"vulkan"', "renderDistance:12", "simulationDistance:10",
                         'resourcePacks:["vanilla","file/Fancy Crops v1.4.zip","file/FreshAnimations_v1.11.2_26.1+.zip"]',
                         "guiScale:3"]) + "\n"
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("modrinth.index.json", json.dumps(index, indent=1))
        for folder, f in overrides:
            z.write(f, f"overrides/{folder}/{f.name}")
        dp = ROOT / "datapack" / "sts_challenge"
        for p in sorted(dp.rglob("*")):
            if p.is_file():
                z.write(p, "overrides/datapacks/sts_challenge/" + str(p.relative_to(dp)))
        z.writestr("overrides/vitrail/pack.txt", (INSTANCE / "vitrail" / "pack.txt").read_text().replace(
            "enabled=true", "enabled=false"))
        z.writestr("overrides/options.txt", options)
        if SERVER[1]:
            z.writestr("overrides/servers.dat", nbt_servers([SERVER]))
    print(f"{OUT}: {len(files)} Modrinth downloads, overrides: {[f.name for _, f in overrides]}, "
          f"{OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    sys.exit(main())
