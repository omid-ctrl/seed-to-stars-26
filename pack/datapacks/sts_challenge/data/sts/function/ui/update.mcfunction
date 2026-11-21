execute store result bossbar sts:crops max run scoreboard players get #g.crops sts.data
execute store result bossbar sts:crops value run scoreboard players get #crops sts.data
bossbar set sts:crops name [{"text":"Harvest Silo  ","color":"gold"},{"score":{"name":"#crops","objective":"sts.data"},"color":"white"},{"text":" / ","color":"gray"},{"score":{"name":"#g.crops","objective":"sts.data"},"color":"gray"},{"text":" crops","color":"gray"}]
scoreboard players set #vp sts.tmp 0
scoreboard players set #vdone sts.tmp 0
scoreboard players operation #p sts.tmp = #v.diamond_block sts.data
execute if score #p sts.tmp > #g.diamond_block sts.data run scoreboard players operation #p sts.tmp = #g.diamond_block sts.data
scoreboard players operation #p sts.tmp *= #thousand sts.data
scoreboard players operation #p sts.tmp /= #g.diamond_block sts.data
scoreboard players operation #vp sts.tmp += #p sts.tmp
execute if score #v.diamond_block sts.data >= #g.diamond_block sts.data run scoreboard players add #vdone sts.tmp 1
execute if score #v.diamond_block sts.data >= #g.diamond_block sts.data run advancement grant @a only sts:guide/vault_diamond_block
scoreboard players operation #p sts.tmp = #v.emerald_block sts.data
execute if score #p sts.tmp > #g.emerald_block sts.data run scoreboard players operation #p sts.tmp = #g.emerald_block sts.data
scoreboard players operation #p sts.tmp *= #thousand sts.data
scoreboard players operation #p sts.tmp /= #g.emerald_block sts.data
scoreboard players operation #vp sts.tmp += #p sts.tmp
execute if score #v.emerald_block sts.data >= #g.emerald_block sts.data run scoreboard players add #vdone sts.tmp 1
execute if score #v.emerald_block sts.data >= #g.emerald_block sts.data run advancement grant @a only sts:guide/vault_emerald_block
scoreboard players operation #p sts.tmp = #v.iron_block sts.data
execute if score #p sts.tmp > #g.iron_block sts.data run scoreboard players operation #p sts.tmp = #g.iron_block sts.data
scoreboard players operation #p sts.tmp *= #thousand sts.data
scoreboard players operation #p sts.tmp /= #g.iron_block sts.data
scoreboard players operation #vp sts.tmp += #p sts.tmp
execute if score #v.iron_block sts.data >= #g.iron_block sts.data run scoreboard players add #vdone sts.tmp 1
execute if score #v.iron_block sts.data >= #g.iron_block sts.data run advancement grant @a only sts:guide/vault_iron_block
scoreboard players operation #p sts.tmp = #v.gold_block sts.data
execute if score #p sts.tmp > #g.gold_block sts.data run scoreboard players operation #p sts.tmp = #g.gold_block sts.data
scoreboard players operation #p sts.tmp *= #thousand sts.data
scoreboard players operation #p sts.tmp /= #g.gold_block sts.data
scoreboard players operation #vp sts.tmp += #p sts.tmp
execute if score #v.gold_block sts.data >= #g.gold_block sts.data run scoreboard players add #vdone sts.tmp 1
execute if score #v.gold_block sts.data >= #g.gold_block sts.data run advancement grant @a only sts:guide/vault_gold_block
scoreboard players operation #p sts.tmp = #v.copper_block sts.data
execute if score #p sts.tmp > #g.copper_block sts.data run scoreboard players operation #p sts.tmp = #g.copper_block sts.data
scoreboard players operation #p sts.tmp *= #thousand sts.data
scoreboard players operation #p sts.tmp /= #g.copper_block sts.data
scoreboard players operation #vp sts.tmp += #p sts.tmp
execute if score #v.copper_block sts.data >= #g.copper_block sts.data run scoreboard players add #vdone sts.tmp 1
execute if score #v.copper_block sts.data >= #g.copper_block sts.data run advancement grant @a only sts:guide/vault_copper_block
scoreboard players operation #p sts.tmp = #v.redstone_block sts.data
execute if score #p sts.tmp > #g.redstone_block sts.data run scoreboard players operation #p sts.tmp = #g.redstone_block sts.data
scoreboard players operation #p sts.tmp *= #thousand sts.data
scoreboard players operation #p sts.tmp /= #g.redstone_block sts.data
scoreboard players operation #vp sts.tmp += #p sts.tmp
execute if score #v.redstone_block sts.data >= #g.redstone_block sts.data run scoreboard players add #vdone sts.tmp 1
execute if score #v.redstone_block sts.data >= #g.redstone_block sts.data run advancement grant @a only sts:guide/vault_redstone_block
scoreboard players operation #p sts.tmp = #v.lapis_block sts.data
execute if score #p sts.tmp > #g.lapis_block sts.data run scoreboard players operation #p sts.tmp = #g.lapis_block sts.data
scoreboard players operation #p sts.tmp *= #thousand sts.data
scoreboard players operation #p sts.tmp /= #g.lapis_block sts.data
scoreboard players operation #vp sts.tmp += #p sts.tmp
execute if score #v.lapis_block sts.data >= #g.lapis_block sts.data run scoreboard players add #vdone sts.tmp 1
execute if score #v.lapis_block sts.data >= #g.lapis_block sts.data run advancement grant @a only sts:guide/vault_lapis_block
scoreboard players operation #p sts.tmp = #v.netherite_block sts.data
execute if score #p sts.tmp > #g.netherite_block sts.data run scoreboard players operation #p sts.tmp = #g.netherite_block sts.data
scoreboard players operation #p sts.tmp *= #thousand sts.data
scoreboard players operation #p sts.tmp /= #g.netherite_block sts.data
scoreboard players operation #vp sts.tmp += #p sts.tmp
execute if score #v.netherite_block sts.data >= #g.netherite_block sts.data run scoreboard players add #vdone sts.tmp 1
execute if score #v.netherite_block sts.data >= #g.netherite_block sts.data run advancement grant @a only sts:guide/vault_netherite_block
execute store result bossbar sts:vault value run scoreboard players get #vp sts.tmp
bossbar set sts:vault name [{"text":"Great Vault  ","color":"aqua"},{"score":{"name":"#vdone","objective":"sts.tmp"},"color":"white"},{"text":" / 8 ore blocks complete","color":"gray"}]
execute if score #vdone sts.tmp matches 8.. run advancement grant @a only sts:guide/great_vault
execute if score #crops sts.data matches 1000.. run advancement grant @a only sts:guide/crops_1k
execute if score #crops sts.data matches 10000.. run advancement grant @a only sts:guide/crops_10k
execute if score #crops sts.data matches 100000.. run advancement grant @a only sts:guide/crops_100k
execute if score #crops sts.data matches 500000.. run advancement grant @a only sts:guide/crops_500k
execute if score #crops sts.data matches 1000000.. run advancement grant @a only sts:guide/crops_1m
execute as @a[advancements={sts:guide/crops_1m=true,sts:guide/great_vault=true,sts:bosses/dragon=true,sts:bosses/wither=true,sts:guide/stars=false}] run function sts:ui/stars
bossbar set sts:crops players @a[tag=!sts.nobars]
bossbar set sts:vault players @a[tag=!sts.nobars]
