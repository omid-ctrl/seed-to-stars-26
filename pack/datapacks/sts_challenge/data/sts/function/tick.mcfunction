execute as @a[scores={sts.placed=1..}] at @s run function sts:place/start
scoreboard players add #t sts.tmp 1
execute if score #t sts.tmp matches 20.. run function sts:second
