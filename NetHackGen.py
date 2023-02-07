from worlds.nethack import Items, Locations
from worlds.nethack.Items import ItemDef

if __name__ == "__main__":
    print("// GENERATED CODE - use NetHackGen.py in AP codebase")

    print("#[derive(Clone, Copy, Debug, Hash, PartialEq, Eq, serde::Serialize, serde::Deserialize)]")
    print("pub enum Item {")
    for name, val in Items.__dict__.items():
        if isinstance(val, ItemDef):
            print(name, ",")
    print("}")

    print("impl Item {")
    print("pub fn from_id(id: i64) -> Option<Self> {")
    print("match id {")
    for name, val in Items.__dict__.items():
        if isinstance(val, ItemDef):
            print(val.code, "=> Some(Self::", name, "),")
    print("_ => None,")
    print("}")
    print("}")
    print("}")

    print("#[derive(Clone, Copy, Debug, Hash, PartialEq, Eq, serde::Serialize, serde::Deserialize)]")
    print("pub enum LocationPool {")
    for name, ids in Locations.client_pools.items():
        print(name, ",")
    print("}")

    print("pub static LOCATIONS: &[(LocationPool, &[i64])] = &[")
    for name, ids in Locations.client_pools.items():
        print("(LocationPool::", name,
              ",&[", ",".join([str(x) for x in ids]), "]", "),")
    print("];")
