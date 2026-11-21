summon minecraft:marker ~ ~ ~ {Tags:["sts.silo"]}
tellraw @s [{"text":"Harvest Silo ready. ","color":"gold"},{"text":"Feed it crops by hand, hopper or belt.","color":"gray"}]
playsound minecraft:block.composter.ready block @s ~ ~ ~ 1 1
particle minecraft:happy_villager ~ ~0.6 ~ 0.4 0.3 0.4 0 20
