summon minecraft:marker ~ ~ ~ {Tags:["sts.vault"]}
tellraw @s [{"text":"Ore Vault ready. ","color":"aqua"},{"text":"Feed it ore blocks. /trigger sts_status shows what is still needed.","color":"gray"}]
playsound minecraft:block.beacon.activate block @s ~ ~ ~ 1 1.4
particle minecraft:end_rod ~ ~0.6 ~ 0.4 0.3 0.4 0.02 20
