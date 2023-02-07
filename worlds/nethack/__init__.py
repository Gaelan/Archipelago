# world/mygame/__init__.py

from worlds.AutoWorld import WebWorld, World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification, LocationProgressType
from Utils import get_options, output_path
from worlds.generic.Rules import add_rule, set_rule, forbid_item

from . import Items, Locations
from .Items import NetHackItem
from .Locations import NetHackLocation


class NetHackWebWorld(WebWorld):
    theme = "stone"


class NetHackWorld(World):
    """
    NetHack is a classic roguelike dungeon crawler. The player must venture
    deep into the procedurally-generated Mazes of Menace to retrieve the
    Amulet of Yendor.
    """
    game: str = "NetHack"  # name of the game/world
    option_definitions = {}  # options the player can set
    topology_present: bool = True  # show path to required location checks in spoiler

    # web = NetHackWebWorld

    data_version = 0

    item_name_to_id = Items.name_to_id
    location_name_to_id = Locations.name_to_id

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    item_name_groups = {
        # "weapons": {"sword", "lance"}
    }

    def create_regions(self) -> None:
        r = Region("Menu", RegionType.Generic, "Menu",
                   self.player, self.multiworld)
        r.exits = [Entrance(self.player, "New Game", r)]
        self.multiworld.regions.append(r)

        r = Region("Dungeons of Doom", RegionType.Generic,
                   "Dungeons of Doom", self.player, self.multiworld)
        r.locations = [x.reify(self.player, r) for x in Locations.dungeons]
        r.exits = [
            Entrance(self.player, "Stairs to Mines", r),
            Entrance(self.player, "Stairs to Sokoban", r),
            Entrance(self.player, "Portal to Quest", r),
            Entrance(self.player, "Portal to Ludios", r),
            Entrance(self.player, "Castle Trapdoor", r),
            Entrance(self.player, "Escape Stair", r)
        ]
        self.multiworld.regions.append(r)
        self.multiworld.get_entrance("New Game", self.player).connect(
            self.multiworld.get_region("Dungeons of Doom", self.player))

        r = Region("Gnomish Mines", RegionType.Generic,
                   "Gnomish Mines", self.player, self.multiworld)
        r.locations = [x.reify(self.player, r) for x in Locations.mines]
        r.exits = []
        self.multiworld.regions.append(r)
        self.multiworld.get_entrance("Stairs to Mines", self.player).connect(
            self.multiworld.get_region("Gnomish Mines", self.player))

        r = Region("Sokoban", RegionType.Generic,
                   "Sokoban", self.player, self.multiworld)
        r.locations = [x.reify(self.player, r) for x in Locations.sokoban]
        r.exits = []
        self.multiworld.regions.append(r)
        self.multiworld.get_entrance("Stairs to Sokoban", self.player).connect(
            self.multiworld.get_region("Sokoban", self.player))

        r = Region("Quest", RegionType.Generic,
                   "Quest", self.player, self.multiworld)
        r.locations = [x.reify(self.player, r) for x in Locations.quest]
        r.exits = []
        self.multiworld.regions.append(r)
        self.multiworld.get_entrance("Portal to Quest", self.player).connect(
            self.multiworld.get_region("Quest", self.player))

        r = Region("Fort Ludios", RegionType.Generic,
                   "Fort Ludios", self.player, self.multiworld)
        r.locations = [x.reify(self.player, r) for x in Locations.ludios]
        r.exits = []
        self.multiworld.regions.append(r)
        # n.b. this entrance may or may not actually exist
        self.multiworld.get_entrance("Portal to Ludios", self.player).connect(
            self.multiworld.get_region("Fort Ludios", self.player))

        r = Region("Gehennom", RegionType.Generic,
                   "Gehennom", self.player, self.multiworld)
        r.locations = [x.reify(self.player, r) for x in Locations.gehennom]
        r.exits = [
            Entrance(self.player, "Stairs to Vlad's Tower", r),
            Entrance(self.player, "Vibrating Square", r),
        ]
        self.multiworld.regions.append(r)
        self.multiworld.get_entrance("Castle Trapdoor", self.player).connect(
            self.multiworld.get_region("Gehennom", self.player))

        r = Region("Vlad's Tower", RegionType.Generic,
                   "Gehennom", self.player, self.multiworld)
        r.locations = [x.reify(self.player, r) for x in Locations.vlad]
        r.exits = []
        self.multiworld.regions.append(r)
        self.multiworld.get_entrance("Stairs to Vlad's Tower", self.player).connect(
            self.multiworld.get_region("Vlad's Tower", self.player))

        r = Region("Moloch's Sanctum", RegionType.Generic,
                   "Moloch's Sanctum", self.player, self.multiworld)
        r.locations = [x.reify(self.player, r) for x in Locations.sanctum]
        r.exits = []
        self.multiworld.regions.append(r)
        self.multiworld.get_entrance("Vibrating Square", self.player).connect(
            self.multiworld.get_region("Moloch's Sanctum", self.player))

        r = Region("End Game", RegionType.Generic,
                   "End Game", self.player, self.multiworld)
        r.locations = [NetHackLocation(
            "High Altar", None, LocationProgressType.DEFAULT, self.player, r)]
        self.multiworld.regions.append(r)
        self.multiworld.get_entrance("Escape Stair", self.player).connect(
            self.multiworld.get_region("End Game", self.player))

    # TODO: place locations in regions

    def create_items(self) -> None:
        for item in Locations.pool:
            self.multiworld.itempool.append(item.reify(self.player))

    def generate_basic(self) -> None:
        self.multiworld.get_location(
            "High Altar", self.player).place_locked_item(NetHackItem("Victory", None, ItemClassification.progression, self.player))

        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            "Victory", self.player)

    def set_rules(self) -> None:
        set_rule(self.multiworld.get_entrance("Escape Stair", self.player),
                 lambda state: state.has(Items.AmuletOfYendor.name, self.player))

        invocation_items = [
            Items.Bell.name,
            Items.Book.name,
            Items.Candelabrum.name,
            Items.WaxCandles.name,
            Items.TallowCandles.name
        ]
        set_rule(self.multiworld.get_entrance("Vibrating Square", self.player),
                 lambda state: all([state.has(x, self.player) for x in invocation_items]))

    def fill_slot_data(self):
        loc_ids = Locations.name_to_id.values()
        return {"items": {loc.address: loc.item.code for loc in self.multiworld.get_locations(self.player) if loc.address != None}}
