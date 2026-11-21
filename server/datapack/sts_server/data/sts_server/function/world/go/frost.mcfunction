schedule clear sts_server:world/do/crash
schedule clear sts_server:world/do/winter
schedule clear sts_server:world/do/islands
schedule clear sts_server:world/do/wasteland
schedule clear sts_server:world/do/frost
schedule clear sts_server:world/warn
tellraw @a [{"text":"[World] ","color":"gold"},{"text":"Switching to Frost (hard, snow seed) in 30 seconds. Everyone is disconnected; rejoin in about a minute.","color":"yellow"}]
playsound minecraft:block.note_block.bell master @a ~ ~ ~ 1 0.8
schedule function sts_server:world/warn 20s replace
schedule function sts_server:world/do/frost 30s replace
