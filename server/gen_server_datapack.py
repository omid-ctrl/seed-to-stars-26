#!/usr/bin/env python3
"""Generate sts_server: the op-only world switcher for the Seed to Stars 26.3 server on deemo.

Ops type /function sts_server:world/list (clickable list), pick a world, and a 30 s countdown runs. When it ends the
server itself says "STSWORLD|switch|<key>"; sts26_worlds.py sees that log line, backs up the old world and restarts
the server on the new one. Only the server can produce "[Server] ..." in the log (chat is "<name> ..."), and only ops
can run /function, so nobody else can trigger a switch.
"""
import json
import shutil
from pathlib import Path

WORLDS = [("crash", "The Crash (Island)"), ("winter", "Eternal Winter (Snow)"), ("islands", "Tiny Islands (Ocean)"),
          ("wasteland", "Wasteland (Desert)"), ("amplified", "Amplified Snow (fresh world)"),
          ("standard", "Standard BOP, snow start (fresh world)")]
OUT = Path(__file__).resolve().parent / "datapack" / "sts_server"


def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text if isinstance(text, str) else json.dumps(text, indent=2) + "\n", encoding="utf-8")


def fn(name, lines):
    write(f"data/sts_server/function/{name}.mcfunction", "\n".join(lines) + "\n")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    write("pack.mcmeta", {"pack": {"description": "Seed to Stars 26.3 server: world switcher", "min_format": 121,
                                   "max_format": 121}})
    lst = ['tellraw @s {"text":"== Worlds on this server ==","color":"gold","bold":true}',
           'tellraw @s [{"text":"Now playing: ","color":"gray"},{"nbt":"current","storage":"sts_server:world","color":"white"}]']
    for key, name in WORLDS:
        lst.append('tellraw @s [{"text":" > ","color":"dark_gray"},{"text":%s,"color":"aqua","underlined":true,'
                   '"click_event":{"action":"run_command","command":"/function sts_server:world/go/%s"},'
                   '"hover_event":{"action":"show_text","value":"Switch to %s (30 second countdown)"}}]'
                   % (json.dumps(name), key, name))
    lst.append('tellraw @s {"text":"Click a world to switch. /function sts_server:world/cancel stops a countdown.","color":"dark_gray"}')
    fn("world/list", lst)
    clear = [f"schedule clear sts_server:world/do/{k}" for k, _ in WORLDS] + ["schedule clear sts_server:world/warn"]
    for key, name in WORLDS:
        fn(f"world/go/{key}", clear + [
            'tellraw @a [{"text":"[World] ","color":"gold"},{"text":"Switching to %s in 30 seconds. Everyone is '
            'disconnected; rejoin in about a minute.","color":"yellow"}]' % name,
            "playsound minecraft:block.note_block.bell master @a ~ ~ ~ 1 0.8",
            "schedule function sts_server:world/warn 20s replace",
            f"schedule function sts_server:world/do/{key} 30s replace"])
        fn(f"world/do/{key}", [f"say STSWORLD|switch|{key}"])
    fn("world/warn", ['tellraw @a [{"text":"[World] ","color":"gold"},{"text":"Switching in 10 seconds...","color":"yellow"}]'])
    fn("world/cancel", clear + ['tellraw @a [{"text":"[World] ","color":"gold"},{"text":"World switch cancelled.","color":"gray"}]'])
    print("wrote", sum(1 for p in OUT.rglob("*") if p.is_file()), "files to", OUT)


if __name__ == "__main__":
    main()
