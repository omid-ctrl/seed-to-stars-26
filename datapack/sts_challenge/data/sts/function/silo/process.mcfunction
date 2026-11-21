execute unless block ~ ~ ~ minecraft:barrel{components:{"minecraft:custom_data":{sts:"silo"}}} run return run kill @s
execute store result score #n1 sts.tmp if items block ~ ~ ~ container.* #sts:crops_1
execute store result score #n9 sts.tmp if items block ~ ~ ~ container.* #sts:crops_9
execute if score #n1 sts.tmp matches 0 if score #n9 sts.tmp matches 0 run return 0
scoreboard players operation #n9 sts.tmp *= #nine sts.data
scoreboard players operation #crops sts.data += #n1 sts.tmp
scoreboard players operation #crops sts.data += #n9 sts.tmp
function sts:silo/clear
particle minecraft:happy_villager ~ ~0.7 ~ 0.3 0.2 0.3 0 4
