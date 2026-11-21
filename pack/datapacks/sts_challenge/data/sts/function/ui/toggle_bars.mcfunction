scoreboard players set @s sts_bars 0
execute if entity @s[tag=sts.nobars] run title @s actionbar {"text":"Goal bars shown","color":"gold"}
execute if entity @s[tag=sts.nobars] run return run tag @s remove sts.nobars
title @s actionbar {"text":"Goal bars hidden (press ; to show)","color":"gray"}
tag @s add sts.nobars
