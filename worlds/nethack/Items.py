from BaseClasses import ItemClassification as IC, Item


class NetHackItem(Item):
    game = "NetHack"  # name of the game/world this item is from

    def __init__(this, name, id, ic, player):
        this.name = name
        this.code = id
        this.classification = ic
        this.player = player


class ItemDef:
    def __init__(this, name, id, ic):
        this.name = name
        this.code = id
        this.classification = ic

    def reify(this, player):
        return NetHackItem(this.name, this.code, this.classification, player)


base_id = 0x6e68 * 1000  # hex for "nh"
next_id = base_id

name_to_id = {}


def make_item(name, ic=IC.filler):
    global next_id

    id = next_id
    next_id += 1
    name_to_id[name] = id
    return ItemDef(name, id, ic)


# progression items
AmuletOfYendor = make_item('Amulet of Yendor', ic=IC.progression)
Bell = make_item('Bell of Opening', ic=IC.progression)
Book = make_item('Book of the Dead', ic=IC.progression)
Candelabrum = make_item('Candelabrum of Invocation', ic=IC.progression)

# mines loot
Luckstone = make_item('luckstone', ic=IC.useful)

# sokoban loot
SokobanReward = make_item('sokoban reward', ic=IC.useful)
EarthScroll = make_item('scroll of earth', ic=IC.useful)

# rogue level loot
RogueWeapon = make_item('mace or two-handed sword', ic=IC.useful)
RogueArmor = make_item('ring mail or plate mail', ic=IC.useful)

# quest loot
QuestArtifact = make_item('quest artifact', ic=IC.useful)

# castle loot
WandOfWishing = make_item('wand of wishing', ic=IC.useful)

# ludios loot
Diamond = make_item('diamond')
Ruby = make_item('ruby')
Emerald = make_item('emerald')
Amethyst = make_item('amethyst')

# vlad loot
WaxCandles = make_item('wax candles', ic=IC.progression)
TallowCandles = make_item('tallow candles', ic=IC.progression)

VladAmulet = make_item('amulet of strangulation or life saving', IC.useful)
WaterWalkingBoots = make_item('water walking boots', ic=IC.useful)
CrystalPlateMail = make_item('crystal plate mail', ic=IC.useful)
InvisibilitySpellbook = make_item('spellbook of invisibility', ic=IC.useful)

LongSword = make_item('long sword', ic=IC.useful)
LockPick = make_item('lock pick', ic=IC.useful)
ElvenClak = make_item('elven cloak', ic=IC.useful)
Blindfold = make_item('blindfold', ic=IC.useful)

# random items
RandAmulet = make_item('random amulet')
RandArmor = make_item('random armor')
RandFood = make_item('random food')
RandGem = make_item('random gem')
RandPotion = make_item('random potion')
RandRing = make_item('random ring')
RandScroll = make_item('random scroll')
RandSpellbook = make_item('random spellbook')
RandTool = make_item('random tool')
RandWand = make_item('random wand')
RandWeapon = make_item('random weapon')

Rand = make_item('random item')
