scoreboard players set @s sts_status 0
tellraw @s {"text":"== Seed to Stars ==","color":"gold","bold":true}
tellraw @s [{"text":"Harvest Silo: ","color":"gold"},{"score":{"name":"#crops","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.crops","objective":"sts.data"}},{"text":" crops","color":"gray"}]
tellraw @s {"text":"Great Vault (blocks delivered / needed):","color":"aqua"}
tellraw @s [{"text":"  Diamond: ","color":"gray"},{"score":{"name":"#v.diamond_block","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.diamond_block","objective":"sts.data"}}]
tellraw @s [{"text":"  Emerald: ","color":"gray"},{"score":{"name":"#v.emerald_block","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.emerald_block","objective":"sts.data"}}]
tellraw @s [{"text":"  Iron: ","color":"gray"},{"score":{"name":"#v.iron_block","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.iron_block","objective":"sts.data"}}]
tellraw @s [{"text":"  Gold: ","color":"gray"},{"score":{"name":"#v.gold_block","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.gold_block","objective":"sts.data"}}]
tellraw @s [{"text":"  Copper: ","color":"gray"},{"score":{"name":"#v.copper_block","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.copper_block","objective":"sts.data"}}]
tellraw @s [{"text":"  Redstone: ","color":"gray"},{"score":{"name":"#v.redstone_block","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.redstone_block","objective":"sts.data"}}]
tellraw @s [{"text":"  Lapis: ","color":"gray"},{"score":{"name":"#v.lapis_block","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.lapis_block","objective":"sts.data"}}]
tellraw @s [{"text":"  Netherite: ","color":"gray"},{"score":{"name":"#v.netherite_block","objective":"sts.data"},"color":"white"},{"text":" / "},{"score":{"name":"#g.netherite_block","objective":"sts.data"}}]
tellraw @s {"text":"Keys: ; hides or shows the bars, ' shows this, [ lists bosses (rebind under Controls > Seed to Stars). Or /trigger sts_bars, sts_status, sts_bosses.","color":"dark_gray","italic":true}
