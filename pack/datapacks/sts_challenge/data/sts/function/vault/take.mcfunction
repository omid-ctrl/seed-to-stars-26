$execute if score #v.$(item) sts.data >= #g.$(item) sts.data run return 0
$execute store result score #n sts.tmp if items block ~ ~ ~ container.* minecraft:$(item)
execute if score #n sts.tmp matches 0 run return 0
$scoreboard players operation #v.$(item) sts.data += #n sts.tmp
$function sts:vault/clear {item:"$(item)"}
particle minecraft:end_rod ~ ~0.7 ~ 0.3 0.2 0.3 0.01 4
