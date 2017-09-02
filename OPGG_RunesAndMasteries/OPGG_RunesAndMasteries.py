from bs4 import BeautifulSoup
from collections import Counter
import humanize
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
        rune_img = rune.find("img", class_="Image NonBorder")["src"]
        rune_id = re.search("(\d+).png$", rune_img).group(1)

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
        mastery_id = re.search("(\d+).png$", mastery["src"]).group(1)

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

with open("runes.json") as file:
    runes_static = json.load(file)["data"]

def pprint_runes(runes):
    for id, count in runes:
        print(count, runes_static[str(id)]["name"])

def pprint_masteries(masteries):
    "Print masteries in a neatly formatted way."
    print("---F---  ---C---  ---R---")
    print("{0}     {1}  {2}     {3}  {4}     {5}".format(masteries.get("6111", 0), masteries.get("6114", 0),
        masteries.get("6311", 0), masteries.get("6312", 0),
        masteries.get("6211", 0), masteries.get("6212", 0)))
    print("{0}  {1}  {2}  {3}  {4}  {5}  {6}  {7}  {8}".format(masteries.get("6121", 0), masteries.get("6122", 0), masteries.get("6123", 0),
        masteries.get("6321", 0), masteries.get("6322", 0), masteries.get("6323", 0),
        masteries.get("6221", 0), masteries.get("6223", 0), masteries.get("6222", 0)))
    print("{0}     {1}  {2}     {3}  {4}     {5}".format(masteries.get("6131", 0), masteries.get("6134", 0),
        masteries.get("6331", 0), masteries.get("6332", 0),
        masteries.get("6231", 0), masteries.get("6232", 0)))
    print("{0}  {1}  {2}  {3}  {4}  {5}  {6}  {7}  {8}".format(masteries.get("6141", 0), masteries.get("6142", 0), masteries.get("6143", 0),
        masteries.get("6341", 0), masteries.get("6342", 0), masteries.get("6343", 0),
        masteries.get("6241", 0), masteries.get("6242", 0), masteries.get("6243", 0)))
    print("{0}     {1}  {2}     {3}  {4}     {5}".format(masteries.get("6151", 0), masteries.get("6154", 0),
        masteries.get("6351", 0), masteries.get("6352", 0),
        masteries.get("6251", 0), masteries.get("6252", 0)))
    print("{0}  {1}  {2}  {3}  {4}  {5}  {6}  {7}  {8}".format(masteries.get("6161", 0), masteries.get("6162", 0), masteries.get("6164", 0),
        masteries.get("6361", 0), masteries.get("6362", 0), masteries.get("6363", 0),
        masteries.get("6261", 0), masteries.get("6262", 0), masteries.get("6263", 0)))

# See modes below for more info
mode = 1

# MODE 1: Get new data from OP.GG and save to file
if mode == 1:
    # Parse champion analytics overview page
    soup = BeautifulSoup(urllib.request.urlopen("https://na.op.gg/champion/statistics"), "html.parser")

    all_runes = []
    all_masteries = []

    # Find all div element containing champions
    for champion in soup("div", attrs={"data-champion-name": re.compile(".*")}):
        # Get the champion's name and key
        name, key = (champion["data-champion-name"].capitalize(),
        champion["data-champion-key"])

        # Get the roles associated with the champion
        roles = re.findall("Role-(\w+)", " ".join(champion["class"]))

        # Get rune and masteries for the champion in each role
        for role in roles:
            runes, masteries = get_runes_and_masteries(key, role.lower())
            all_runes.append(runes)
            all_masteries.append(masteries)
            print("Processed", key.capitalize(), role.capitalize())

    # Write data to file
    with open("cached_runes.json", "w") as file:
        json.dump(all_runes, file, indent=4)

    with open("cached_masteries.json", "w") as file:
        json.dump(all_masteries, file, indent=4)

# MODE 2: Use cached data
elif mode == 2:
    # Open up cached data files
    with open("cached_runes.json") as file:
        all_runes = json.load(file)

    with open("cached_masteries.json") as file:
        all_masteries = json.load(file)

    # create frozen set so we can use dict as keys
    frozen_runes = [frozenset(x.items()) for x in all_runes]
    frozen_masteries = [frozenset(x.items()) for x in all_masteries]

    # Count up the number of unique rune pages and mastery pages
    rune_counts = Counter(frozen_runes)
    masteries_counts = Counter(frozen_masteries)

    # Print out the 20 most common rune pages
    print("Total unique rune pages:", len(rune_counts))
    print("Top 20 Runes:")
    for rune_page in rune_counts.most_common(20):
        pprint_runes(rune_page[0])
        print()

    # Print out the 20 most common mastery pages
    print("Total unique mastery pages:", len(masteries_counts))
    print("Top 20 Masteries:")
    for mastery_page in masteries_counts.most_common(20):
        pprint_masteries(dict(mastery_page[0]))
        print()

# MODE 3: Ask user for champion key and role
elif mode == 3:
    while True:
        # Get champion key from user
        key = input("Enter champion key (q to quit): ")
        if key == "q":
            break

        # Get champion role from user
        role = input("Enter champion role (q to quit): ")
        if role == "q":
            break

        # Look up champion rune and mastery data on OP.GG
        runes, masteries = get_runes_and_masteries(key, role)

        # Print out results
        print()
        pprint_runes(runes.items())
        print()
        pprint_masteries(masteries)
        print()
