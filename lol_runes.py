"""OP.GG Runes

"""

import re
from itertools import product
from multiprocessing import cpu_count, Pool
from urllib.request import urlopen

from bs4 import BeautifulSoup

RUNE_PATHS = {
    8000: "Precision",
    8100: "Domination",
    8200: "Sorcery",
    8300: "Inspiration",
    8400: "Resolve"
}

RUNE_KEYSTONES = {
    8000: {
        8005: "Press the Attack",
        8008: "Lethal Tempo",
        8021: "Fleet Footwork"
    },
    8100: {
        8112: "Electrocute",
        8124: "Predator",
        8128: "Dark Harvest"
    },
    8200: {
        8214: "Summon Aery",
        8229: "Arcane Comet",
        8230: "Phase Rush"
    },
    8300: {
        8326: "Unsealed Spellbook",
        8351: "Glacial Augment",
        8359: "Kleptomancy"
    },
    8400: {
        8437: "Grasp of the Undying",
        8439: "Aftershock",
        8465: "Guardian"
    }
}

RUNE_LESSERS = {
    8000: [{
        8009: "Presence of Mind",
        9101: "Overheal",
        9111: "Triumph"
    }, {
        9103: "Legend: Bloodline",
        9104: "Legend: Alacrity",
        9105: "Legend: Tenacity"
    }, {
        8014: "Coup de Grace",
        8017: "Cut Down",
        8299: "Last Stand"
    }],
    8100: [{
        8126: "Cheap Shot",
        8139: "Taste of Blood",
        8143: "Sudden Impact"
    }, {
        8120: "Ghost Poro",
        8136: "Zombie Ward",
        8138: "Eyeball Collection"
    }, {
        8105: "Relentless Hunter",
        8134: "Ingenious Hunter",
        8135: "Ravenous Hunter"
    }],
    8200: [{
        8224: "Nullifying Orb",
        8226: "Manaflow Band",
        8243: "The Ultimate Hat"
    }, {
        8210: "Transcendence",
        8233: "Absolute Focus",
        8234: "Celerity"
    }, {
        8232: "Waterwalking",
        8236: "Gathering Storm",
        8237: "Scorch"
    }],
    8300: [{
        8306: "Hextech Flashtraption",
        8313: "Perfect Timing",
        8345: "Biscuit Delivery"
    }, {
        8304: "Magical Footwear",
        8316: "Minion Dematerializer",
        8321: "Future's Market"
    }, {
        8339: "Celestial Body",
        8347: "Cosmic Insight",
        8410: "Approach Velocity"
    }],
    8400: [{
        8242: "Unflinching",
        8446: "Demolish",
        8463: "Font of Life"
    }, {
        8429: "Conditioning",
        8430: "Iron Skin",
        8435: "Mirror Shell"
    }, {
        8444: "Second Wind",
        8451: "Overgrowth",
        8453: "Revitalize"
    }]}

CHAMPIONS = {
    "monkeyking": 62,
    "jax": 24,
    "fiddlesticks": 9,
    "shaco": 35,
    "warwick": 19,
    "xayah": 498,
    "nidalee": 76,
    "zyra": 143,
    "kled": 240,
    "brand": 63,
    "rammus": 33,
    "illaoi": 420,
    "corki": 42,
    "braum": 201,
    "darius": 122,
    "tryndamere": 23,
    "missfortune": 21,
    "yorick": 83,
    "xerath": 101,
    "sivir": 15,
    "riven": 92,
    "orianna": 61,
    "gangplank": 41,
    "malphite": 54,
    "poppy": 78,
    "karthus": 30,
    "jayce": 126,
    "nunu": 20,
    "trundle": 48,
    "graves": 104,
    "zoe": 142,
    "gnar": 150,
    "lux": 99,
    "shyvana": 102,
    "renekton": 58,
    "fiora": 114,
    "jinx": 222,
    "kalista": 429,
    "fizz": 105,
    "kassadin": 38,
    "sona": 37,
    "irelia": 39,
    "viktor": 112,
    "rakan": 497,
    "kindred": 203,
    "cassiopeia": 69,
    "maokai": 57,
    "ornn": 516,
    "thresh": 412,
    "kayle": 10,
    "hecarim": 120,
    "khazix": 121,
    "olaf": 2,
    "ziggs": 115,
    "syndra": 134,
    "drmundo": 36,
    "karma": 43,
    "annie": 1,
    "akali": 84,
    "volibear": 106,
    "yasuo": 157,
    "kennen": 85,
    "rengar": 107,
    "ryze": 13,
    "shen": 98,
    "zac": 154,
    "talon": 91,
    "swain": 50,
    "bard": 432,
    "sion": 14,
    "vayne": 67,
    "nasus": 75,
    "kayn": 141,
    "twistedfate": 4,
    "chogath": 31,
    "udyr": 77,
    "lucian": 236,
    "ivern": 427,
    "leona": 89,
    "caitlyn": 51,
    "sejuani": 113,
    "nocturne": 56,
    "zilean": 26,
    "azir": 268,
    "rumble": 68,
    "morgana": 25,
    "taliyah": 163,
    "teemo": 17,
    "urgot": 6,
    "amumu": 32,
    "galio": 3,
    "heimerdinger": 74,
    "anivia": 34,
    "ashe": 22,
    "velkoz": 161,
    "singed": 27,
    "skarner": 72,
    "varus": 110,
    "twitch": 29,
    "garen": 86,
    "blitzcrank": 53,
    "masteryi": 11,
    "elise": 60,
    "alistar": 12,
    "katarina": 55,
    "ekko": 245,
    "mordekaiser": 82,
    "lulu": 117,
    "camille": 164,
    "aatrox": 266,
    "draven": 119,
    "tahmkench": 223,
    "pantheon": 80,
    "xinzhao": 5,
    "aurelionsol": 136,
    "leesin": 64,
    "taric": 44,
    "malzahar": 90,
    "lissandra": 127,
    "diana": 131,
    "tristana": 18,
    "reksai": 421,
    "vladimir": 8,
    "jarvaniv": 59,
    "nami": 267,
    "jhin": 202,
    "soraka": 16,
    "veigar": 45,
    "janna": 40,
    "nautilus": 111,
    "evelynn": 28,
    "gragas": 79,
    "zed": 238,
    "vi": 254,
    "kogmaw": 96,
    "ahri": 103,
    "quinn": 133,
    "leblanc": 7,
    "ezreal": 81
}

# Number of processes to be spawned for concurrency
NUM_PROCESSES = cpu_count()

# Percentage threshold for even considering a rune setup
PICKRATE_THRESHOLD = 0.10


def check_champion_name(champ_name):
    """Validates a string to be the name of a champion.

    If the string is a valid champion name, this function will return the corresponding ID. Otherwise, it returns None.

    Parameters
    ----------
    champ_name : str
        Champion name.

    Returns
    -------
    int
        Champion ID.

    """

    # First, change it to all lowercase
    champ_name = champ_name.strip().lower()

    # Remove spaces and apostrophes
    champ_name = champ_name.replace(" ", "")
    champ_name = champ_name.replace("'", "")

    # Change wukong -> monkeyking
    if champ_name == "wukong":
        champ_name = "monkeyking"

    # Check if key is in champion dictionary
    if champ_name in CHAMPIONS:
        # If it is, return the ID of that champion
        return CHAMPIONS[champ_name]
    else:
        return None


def check_champion_role(champ_role):
    """Validates a string to be a role.

    If the string is a valid role, this function will returns the role in uppercase. Otherwise, it returns None.

    Parameters
    ----------
    champ_role : str
        Role.

    Returns
    -------
    str
        Valid role.

    """

    # Convert string to all uppercase
    champ_role = champ_role.upper()

    # Check that it matches one of the five possible roles
    if champ_role == "TOP" or champ_role == "JUNGLE" or champ_role == "MID" or \
            champ_role == "ADC" or champ_role == "SUPPORT":
        return champ_role
    else:
        return None


def get_runes_for_paths(champ_id, champ_role, keystone_id, secondary_path_id):
    """Retrieve rune data from OP.GG.

    Parses the OP.GG analytics page for the given champion, role, keystone rune, and secondary path and returns the highest winrate rune page.

    Parameters
    ----------
    champ_id : int
        Champion ID.
    champ_role : str
        Role.
    keystone_id : int
        Keystone rune ID.
    secondary_path_id : str
        Secondary path ID.

    Returns
    -------
    dict
        Rune setup.

    """

    # Generate the URL to the runes data for the combination of primary and secondary paths
    rune_url = "http://www.op.gg/champion/ajax/statistics/runeList/championId={0}&position={1}&primaryPerkId={2}&subPerkStyleId={3}"
    rune_url = rune_url.format(
        champ_id, champ_role, keystone_id, secondary_path_id)

    # Parse the champion's rune page using BeautifulSoup
    rune_soup = BeautifulSoup(urlopen(rune_url), "html.parser")

    # Find the rune setup with the highest winrate
    best_runes, best_pickrate, best_winrate = (None, 0, 0)
    table_rows = rune_soup.tbody("tr")
    for row in table_rows:
        runes_data = row(
            "td", "champion-stats__table__cell champion-stats__table__cell--data")[0]
        runes_pickrate = float(row(
            "td", "champion-stats__table__cell champion-stats__table__cell--pickrate"
        )[0].contents[0].strip(" %%"))
        runes_winrate = float(row(
            "td", "champion-stats__table__cell champion-stats__table__cell--winrate"
        )[0].string.strip(" %%"))

        # Don't consider rune setups that are picked less than the threshold
        if runes_pickrate >= PICKRATE_THRESHOLD:
            # Split ties using pickrate
            if runes_winrate > best_winrate \
                    or (runes_winrate == best_winrate and runes_pickrate > best_pickrate):
                best_runes = runes_data
                best_pickrate = runes_pickrate
                best_winrate = runes_winrate

    # Parse the rune setup into dictionary
    return_dict = {
        "runes": str(best_runes),
        "keystone": keystone_id,
        "secondary": secondary_path_id,
        "pickrate": best_pickrate,
        "winrate": best_winrate
    }

    return return_dict


def get_runes(champ_id, champ_role):
    """Retrieve rune data from OP.GG.

    Parses the OP.GG analytics page for the given champion in the given role and returns the highest winrate rune page of all path combinations.

    Parameters
    ----------
    champ_id : int
        Champion ID.
    champ_role : str
        Role.

    Returns
    -------
    dict
        Rune setup.

    """

    # Create a list of the keystone IDs
    keystone_ids = [keystone_id for keystones in RUNE_KEYSTONES.values()
                    for keystone_id in keystones]

    # Execute loop in parallel to speed up execution
    all_runes = []
    with Pool(NUM_PROCESSES) as pool:
        # Loop through all combinations of primary and secondary paths
        all_runes = pool.starmap(get_runes_for_paths, [
            (champ_id, champ_role, x, y) for x, y in product(keystone_ids, RUNE_PATHS)
        ])

    # Find the highest winrate setup across all combinations of primary and secondary paths
    best_runes, best_pickrate, best_winrate = (None, 0, 0)
    for setup in all_runes:
        # Only consider rune setups whose best pickrate is above our threshold
        if setup["pickrate"] >= PICKRATE_THRESHOLD:
            # Split ties using pickrate
            if setup["winrate"] > best_winrate \
                    or (setup["winrate"] == best_winrate and setup["pickrate"] > best_pickrate):
                best_runes = setup
                best_pickrate = setup["pickrate"]
                best_winrate = setup["winrate"]

    # Determine the ID of the primary path
    primary_path_id = (best_runes["keystone"] // 100) * 100

    # Parse the rune setup into dictionary
    return_dict = {
        "primary": (primary_path_id, [best_runes["keystone"]]),
        "secondary": (best_runes["secondary"], []),
        "pickrate": best_pickrate,
        "winrate": best_winrate
    }

    # Parse HTML for best rune setup to get rune IDs
    id_regex = re.compile("(\d*).png")
    best_runes_soup = BeautifulSoup(best_runes["runes"], "html.parser")
    primary_runes, secondary_runes = [path(class_="perk-page__item perk-page__item--active")
                                      for path in best_runes_soup(class_="perk-page")]

    # Add rune IDs for primary path into return dictionary
    for primary_rune in primary_runes:
        rune_id = int(id_regex.findall(primary_rune.img["src"])[0])
        return_dict["primary"][1].append(rune_id)

    # Add rune IDs for secondary path into return dictionary
    for secondary_rune in secondary_runes:
        rune_id = int(id_regex.findall(secondary_rune.img["src"])[0])
        return_dict["secondary"][1].append(rune_id)

    return return_dict


def pprint_runes(runes_dict):
    """Prints a rune setup in a nicely formatted matter.

    Parameters
    ----------
    runes_dict : dict
        Rune setup.

    """

    primary_path_id = runes_dict["primary"][0]
    secondary_path_id = runes_dict["secondary"][0]

    primary_runes = {}
    for lesser_runes in RUNE_LESSERS[primary_path_id]:
        primary_runes.update(lesser_runes)

    secondary_runes = {}
    for lesser_runes in RUNE_LESSERS[secondary_path_id]:
        secondary_runes.update(lesser_runes)

    # Print primary path
    print("Primary:", RUNE_PATHS[primary_path_id])
    for primary_rune in runes_dict["primary"][1]:
        if primary_rune not in primary_runes:
            print("    ", RUNE_KEYSTONES[primary_path_id][primary_rune])
        else:
            print("    ", primary_runes[primary_rune])

    # Print secondary path
    print("Secondary:", RUNE_PATHS[secondary_path_id])
    for secondary_rune in runes_dict["secondary"][1]:
        print("    ", secondary_runes[secondary_rune])

    # Print winrate and pickrate
    print("Win %: {0:0.2F}%    Pick %: {1:0.2F}%".format(
        runes_dict["winrate"], runes_dict["pickrate"]))


if __name__ == "__main__":
    while True:
        # Get champion key from user
        NAME = input("Enter champion key (q to quit): ")
        if NAME == "" or NAME == "q":
            break

        # Convert champion name to ID
        CHAMPION_ID = check_champion_name(NAME)
        if CHAMPION_ID is None:
            print("ERROR: Invalid champion name {}.".format(NAME))
            continue

        # Get champion role from user
        ROLE = input("Enter champion role (q to quit): ")
        if ROLE == "" or ROLE == "q":
            break

        # Check that role is valid
        VALID_ROLE = check_champion_role(ROLE)
        if VALID_ROLE is None:
            print("ERROR: Invalid champion role {}.".format(ROLE))
            continue

        try:
            # Look up champion rune data on OP.GG
            BEST_RUNES = get_runes(CHAMPION_ID, ROLE)

            # Print the runes in a pretty format
            pprint_runes(BEST_RUNES)
        except:
            print("ERROR: Unable to retrieve runes.")
