scoreboard players set #t sts.tmp 0
execute as @e[type=minecraft:marker,tag=sts.silo] at @s run function sts:silo/process
execute as @e[type=minecraft:marker,tag=sts.vault] at @s run function sts:vault/process
function sts:ui/update
execute as @a[scores={sts_status=1..}] run function sts:ui/status
execute as @a[scores={sts_bars=1..}] run function sts:ui/toggle_bars
execute as @a[scores={sts_bosses=1..}] run function sts:ui/bosses
function sts:ui/objectives
scoreboard players enable @a sts_status
scoreboard players enable @a sts_bars
scoreboard players enable @a sts_bosses
