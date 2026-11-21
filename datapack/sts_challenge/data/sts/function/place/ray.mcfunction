execute if block ~ ~ ~ minecraft:barrel{components:{"minecraft:custom_data":{sts:"silo"}}} align xyz positioned ~.5 ~.5 ~.5 unless entity @e[type=minecraft:marker,tag=sts.silo,distance=..0.6] run return run function sts:place/new_silo
execute if block ~ ~ ~ minecraft:barrel{components:{"minecraft:custom_data":{sts:"vault"}}} align xyz positioned ~.5 ~.5 ~.5 unless entity @e[type=minecraft:marker,tag=sts.vault,distance=..0.6] run return run function sts:place/new_vault
scoreboard players remove #ray sts.tmp 1
execute if score #ray sts.tmp matches 1.. positioned ^ ^ ^0.1 run function sts:place/ray
