#!/usr/bin/env python3
"""Generate the Seed to Stars 26.3 challenge datapack (sts_challenge).

Harvest Silo (1,000,000 crops) and Great Vault (ore blocks), boss bars,
/trigger commands and a light guide tab in the Advancements screen.
Minecraft Java 26.3 (data pack format 121). Run: python3 tools/gen_datapack.py
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "datapack" / "sts_challenge"
NS = OUT / "data" / "sts"

CROP_GOAL = 1_000_000
CROP_MILESTONES = [(1_000, "1k", "First Thousand", "task"), (10_000, "10k", "Ten Thousand", "task"),
                   (100_000, "100k", "Breadbasket", "goal"), (500_000, "500k", "Half a Million", "goal"),
                   (1_000_000, "1m", "A Million Harvests", "challenge")]
# item, goal, display name, icon
VAULT = [("diamond_block", 64, "Diamond"), ("emerald_block", 32, "Emerald"), ("iron_block", 512, "Iron"),
         ("gold_block", 256, "Gold"), ("copper_block", 256, "Copper"), ("redstone_block", 128, "Redstone"),
         ("lapis_block", 128, "Lapis"), ("netherite_block", 4, "Netherite")]

# Whole crops count 1. Seeds, cut or chopped pieces and meals do not count.
CROPS_1 = ["minecraft:" + i for i in ["wheat", "carrot", "potato", "beetroot", "melon_slice", "pumpkin", "sugar_cane",
                                      "cactus", "cocoa_beans", "nether_wart", "sweet_berries", "glow_berries"]]
CROPS_1_MOD = ["farmersdelight:cabbage", "farmersdelight:onion", "farmersdelight:tomato", "farmersdelight:rice_panicle",
               "culturaldelights:corn_cob", "culturaldelights:cucumber", "culturaldelights:eggplant",
               "culturaldelights:white_eggplant", "culturaldelights:avocado",
               "rusticdelight:cotton_boll", "rusticdelight:coffee_beans",
               "ubesdelight:ube", "ubesdelight:garlic", "ubesdelight:ginger", "ubesdelight:lemongrass"]
PEPPERS = ["green", "yellow", "red", "orange", "white", "pink", "blue", "purple", "black"]
CROPS_1_MOD += [f"rusticdelight:bell_pepper_{c}" for c in PEPPERS]
# Croptopia 4.3.2: every item in its c:crops/* tags (crops and tree fruit; seeds and saplings are separate items).
CROPTOPIA = """almond apricot artichoke asparagus avocado banana barley basil bellpepper blackbean blackberry blueberry
broccoli cabbage cantaloupe cashew cauliflower celery cherry chile_pepper cinnamon coconut coffee_beans corn cranberry
cucumber currant date dragonfruit eggplant elderberry fig garlic ginger grape grapefruit greenbean greenonion honeydew
hops kale kiwi kumquat leek lemon lettuce lime mango mustard nectarine nutmeg oat olive onion orange peach peanut pear
pecan pepper persimmon pineapple plum radish raspberry rhubarb rice rutabaga saguaro soybean spinach squash starfruit
strawberry sweetpotato tea_leaves tomatillo tomato turmeric turnip""".split()
CROPS_1_MOD += [f"croptopia:{c}" for c in CROPTOPIA]
# Packed storage counts 9 (every recipe checked: 9 of the crop above).
CROPS_9 = ["minecraft:hay_block", "minecraft:melon", "minecraft:nether_wart_block"]
CROPS_9_MOD = ["farmersdelight:carrot_crate", "farmersdelight:potato_crate", "farmersdelight:beetroot_crate",
               "farmersdelight:cabbage_crate", "farmersdelight:onion_crate", "farmersdelight:tomato_crate",
               "farmersdelight:rice_bale", "culturaldelights:avocado_crate", "culturaldelights:corn_cob_crate",
               "culturaldelights:cucumber_crate", "culturaldelights:eggplant_crate",
               "culturaldelights:white_eggplant_crate", "rusticdelight:cotton_boll_crate",
               "rusticdelight:coffee_beans_bag", "ubesdelight:garlic_crate", "ubesdelight:ginger_crate",
               "ubesdelight:lemongrass_crate", "ubesdelight:ube_crate"]
CROPS_9_MOD += [f"rusticdelight:bell_pepper_{c}_crate" for c in PEPPERS]

# (key, how it is earned, target, icon, title, frame, hint). Icons are vanilla items so a missing mod never breaks a row.
BOSSES = [
    ("dragon", "kill", "minecraft:ender_dragon", "minecraft:dragon_head", "Ender Dragon", "challenge",
     "The End: break the End Crystals on the pillars, then the dragon."),
    ("wither", "kill", "minecraft:wither", "minecraft:wither_skeleton_skull", "The Wither", "challenge",
     "Summon it: 4 soul sand in a T, 3 wither skeleton skulls on top. Fight it underground."),
    ("elder", "kill", "minecraft:elder_guardian", "minecraft:prismarine_shard", "Elder Guardian", "goal",
     "Ocean Monuments hold three. Water Breathing, and milk for Mining Fatigue."),
    ("warden", "kill", "minecraft:warden", "minecraft:sculk_shrieker", "The Warden", "challenge",
     "Ancient Cities in the Deep Dark. Stay quiet; it hunts by sound."),
    ("wildfire", "kill", "friendsandfoes:wildfire", "minecraft:fire_charge", "Wildfire", "goal",
     "Friends & Foes boss of the Nether. Break its shields first; it drops a crown."),
    ("iceologer", "kill", "friendsandfoes:iceologer", "minecraft:blue_ice", "Iceologer", "goal",
     "Friends & Foes: an illager that hurls ice."),
    ("illusioner", "kill", "friendsandfoes:illusioner", "minecraft:spyglass", "Illusioner", "goal",
     "Friends & Foes: an illager that hides among copies of itself."),
    ("mutant_zombie", "kill", "mutantmonsters:mutant_zombie", "minecraft:zombie_head", "Mutant Zombie", "goal",
     "Rare night spawn, or splash Chemical X on a zombie."),
    ("mutant_skeleton", "kill", "mutantmonsters:mutant_skeleton", "minecraft:skeleton_skull", "Mutant Skeleton", "goal",
     "Rare night spawn, or splash Chemical X on a skeleton."),
    ("mutant_creeper", "kill", "mutantmonsters:mutant_creeper", "minecraft:creeper_head", "Mutant Creeper", "goal",
     "Rare night spawn, or splash Chemical X on a creeper."),
    ("mutant_enderman", "kill", "mutantmonsters:mutant_enderman", "minecraft:ender_eye", "Mutant Enderman", "goal",
     "Rare spawn, or splash Chemical X on an enderman."),
]
OBJECTIVES = [
    ("raid", "vanilla", "minecraft:adventure/hero_of_the_village", "minecraft:bell", "Win a Raid", "goal",
     "Drink an Ominous Bottle near a village and beat every wave."),
    ("evoker", "kill", "minecraft:evoker", "minecraft:totem_of_undying", "Evoker", "goal",
     "Woodland Mansions and raids. Drops a Totem of Undying."),
    ("trial", "vanilla", "minecraft:adventure/minecraft_trials_edition", "minecraft:trial_key", "Trial Chambers", "task",
     "Find a Trial Chamber underground and step inside."),
    ("ominous_vault", "vanilla", "minecraft:adventure/revaulting", "minecraft:ominous_trial_key", "Ominous Vault", "goal",
     "Open an Ominous Vault with an Ominous Trial Key. The Heavy Core makes a Mace."),
    ("elytra", "has", "minecraft:elytra", "minecraft:elytra", "Wings of the End", "goal",
     "End Cities, through the gateway that opens after the dragon."),
]

SILO_DATA = '{sts:"silo"}'
VAULT_DATA = '{sts:"vault"}'
SLOTS = range(27)  # a barrel


def write(rel, content):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, (dict, list)):
        content = json.dumps(content, indent=2, ensure_ascii=False) + "\n"
    p.write_text(content, encoding="utf-8")


def fn(name, lines):
    write(f"data/sts/function/{name}.mcfunction", "\n".join(lines) + "\n")


def tag(values):
    return {"values": [v if v.startswith("minecraft:") or v.startswith("#") else {"id": v, "required": False}
                       for v in values]}


def text(s, color=None, **kw):
    c = {"text": s}
    if color:
        c["color"] = color
    c.update(kw)
    return c


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    write("pack.mcmeta", {"pack": {"description": "Seed to Stars 26.3: Harvest Silo, Great Vault and the guide tab",
                                   "min_format": 121, "max_format": 121}})
    write("data/minecraft/tags/function/load.json", {"values": ["sts:load"]})
    write("data/minecraft/tags/function/tick.json", {"values": ["sts:tick"]})
    write("data/sts/tags/item/crops_1.json", tag(CROPS_1 + CROPS_1_MOD))
    write("data/sts/tags/item/crops_9.json", tag(CROPS_9 + CROPS_9_MOD))
    write("data/sts/tags/item/crops_any.json", {"values": ["#sts:crops_1", "#sts:crops_9"]})

    # Recipes: the Silo is early game, the Vault needs a diamond pickaxe (obsidian) and 36 iron.
    lore_silo = [text("Feed it crops: by hand, hopper or belt.", "gray", italic=False),
                 text("Hay bales and crates count as 9.", "gray", italic=False)]
    lore_vault = [text("Feed it ore blocks for the Great Vault.", "gray", italic=False),
                  text("/trigger sts_status shows what is still needed.", "gray", italic=False)]
    write("data/sts/recipe/harvest_silo.json", {
        "type": "minecraft:crafting_shaped", "category": "misc",
        "key": {"H": "minecraft:hay_block", "B": "minecraft:barrel"}, "pattern": ["HHH", "HBH", "HHH"],
        "result": {"id": "minecraft:barrel", "components": {
            "minecraft:custom_name": text("Harvest Silo", "gold", italic=False),
            "minecraft:custom_data": SILO_DATA, "minecraft:lore": lore_silo,
            "minecraft:enchantment_glint_override": True}}})
    write("data/sts/recipe/ore_vault.json", {
        "type": "minecraft:crafting_shaped", "category": "misc",
        "key": {"I": "minecraft:iron_block", "O": "minecraft:obsidian", "B": "minecraft:barrel"},
        "pattern": ["IOI", "OBO", "IOI"],
        "result": {"id": "minecraft:barrel", "components": {
            "minecraft:custom_name": text("Ore Vault", "aqua", italic=False),
            "minecraft:custom_data": VAULT_DATA, "minecraft:lore": lore_vault,
            "minecraft:enchantment_glint_override": True}}})

    # ---- functions ----
    load = ["scoreboard objectives add sts.data dummy", "scoreboard objectives add sts.tmp dummy",
            "scoreboard objectives add sts.placed minecraft.used:minecraft.barrel",
            "scoreboard objectives add sts_status trigger", "scoreboard objectives add sts_bars trigger",
            "scoreboard objectives add sts_bosses trigger",
            # Some premade maps switch limited crafting on, which hides every mod recipe (Create, Farmer's Delight).
            "gamerule limited_crafting false",
            "scoreboard players set #nine sts.data 9", "scoreboard players set #thousand sts.data 1000",
            f"execute unless score #g.crops sts.data matches -2147483648.. run scoreboard players set #g.crops sts.data {CROP_GOAL}",
            "execute unless score #crops sts.data matches -2147483648.. run scoreboard players set #crops sts.data 0"]
    for item, goal, _ in VAULT:
        load.append(f"execute unless score #g.{item} sts.data matches -2147483648.. run scoreboard players set #g.{item} sts.data {goal}")
        load.append(f"execute unless score #v.{item} sts.data matches -2147483648.. run scoreboard players set #v.{item} sts.data 0")
    load += ['bossbar add sts:crops {"text":"Harvest Silo"}', "bossbar set sts:crops color green",
             "bossbar set sts:crops style notched_10",
             'bossbar add sts:vault {"text":"Great Vault"}', "bossbar set sts:vault color blue",
             "bossbar set sts:vault style notched_10", f"bossbar set sts:vault max {len(VAULT) * 1000}",
             "function sts:ui/update"]
    fn("load", load)
    fn("tick", ["execute as @a[scores={sts.placed=1..}] at @s run function sts:place/start",
                "scoreboard players add #t sts.tmp 1",
                "execute if score #t sts.tmp matches 20.. run function sts:second"])
    fn("second", ["scoreboard players set #t sts.tmp 0",
                  "execute as @e[type=minecraft:marker,tag=sts.silo] at @s run function sts:silo/process",
                  "execute as @e[type=minecraft:marker,tag=sts.vault] at @s run function sts:vault/process",
                  "function sts:ui/update",
                  "execute as @a[scores={sts_status=1..}] run function sts:ui/status",
                  "execute as @a[scores={sts_bars=1..}] run function sts:ui/toggle_bars",
                  "execute as @a[scores={sts_bosses=1..}] run function sts:ui/bosses",
                  "function sts:ui/objectives",
                  "scoreboard players enable @a sts_status", "scoreboard players enable @a sts_bars",
                  "scoreboard players enable @a sts_bosses"])

    # Placement: the barrel "used" stat ticks up; ray-cast from the eyes to the barrel just placed.
    fn("place/start", ["scoreboard players set @s sts.placed 0", "scoreboard players set #ray sts.tmp 60",
                       "execute anchored eyes positioned ^ ^ ^ run function sts:place/ray"])
    fn("place/ray", [
        f"execute if block ~ ~ ~ minecraft:barrel{{components:{{\"minecraft:custom_data\":{SILO_DATA}}}}} align xyz positioned ~.5 ~.5 ~.5 unless entity @e[type=minecraft:marker,tag=sts.silo,distance=..0.6] run return run function sts:place/new_silo",
        f"execute if block ~ ~ ~ minecraft:barrel{{components:{{\"minecraft:custom_data\":{VAULT_DATA}}}}} align xyz positioned ~.5 ~.5 ~.5 unless entity @e[type=minecraft:marker,tag=sts.vault,distance=..0.6] run return run function sts:place/new_vault",
        "scoreboard players remove #ray sts.tmp 1",
        "execute if score #ray sts.tmp matches 1.. positioned ^ ^ ^0.1 run function sts:place/ray"])
    fn("place/new_silo", ['summon minecraft:marker ~ ~ ~ {Tags:["sts.silo"]}',
                          'tellraw @s [{"text":"Harvest Silo ready. ","color":"gold"},{"text":"Feed it crops by hand, hopper or belt.","color":"gray"}]',
                          "playsound minecraft:block.composter.ready block @s ~ ~ ~ 1 1",
                          "particle minecraft:happy_villager ~ ~0.6 ~ 0.4 0.3 0.4 0 20"])
    fn("place/new_vault", ['summon minecraft:marker ~ ~ ~ {Tags:["sts.vault"]}',
                           'tellraw @s [{"text":"Ore Vault ready. ","color":"aqua"},{"text":"Feed it ore blocks. /trigger sts_status shows what is still needed.","color":"gray"}]',
                           "playsound minecraft:block.beacon.activate block @s ~ ~ ~ 1 1.4",
                           "particle minecraft:end_rod ~ ~0.6 ~ 0.4 0.3 0.4 0.02 20"])

    fn("silo/process", [
        f"execute unless block ~ ~ ~ minecraft:barrel{{components:{{\"minecraft:custom_data\":{SILO_DATA}}}}} run return run kill @s",
        "execute store result score #n1 sts.tmp if items block ~ ~ ~ container.* #sts:crops_1",
        "execute store result score #n9 sts.tmp if items block ~ ~ ~ container.* #sts:crops_9",
        "execute if score #n1 sts.tmp matches 0 if score #n9 sts.tmp matches 0 run return 0",
        "scoreboard players operation #n9 sts.tmp *= #nine sts.data",
        "scoreboard players operation #crops sts.data += #n1 sts.tmp",
        "scoreboard players operation #crops sts.data += #n9 sts.tmp",
        "function sts:silo/clear",
        "particle minecraft:happy_villager ~ ~0.7 ~ 0.3 0.2 0.3 0 4"])
    fn("silo/clear", [f"execute if items block ~ ~ ~ container.{i} #sts:crops_any run item replace block ~ ~ ~ container.{i} with minecraft:air" for i in SLOTS])

    fn("vault/process", [
        f"execute unless block ~ ~ ~ minecraft:barrel{{components:{{\"minecraft:custom_data\":{VAULT_DATA}}}}} run return run kill @s"]
       + [f'function sts:vault/take {{item:"{item}"}}' for item, _, _ in VAULT])
    fn("vault/take", ["$execute if score #v.$(item) sts.data >= #g.$(item) sts.data run return 0",
                      "$execute store result score #n sts.tmp if items block ~ ~ ~ container.* minecraft:$(item)",
                      "execute if score #n sts.tmp matches 0 run return 0",
                      "$scoreboard players operation #v.$(item) sts.data += #n sts.tmp",
                      '$function sts:vault/clear {item:"$(item)"}',
                      "particle minecraft:end_rod ~ ~0.7 ~ 0.3 0.2 0.3 0.01 4"])
    fn("vault/clear", [f"$execute if items block ~ ~ ~ container.{i} minecraft:$(item) run item replace block ~ ~ ~ container.{i} with minecraft:air" for i in SLOTS])

    # UI: boss bars, milestones, final.
    upd = ["execute store result bossbar sts:crops max run scoreboard players get #g.crops sts.data",
           "execute store result bossbar sts:crops value run scoreboard players get #crops sts.data",
           'bossbar set sts:crops name [{"text":"Harvest Silo  ","color":"gold"},{"score":{"name":"#crops","objective":"sts.data"},"color":"white"},{"text":" / ","color":"gray"},{"score":{"name":"#g.crops","objective":"sts.data"},"color":"gray"},{"text":" crops","color":"gray"}]',
           "scoreboard players set #vp sts.tmp 0", "scoreboard players set #vdone sts.tmp 0"]
    for item, _, _ in VAULT:
        upd += [f"scoreboard players operation #p sts.tmp = #v.{item} sts.data",
                f"execute if score #p sts.tmp > #g.{item} sts.data run scoreboard players operation #p sts.tmp = #g.{item} sts.data",
                "scoreboard players operation #p sts.tmp *= #thousand sts.data",
                f"scoreboard players operation #p sts.tmp /= #g.{item} sts.data",
                "scoreboard players operation #vp sts.tmp += #p sts.tmp",
                f"execute if score #v.{item} sts.data >= #g.{item} sts.data run scoreboard players add #vdone sts.tmp 1",
                f"execute if score #v.{item} sts.data >= #g.{item} sts.data run advancement grant @a only sts:guide/vault_{item}"]
    upd += ["execute store result bossbar sts:vault value run scoreboard players get #vp sts.tmp",
            'bossbar set sts:vault name [{"text":"Great Vault  ","color":"aqua"},{"score":{"name":"#vdone","objective":"sts.tmp"},"color":"white"},{"text":" / %d ore blocks complete","color":"gray"}]' % len(VAULT),
            f"execute if score #vdone sts.tmp matches {len(VAULT)}.. run advancement grant @a only sts:guide/great_vault"]
    for n, key, _, _ in CROP_MILESTONES:
        upd.append(f"execute if score #crops sts.data matches {n}.. run advancement grant @a only sts:guide/crops_{key}")
    upd += ["execute as @a[advancements={sts:guide/crops_1m=true,sts:guide/great_vault=true,sts:bosses/dragon=true,sts:bosses/wither=true,sts:guide/stars=false}] run function sts:ui/stars",
            "bossbar set sts:crops players @a[tag=!sts.nobars]", "bossbar set sts:vault players @a[tag=!sts.nobars]"]
    fn("ui/update", upd)
    fn("ui/stars", ["advancement grant @s only sts:guide/stars",
                    'tellraw @a [{"text":"","color":"gold"},{"selector":"@s"},{"text":" went from Seed to Stars!"}]',
                    "playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 1"])
    status = ["scoreboard players set @s sts_status 0",
              'tellraw @s {"text":"== Seed to Stars ==","color":"gold","bold":true}',
              'tellraw @s [{"text":"Harvest Silo: ","color":"gold"},{"score":{"name":"#crops","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.crops","objective":"sts.data"}},{"text":" crops","color":"gray"}]',
              'tellraw @s {"text":"Great Vault (blocks delivered / needed):","color":"aqua"}']
    for item, _, name in VAULT:
        status.append('tellraw @s [{"text":"  %s: ","color":"gray"},{"score":{"name":"#v.%s","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.%s","objective":"sts.data"}}]' % (name, item, item))
    status.append('tellraw @s {"text":"Keys: ; hides or shows the bars, \' shows this, [ lists bosses (rebind under Controls > Seed to Stars). Or /trigger sts_bars, sts_status, sts_bosses.","color":"dark_gray","italic":true}')
    fn("ui/status", status)
    fn("ui/toggle_bars", ["scoreboard players set @s sts_bars 0",
                          'execute if entity @s[tag=sts.nobars] run title @s actionbar {"text":"Goal bars shown","color":"gold"}',
                          "execute if entity @s[tag=sts.nobars] run return run tag @s remove sts.nobars",
                          'title @s actionbar {"text":"Goal bars hidden (press ; to show)","color":"gray"}',
                          "tag @s add sts.nobars"])

    # ---- guide tab (advancements) ----
    def adv(name, parent, icon, title, desc, criteria, frame="task", hidden=False, toast=True, chat=True,
            background=None, rewards=None, requirements=None):
        d = {"display": {"icon": {"id": icon}, "title": text(title), "description": text(desc),
                         "frame": frame, "show_toast": toast, "announce_to_chat": chat, "hidden": hidden},
             "criteria": criteria}
        if parent:
            d["parent"] = "sts:guide/" + parent
        if background:
            d["display"]["background"] = background
        if rewards:
            d["rewards"] = rewards
        if requirements:
            d["requirements"] = requirements
        write(f"data/sts/advancement/guide/{name}.json", d)

    def has(*items, data=None):
        crit = {}
        for i, it in enumerate(items):
            pred = {"items": it}
            if data:
                pred["predicates"] = {"minecraft:custom_data": data}
            crit[f"has_{i}"] = {"trigger": "minecraft:inventory_changed", "conditions": {"items": [pred]}}
        return crit

    def any_of(crit):
        return [list(crit)]

    def kill(entity):
        return {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": {
            "type": "minecraft:entity_properties", "entity": "this",
            "predicate": {"minecraft:entity_type": entity}}}}}

    def dim(to):
        return {"enter": {"trigger": "minecraft:changed_dimension", "conditions": {"to": to}}}

    impossible = {"done": {"trigger": "minecraft:impossible"}}

    adv("root", None, "minecraft:wheat_seeds", "Seed to Stars",
        "Fill the Harvest Silo with a million crops and the Great Vault with ore blocks, and beat the bosses on the way. /trigger sts_status shows progress.",
        {"joined": {"trigger": "minecraft:tick"}}, toast=False, chat=False,
        background="minecraft:gui/advancements/backgrounds/husbandry",
        rewards={"recipes": ["sts:harvest_silo", "sts:ore_vault"]})
    # Farming
    adv("silo", "root", "minecraft:hay_block", "The Harvest Silo",
        "Craft it: a barrel ringed by 8 hay bales. Place it and feed it crops. Hay bales and crates count as 9.",
        has("minecraft:barrel", data=SILO_DATA))
    prev = "silo"
    for n, key, title, frame in CROP_MILESTONES:
        adv(f"crops_{key}", prev, "minecraft:wheat" if n < 100_000 else "minecraft:hay_block", title,
            f"Deliver {n:,} crops to the Harvest Silo.", impossible, frame=frame)
        prev = f"crops_{key}"
    adv("water_wheel", "silo", "create:water_wheel", "Turning Water",
        "Create runs on rotation from water wheels and windmills. Hold W over any Create item to watch a Ponder scene.",
        has("create:water_wheel", "create:large_water_wheel", "create:windmill_bearing"),
        requirements=[["has_0", "has_1", "has_2"]])
    adv("harvester", "water_wheel", "create:mechanical_harvester", "Iron Farmhands",
        "Mount Mechanical Harvesters on a moving contraption to sweep whole fields, then carry the crops to the Silo with belts and chutes.",
        has("create:mechanical_harvester"))
    adv("belt", "harvester", "create:belt_connector", "On the Belt",
        "A belt into a hopper on the Silo makes the whole farm count itself.", has("create:belt_connector"))
    # Mining
    adv("vault", "root", "minecraft:obsidian", "The Ore Vault",
        "Craft it: a barrel with 4 iron blocks and 4 obsidian. The Great Vault wants " +
        ", ".join(f"{g} {nm.lower()}" for _, g, nm in VAULT) + " blocks.",
        has("minecraft:barrel", data=VAULT_DATA))
    adv("power", "vault", "energizedpower:coal_engine", "Power Up",
        "Energized Power: a Coal Engine burns fuel and Solar Cells drink daylight. Copper cables carry the energy.",
        has("energizedpower:coal_engine", "energizedpower:basic_solar_cell", "energizedpower:heat_generator",
            "energizedpower:thermal_generator"), requirements=[["has_0", "has_1", "has_2", "has_3"]])
    adv("quarry", "power", "quarryplus:quarry", "Strip Mine",
        "Mark an area with Markers, set the Quarry beside them and power it. Enchant it first: Efficiency for speed, Fortune for more ore, Unbreaking to save power.",
        has("quarryplus:quarry"), frame="goal")
    adv("adv_quarry", "quarry", "quarryplus:adv_quarry", "Chunk Destroyer",
        "The Advanced Quarry digs whole chunks down to bedrock.", has("quarryplus:adv_quarry"), frame="goal")
    for item, goal, name in VAULT:
        adv(f"vault_{item}", "vault", f"minecraft:{item}", f"Vault: {name}",
            f"Deliver {goal} {name.lower()} blocks to the Ore Vault.", impossible)
    adv("great_vault", "vault", "minecraft:beacon", "The Great Vault",
        "Every ore block delivered.", impossible, frame="challenge")
    # Bosses
    adv("nether", "root", "minecraft:obsidian", "Into the Fire",
        "Light a Nether portal: 10 obsidian and flint and steel. Fortresses hold blazes and wither skeletons.",
        dim("minecraft:the_nether"))
    adv("blaze", "nether", "minecraft:blaze_rod", "Blaze Rods",
        "Blazes guard Nether Fortresses. Their rods brew potions and make Eyes of Ender.", has("minecraft:blaze_rod"))
    adv("eye", "blaze", "minecraft:ender_eye", "Eyes of Ender",
        "Blaze powder and an ender pearl. Throw one and follow it to the Stronghold.", has("minecraft:ender_eye"))
    adv("end", "eye", "minecraft:end_stone", "The End", "Fill the portal frame and step through. Every boss is in the Bosses & Objectives tab.",
        dim("minecraft:the_end"))
    adv("stars", "end", "minecraft:nether_star", "From Seed to Stars",
        "A million crops, the Great Vault full, the Wither and the Ender Dragon beaten.", impossible,
        frame="challenge")

    # ---- Bosses & Objectives tab: every boss in the pack, one row each, plus the big vanilla objectives ----
    def badv(name, icon, title, desc, criteria, frame):
        d = {"parent": "sts:bosses/root",
             "display": {"icon": {"id": icon}, "title": text(title), "description": text(desc), "frame": frame,
                         "show_toast": True, "announce_to_chat": True, "hidden": False},
             "criteria": criteria}
        write(f"data/sts/advancement/bosses/{name}.json", d)

    write("data/sts/advancement/bosses/root.json", {
        "display": {"icon": {"id": "minecraft:dragon_head"}, "title": text("Bosses & Objectives"),
                    "description": text("Every boss in the pack and the big objectives. Press [ for a checklist in chat."),
                    "frame": "task", "show_toast": False, "announce_to_chat": False, "hidden": False,
                    "background": "minecraft:gui/advancements/backgrounds/end"},
        "criteria": {"joined": {"trigger": "minecraft:tick"}}})
    for key, kind, target, icon, title, frame, hint in BOSSES + OBJECTIVES:
        crit = kill(target) if kind == "kill" else (has(target) if kind == "has" else impossible)
        badv(key, icon, title, hint, crit, frame)
    badv("all_bosses", "minecraft:beacon", "Boss Slayer", "Every boss above defeated.", impossible, "challenge")

    # Vanilla objectives that already have an advancement: mirror them into the tab.
    objectives = [f"execute as @a[advancements={{{src}=true,sts:bosses/{key}=false}}] run advancement grant @s only sts:bosses/{key}"
                  for key, kind, src, *_ in OBJECTIVES if kind == "vanilla"]
    boss_ok = ",".join(f"sts:bosses/{k}=true" for k, *_ in BOSSES)
    objectives.append(f"execute as @a[advancements={{{boss_ok},sts:bosses/all_bosses=false}}] run advancement grant @s only sts:bosses/all_bosses")
    fn("ui/objectives", objectives)

    # Chat checklist (/trigger sts_bosses, or the [ key).
    bl = ["scoreboard players set @s sts_bosses 0", "scoreboard players set #done sts.tmp 0",
          'tellraw @s {"text":"== Bosses ==","color":"red","bold":true}']
    def row(key, title, hint):
        return [f"execute if entity @s[advancements={{sts:bosses/{key}=true}}] run scoreboard players add #done sts.tmp 1",
                f'execute if entity @s[advancements={{sts:bosses/{key}=true}}] run tellraw @s [{{"text":" ✔ ","color":"green"}},{{"text":{json.dumps(title)},"color":"white"}}]',
                f'execute unless entity @s[advancements={{sts:bosses/{key}=true}}] run tellraw @s [{{"text":" ✘ ","color":"red"}},{{"text":{json.dumps(title)},"color":"white"}},{{"text":{json.dumps("  " + hint)},"color":"gray"}}]']
    for key, _, _, _, title, _, hint in BOSSES:
        bl += row(key, title, hint)
    bl.append('tellraw @s {"text":"== Objectives ==","color":"aqua","bold":true}')
    for key, _, _, _, title, _, hint in OBJECTIVES:
        bl += row(key, title, hint)
    total = len(BOSSES) + len(OBJECTIVES)
    bl.append('tellraw @s [{"text":"Done: ","color":"gold"},{"score":{"name":"#done","objective":"sts.tmp"},"color":"white"},{"text":" / %d","color":"white"},{"text":"   Full list: Advancements (L) > Bosses & Objectives","color":"dark_gray"}]' % total)
    fn("ui/bosses", bl)


if __name__ == "__main__":
    build()
    n = sum(1 for p in OUT.rglob("*") if p.is_file())
    print(f"wrote {n} files to {OUT}")
