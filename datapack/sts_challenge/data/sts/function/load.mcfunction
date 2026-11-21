scoreboard objectives add sts.data dummy
scoreboard objectives add sts.tmp dummy
scoreboard objectives add sts.placed minecraft.used:minecraft.barrel
scoreboard objectives add sts_status trigger
scoreboard objectives add sts_bars trigger
scoreboard objectives add sts_bosses trigger
gamerule limited_crafting false
scoreboard players set #nine sts.data 9
scoreboard players set #thousand sts.data 1000
execute unless score #g.crops sts.data matches -2147483648.. run scoreboard players set #g.crops sts.data 1000000
execute unless score #crops sts.data matches -2147483648.. run scoreboard players set #crops sts.data 0
execute unless score #g.diamond_block sts.data matches -2147483648.. run scoreboard players set #g.diamond_block sts.data 64
execute unless score #v.diamond_block sts.data matches -2147483648.. run scoreboard players set #v.diamond_block sts.data 0
execute unless score #g.emerald_block sts.data matches -2147483648.. run scoreboard players set #g.emerald_block sts.data 32
execute unless score #v.emerald_block sts.data matches -2147483648.. run scoreboard players set #v.emerald_block sts.data 0
execute unless score #g.iron_block sts.data matches -2147483648.. run scoreboard players set #g.iron_block sts.data 512
execute unless score #v.iron_block sts.data matches -2147483648.. run scoreboard players set #v.iron_block sts.data 0
execute unless score #g.gold_block sts.data matches -2147483648.. run scoreboard players set #g.gold_block sts.data 256
execute unless score #v.gold_block sts.data matches -2147483648.. run scoreboard players set #v.gold_block sts.data 0
execute unless score #g.copper_block sts.data matches -2147483648.. run scoreboard players set #g.copper_block sts.data 256
execute unless score #v.copper_block sts.data matches -2147483648.. run scoreboard players set #v.copper_block sts.data 0
execute unless score #g.redstone_block sts.data matches -2147483648.. run scoreboard players set #g.redstone_block sts.data 128
execute unless score #v.redstone_block sts.data matches -2147483648.. run scoreboard players set #v.redstone_block sts.data 0
execute unless score #g.lapis_block sts.data matches -2147483648.. run scoreboard players set #g.lapis_block sts.data 128
execute unless score #v.lapis_block sts.data matches -2147483648.. run scoreboard players set #v.lapis_block sts.data 0
execute unless score #g.netherite_block sts.data matches -2147483648.. run scoreboard players set #g.netherite_block sts.data 4
execute unless score #v.netherite_block sts.data matches -2147483648.. run scoreboard players set #v.netherite_block sts.data 0
bossbar add sts:crops {"text":"Harvest Silo"}
bossbar set sts:crops color green
bossbar set sts:crops style notched_10
bossbar add sts:vault {"text":"Great Vault"}
bossbar set sts:vault color blue
bossbar set sts:vault style notched_10
bossbar set sts:vault max 8000
function sts:ui/update
