from BaseClasses import Location, LocationProgressType as PT
from . import Items

base_id = 0x6e68 * 1000  # hex for "nh"
next_id = base_id

name_to_id = {}
# location IDs, grouped by pool name, for use in the client
client_pools = {}
# the item pool for AP
pool = []


class LocationDef:
    def __init__(this, name, id, pt):
        this.name = name
        this.address = id
        this.progress_type = pt

    def reify(this, player, region):
        return NetHackLocation(this.name, this.address, this.progress_type, player, region)


class NetHackLocation(Location):  # or from Items import MyGameItem
    game = "NetHack"  # name of the game/world this item is from

    def __init__(this, name, id, pt, player, region):
        this.name = name
        this.address = id
        this.progress_type = pt
        this.player = player
        this.parent_region = region

# we build the list of locations and the item pool at the same time, ensuring
# they stay in sync and we have items occur with the same frequencies as
# vanilla nethack


def make_location(region, client_pool_name, name, item, pt=PT.DEFAULT, count=None):
    if count:
        for i in range(count):
            make_location(region, client_pool_name,
                          f"{name} {i+1}", item, pt=pt)
    else:
        global next_id
        global client_pools

        id = next_id
        next_id += 1
        name_to_id[name] = id

        client_pools.setdefault(client_pool_name, []).append(id)

        pool.append(item)

        region.append(LocationDef(name, id, pt))


# regions
dungeons = []
mines = []
sokoban = []
ludios = []
quest = []
gehennom = []
vlad = []
sanctum = []
endgame = []


make_location(dungeons, "DungeonsRand",
              "Dungeons of Doom random object", Items.Rand, count=34)

# mines: 6-7 standard levels, plus town and end
for i in range(1, 7):
    make_location(mines, f"Mines{i}Tool",
                  f"Gnomish Mines filler level {i}", Items.RandTool)
make_location(mines, "Mines7Tool", "Gnomish Mines filler level 7",
              Items.RandTool, pt=PT.EXCLUDED)
make_location(mines, "MinesRand", "Gnomish Mines random objects",
              Items.Rand, count=8)

make_location(mines, "MinesEndRand", "Mine's End random object", Items.Rand)
make_location(mines, "MinesEndLuckstone",
              "Mine's End luckstone spot", Items.Luckstone)

# sokoban
for i in range(1, 4):
    make_location(
        sokoban, "SokobanRing", f"Sokoban level {i} random object 1", Items.RandRing)
    make_location(
        sokoban, "SokobanWand", f"Sokoban level {i} random object 2", Items.RandWand)
make_location(sokoban, "SokobanEarth", "Sokoban scroll of earth spot",
              Items.EarthScroll, count=2)
make_location(sokoban, "SokobanReward", "Sokoban reward", Items.SokobanReward)
# Sokoban zoo: 28 cells, 1/6 chance of item drop, 1/3 chance of AP item =
# 1.55... items
# plus random monster generations in sokoban, this should be fairly safe?
make_location(sokoban, "SokobanRand", "Sokoban random item", Items.Rand)

# ludios - not accessible in every game, so exclude
make_location(ludios, "LudiosDiamond", "Fort Ludios diamond cache",
              Items.Diamond, pt=PT.EXCLUDED)
make_location(ludios, "LudiosEmerald", "Fort Ludios emerald cache",
              Items.Emerald, pt=PT.EXCLUDED)
make_location(ludios, "LudiosAmethyst", "Fort Ludios amethyst cache",
              Items.Amethyst, pt=PT.EXCLUDED)
make_location(ludios, "LudiosRuby", "Fort Ludios ruby cache",
              Items.Ruby, pt=PT.EXCLUDED)
# Ludios monsters:
# 23 in zoo + 39 in throne room + 68 in barracks = 130
# * 1/3 * 1/6 (as above for sokoban) = 7.22....
# (these are excluded so it's not the end of the world if we don't gen one)
make_location(ludios, "LudiosRand", "Fort Ludios random items",
              Items.Rand, count=7, pt=PT.EXCLUDED)

# quest
make_location(quest, "QuestRand",
              "quest branch random object", Items.Rand, count=13)
make_location(quest, "QuestArtifact",
              "under quest leader", Items.QuestArtifact)
make_location(quest, "Bell", "quest leader inventory",
              Items.Bell, pt=PT.PRIORITY)

# rogue
make_location(dungeons, "RogueArmor",
              "Rogue level bones pile 1", Items.RogueArmor)
make_location(dungeons, "RogueWeapon",
              "Rogue level bones pile 2", Items.RogueWeapon)

# castle
make_location(dungeons, "CastleFood", "castle food storage",
              Items.RandFood, count=4)
make_location(dungeons, "CastleArmor", "castle armor storage",
              Items.RandArmor, count=4)
make_location(dungeons, "CastleWeapon", "castle weapon storage",
              Items.RandWeapon, count=4)
make_location(dungeons, "CastleGem", "castle gem storage",
              Items.RandGem, count=4)
make_location(dungeons, "CastleWand", "castle chest", Items.WandOfWishing)

# gehennom
make_location(gehennom, "GehennomRand",
              "Gehennom random items", Items.Rand, count=41)

geh_special_levels = [
    ("Valley of the Dead", "Valley", [Items.RandArmor, Items.RandWeapon, Items.RandGem,
     Items.RandPotion, Items.RandScroll, Items.RandWand, Items.RandRing, Items.RandTool]),
    ("Asmodeus' Lair", "Asmodeus", [Items.RandArmor, Items.RandWeapon,
     Items.RandGem, Items.RandPotion, Items.RandScroll]),
    ("Baalzebub's Lair", "Baalzebub", [Items.RandArmor, Items.RandWeapon,
     Items.RandGem, Items.RandPotion, Items.RandScroll]),
    ("Jubilex's Swamp",  "Jubilex", [
     Items.RandGem, Items.RandPotion, Items.RandFood]),
    ("Wizard's Tower top floor", "TowerTop", [
     Items.RandPotion, Items.RandScroll, Items.RandSpellbook]),
    ("Wizard's Tower middle floor", "TowerMid", [
     Items.RandPotion, Items.RandScroll, Items.RandSpellbook, Items.RandAmulet]),
    ("Wizard's Tower bottom floor", "TowerBot", [
     Items.RandWeapon, Items.RandPotion, Items.RandScroll, Items.RandTool, Items.RandAmulet]),
    ("Moloch's Sanctum", "Sanctum", [
     Items.RandArmor, Items.RandWeapon, Items.RandGem, Items.RandPotion, Items.RandScroll]),
]

for (name, client_name, items) in geh_special_levels:
    for (i, item) in enumerate(items):
        make_location(sanctum if client_name ==
                      "Sanctum" else gehennom, client_name, f"{name} {i+1}", item)

# fake wizard's tower
make_location(gehennom, "FakeTower", "fake Wizard's Tower", Items.RandAmulet)

# vlad's tower
make_location(vlad, "VladCandle",
              "Vlad's tower top floor candle chest 1", Items.WaxCandles)
make_location(vlad, "VladCandle", "Vlad's tower top floor candle chest 2",
              Items.TallowCandles)
make_location(vlad, "VladChest", "Vlad's tower top floor non-candle chests",
              Items.Rand, count=2)
make_location(vlad, "VladMid",
              "Vlad's tower middle floor niche 1", Items.VladAmulet)
make_location(vlad, "VladMid",
              "Vlad's tower middle floor niche 2", Items.VladAmulet)
make_location(vlad, "VladMid", "Vlad's tower middle floor niche 3",
              Items.CrystalPlateMail)
make_location(vlad, "VladMid", "Vlad's tower middle floor niche 4",
              Items.InvisibilitySpellbook)
make_location(vlad, "VladMid", "Vlad's tower middle floor niche 5",
              Items.WaterWalkingBoots)
make_location(vlad, "ValdBot",
              "Vlad's tower bottom floor niche 1", Items.LongSword)
make_location(vlad, "VladBot",
              "Vlad's tower bottom floor niche 2", Items.LockPick)
make_location(vlad, "VladBot",
              "Vlad's tower bottom floor niche 3", Items.ElvenClak)
make_location(vlad, "VladBot",
              "Vlad's tower bottom floor niche 4", Items.Blindfold)
make_location(vlad, "Candelabrum", "Vlad the Impaler's inventory",
              Items.Candelabrum, pt=PT.PRIORITY)

# wizard's tower
make_location(gehennom, "Book", "under the Wizard of Yendor",
              Items.Book, pt=PT.PRIORITY)

# moloch's sanctum
make_location(sanctum, "Amulet", "High Priest's of Moloch's inventory",
              Items.AmuletOfYendor, pt=PT.PRIORITY)

# nothing in the endgame, at least for now - there may be monster drops, but
# the player isn't exactly supposed to stop and kill everything
