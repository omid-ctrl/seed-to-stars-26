scoreboard players set @s sts_bosses 0
scoreboard players set #done sts.tmp 0
tellraw @s {"text":"== Bosses ==","color":"red","bold":true}
execute if entity @s[advancements={sts:bosses/dragon=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/dragon=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Ender Dragon","color":"white"}]
execute unless entity @s[advancements={sts:bosses/dragon=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Ender Dragon","color":"white"},{"text":"  The End: break the End Crystals on the pillars, then the dragon.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/wither=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/wither=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"The Wither","color":"white"}]
execute unless entity @s[advancements={sts:bosses/wither=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"The Wither","color":"white"},{"text":"  Summon it: 4 soul sand in a T, 3 wither skeleton skulls on top. Fight it underground.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/elder=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/elder=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Elder Guardian","color":"white"}]
execute unless entity @s[advancements={sts:bosses/elder=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Elder Guardian","color":"white"},{"text":"  Ocean Monuments hold three. Water Breathing, and milk for Mining Fatigue.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/warden=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/warden=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"The Warden","color":"white"}]
execute unless entity @s[advancements={sts:bosses/warden=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"The Warden","color":"white"},{"text":"  Ancient Cities in the Deep Dark. Stay quiet; it hunts by sound.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/wildfire=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/wildfire=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Wildfire","color":"white"}]
execute unless entity @s[advancements={sts:bosses/wildfire=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Wildfire","color":"white"},{"text":"  Friends & Foes boss of the Nether. Break its shields first; it drops a crown.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/iceologer=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/iceologer=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Iceologer","color":"white"}]
execute unless entity @s[advancements={sts:bosses/iceologer=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Iceologer","color":"white"},{"text":"  Friends & Foes: an illager that hurls ice.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/illusioner=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/illusioner=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Illusioner","color":"white"}]
execute unless entity @s[advancements={sts:bosses/illusioner=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Illusioner","color":"white"},{"text":"  Friends & Foes: an illager that hides among copies of itself.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/mutant_zombie=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/mutant_zombie=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Mutant Zombie","color":"white"}]
execute unless entity @s[advancements={sts:bosses/mutant_zombie=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Mutant Zombie","color":"white"},{"text":"  Rare night spawn, or splash Chemical X on a zombie.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/mutant_skeleton=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/mutant_skeleton=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Mutant Skeleton","color":"white"}]
execute unless entity @s[advancements={sts:bosses/mutant_skeleton=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Mutant Skeleton","color":"white"},{"text":"  Rare night spawn, or splash Chemical X on a skeleton.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/mutant_creeper=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/mutant_creeper=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Mutant Creeper","color":"white"}]
execute unless entity @s[advancements={sts:bosses/mutant_creeper=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Mutant Creeper","color":"white"},{"text":"  Rare night spawn, or splash Chemical X on a creeper.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/mutant_enderman=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/mutant_enderman=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Mutant Enderman","color":"white"}]
execute unless entity @s[advancements={sts:bosses/mutant_enderman=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Mutant Enderman","color":"white"},{"text":"  Rare spawn, or splash Chemical X on an enderman.","color":"gray"}]
tellraw @s {"text":"== Objectives ==","color":"aqua","bold":true}
execute if entity @s[advancements={sts:bosses/raid=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/raid=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Win a Raid","color":"white"}]
execute unless entity @s[advancements={sts:bosses/raid=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Win a Raid","color":"white"},{"text":"  Drink an Ominous Bottle near a village and beat every wave.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/evoker=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/evoker=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Evoker","color":"white"}]
execute unless entity @s[advancements={sts:bosses/evoker=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Evoker","color":"white"},{"text":"  Woodland Mansions and raids. Drops a Totem of Undying.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/trial=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/trial=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Trial Chambers","color":"white"}]
execute unless entity @s[advancements={sts:bosses/trial=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Trial Chambers","color":"white"},{"text":"  Find a Trial Chamber underground and step inside.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/ominous_vault=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/ominous_vault=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Ominous Vault","color":"white"}]
execute unless entity @s[advancements={sts:bosses/ominous_vault=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Ominous Vault","color":"white"},{"text":"  Open an Ominous Vault with an Ominous Trial Key. The Heavy Core makes a Mace.","color":"gray"}]
execute if entity @s[advancements={sts:bosses/elytra=true}] run scoreboard players add #done sts.tmp 1
execute if entity @s[advancements={sts:bosses/elytra=true}] run tellraw @s [{"text":" ✔ ","color":"green"},{"text":"Wings of the End","color":"white"}]
execute unless entity @s[advancements={sts:bosses/elytra=true}] run tellraw @s [{"text":" ✘ ","color":"red"},{"text":"Wings of the End","color":"white"},{"text":"  End Cities, through the gateway that opens after the dragon.","color":"gray"}]
tellraw @s [{"text":"Done: ","color":"gold"},{"score":{"name":"#done","objective":"sts.tmp"},"color":"white"},{"text":" / 16","color":"white"},{"text":"   Full list: Advancements (L) > Bosses & Objectives","color":"dark_gray"}]
