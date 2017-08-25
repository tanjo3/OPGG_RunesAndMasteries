from bs4 import BeautifulSoup
import re
import urllib.request

# Parse champion analytics overview page
soup = BeautifulSoup(urllib.request.urlopen("https://na.op.gg/champion/statistics"), "html.parser")

# Find all div element containing champions
for x in soup.find_all("div", attrs={"data-champion-name": re.compile(".*")}):
    # For now, print out champion name and key
    print(x["data-champion-name"], x["data-champion-key"])
