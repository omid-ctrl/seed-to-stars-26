#!/usr/bin/env python3
"""Write the packwiz pack in pack/ from the working Prism instance (one-time import; after this, edit pack/ with packwiz).

Every jar/zip in mods/, resourcepacks/ and shaderpacks/ is matched to its exact Modrinth version by sha1 and gets a
.pw.toml metafile. Croptopia and EpheroLib (CurseForge only for 26.3) get CurseForge metafiles. Our own jar (sts_keys)
and the challenge datapack are copied in as files. Disabled jars are skipped. Run `packwiz refresh` in pack/ afterwards.
"""
import hashlib
import json
import shutil
import urllib.request
from pathlib import Path

INSTANCE = Path.home() / "Library/Application Support/PrismLauncher/instances/Seed to Stars 26.3/.minecraft"
ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT / "pack"
UA = {"User-Agent": "seed-to-stars-26/1.0 (packwiz import)", "Content-Type": "application/json"}
CURSEFORGE = {  # filename -> (project id, file id, display name)
    "croptopia-fabric-26.3-4.3.2.jar": (415438, 9413830, "Croptopia"),
    "epherolib-fabric-26.3-1.3.0.jar": (885449, 8913898, "EpheroLib"),
}
OWN = {"sts_keys-1.0.0.jar"}


def api(path, body=None):
    req = urllib.request.Request("https://api.modrinth.com/v2/" + path, headers=UA,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 method="POST" if body is not None else "GET")
    return json.load(urllib.request.urlopen(req))


def toml_str(s):
    return json.dumps(s, ensure_ascii=False)


def side_of(project):
    c, s = project["client_side"], project["server_side"]
    if s == "unsupported":
        return "client"
    # "server-only" mods still run in single-player (the integrated server), so players need them too.
    return "both"


def main():
    files = [(folder, f) for folder in ("mods", "resourcepacks", "shaderpacks")
             for f in sorted((INSTANCE / folder).iterdir()) if f.is_file() and f.suffix in (".jar", ".zip")]
    sha1 = {f: hashlib.sha1(f.read_bytes()).hexdigest() for _, f in files}
    known = api("version_files", {"hashes": list(sha1.values()), "algorithm": "sha1"})
    pids = sorted({v["project_id"] for v in known.values()})
    projects = {p["id"]: p for p in api("projects?ids=" + urllib.request.quote(json.dumps(pids)))}
    for folder in ("mods", "resourcepacks", "shaderpacks", "datapacks"):
        shutil.rmtree(PACK / folder, ignore_errors=True)
        (PACK / folder).mkdir(parents=True)
    done, skipped = 0, []
    for folder, f in files:
        h = sha1[f]
        if f.name in OWN:
            shutil.copy(f, PACK / folder / f.name)
            continue
        if f.name in CURSEFORGE:
            pid, fid, name = CURSEFORGE[f.name]
            meta = (f'name = {toml_str(name)}\nfilename = {toml_str(f.name)}\nside = "both"\n\n[download]\n'
                    f'hash-format = "sha1"\nhash = "{h}"\nmode = "metadata:curseforge"\n\n'
                    f'[update]\n[update.curseforge]\nfile-id = {fid}\nproject-id = {pid}\n')
        elif h in known:
            v = known[h]
            p = projects[v["project_id"]]
            fm = next(x for x in v["files"] if x["hashes"]["sha1"] == h)
            side = side_of(p) if folder == "mods" else "client"
            meta = (f'name = {toml_str(p["title"])}\nfilename = {toml_str(f.name)}\nside = "{side}"\n\n[download]\n'
                    f'url = {toml_str(fm["url"])}\nhash-format = "sha512"\nhash = "{fm["hashes"]["sha512"]}"\n\n'
                    f'[update]\n[update.modrinth]\nmod-id = "{p["id"]}"\nversion = "{v["id"]}"\n')
            slug = p["slug"]
        else:
            skipped.append(f.name)
            continue
        slug = (CURSEFORGE[f.name][2].lower() if f.name in CURSEFORGE else slug)
        (PACK / folder / f"{slug}.pw.toml").write_text(meta, encoding="utf-8")
        done += 1
    dp = ROOT / "datapack" / "sts_challenge"
    shutil.copytree(dp, PACK / "datapacks" / "sts_challenge")
    print(f"metafiles: {done}, own files: {sorted(OWN)}, skipped (no source found): {skipped}")


if __name__ == "__main__":
    main()
