from bs4 import BeautifulSoup
import json
import re
import urllib.request

def get_runes(key, role):
    "Parses the OP.GG analytics page for the given champion in the given role and returns the highest winrate rune page."
    # Create the URL for the champion's runes from the key and role
    rune_url = "https://na.op.gg/champion/{0}/statistics/{1}/rune".format(key, role)

    # Parse the champion's rune page using BeautifulSoup
    rune_soup = BeautifulSoup(urllib.request.urlopen(rune_url), "html.parser")

    all_setups = []

    # Go through all the runes, keeping track of the win rates
    for runes in rune_soup("tr", class_="Row"):
        # Get a single row from the runes table
        rune_setup = runes.find("div", class_="RuneItemList")

        # Ignore header row
        if rune_setup is None:
            continue

        # Get the win rate of this rune setup
        win_rate = float(runes.find("td", class_="Cell WinRate").string.strip().strip("%"))
        all_setups.append((win_rate, rune_setup))

    # Select the rune page with the highest win rate
    best_win_rate, best_runes = max(all_setups, key=lambda x: x[0])

    return_runes = {}

    # Get all the runes for this setup
    for rune in best_runes("div", class_="Item tip"):
        rune_id = int(rune.find("img", class_="Image NonBorder")["src"][62:66])
        quantity = int(rune.find("div", class_="Value").text[1])

        return_runes[rune_id] = quantity

    return (best_win_rate, return_runes)

def get_masteries(key, role):
    "Parses the OP.GG analytics page for the given champion in the given role and returns the highest winrate mastery page."
    # Create the URL for the champion's masteries from the key and role
    mastery_url = "https://na.op.gg/champion/{0}/statistics/{1}/mastery".format(key, role)

    # Parse the champion's masteries page using BeautifulSoup
    mastery_soup = BeautifulSoup(urllib.request.urlopen(mastery_url), "html.parser")

    all_setups = []

    # Go through all the masteries, keeping track of the win rates
    for masteries in mastery_soup("tr", class_="Row"):
        # Get a single row from the masteries table
        mastery_setup = masteries.find("div", class_="mastery-page mastery-page--small")

        # Ignore header row
        if mastery_setup is None:
            continue

        # Get the win rate of this mastery setup
        win_rate = float(masteries.find("td", class_="Cell WinRate").string.strip().strip("%"))
        all_setups.append((win_rate, mastery_setup))

    # Select the mastery page with the highest win rate
    best_win_rate, best_masteries = max(all_setups, key=lambda x: x[0])

    return_masteries = {}

    # Get all the active masteries for this setup
    for mastery in best_masteries("img", src=re.compile(".*/lol/mastery/\d+.png$")):
        mastery_id = int(mastery["src"][65:69])

        rank = mastery.previous_sibling.previous_sibling
        if rank is None:
            return_masteries[mastery_id] = 1
        else:
            return_masteries[mastery_id] = int(rank.string.strip()[0])

    return (best_win_rate, return_masteries)

def get_runes_and_masteries(key, role):
    "Parses the OP.GG analytics page for the given champion in the given role and returns the highest winrate rune and mastery pages."
    # Get the highest winrate rune page
    r_winrate, r_runes = get_runes(key, role)

    # Get the highest winrate mastery page
    m_winrate, m_masteries = get_masteries(key, role)

    return (r_runes, m_masteries)

# Parse champion analytics overview page
soup = BeautifulSoup(urllib.request.urlopen("https://na.op.gg/champion/statistics"), "html.parser")

# Find all div element containing champions
for champion in soup("div", attrs={"data-champion-name": re.compile(".*")}):
    # Get the champion's name and key
    name, key = (champion["data-champion-name"].capitalize(), champion["data-champion-key"])

    # Get the roles associated with the champion
    roles = re.findall("Role-(\w+)", " ".join(champion["class"]))

    for role in roles:
        runes, masteries = get_runes_and_masteries(key, role.lower())
        print("Processed", key.capitalize(), role.capitalize())

    #with open("runes.json") as file:
    #    runes_static = json.load(file)

    #with open("masteries.json") as file:
    #    runes_static = json.load(file)
