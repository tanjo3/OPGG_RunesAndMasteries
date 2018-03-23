import importlib
lol_runes = importlib.import_module("lol_runes")

def test_valid_champion_name_1():
    assert lol_runes.check_champion_name("Ashe") == 22

def test_valid_champion_name_2():
    assert lol_runes.check_champion_name("NAMI") == 267

def test_valid_champion_name_3():
    assert lol_runes.check_champion_name(" aKaLi ") == 84

def test_valid_champion_name_4():
    assert lol_runes.check_champion_name("kha'zix") == 121

def test_valid_champion_name_5():
    assert lol_runes.check_champion_name("Wukong") == 62

def test_invalid_champion_name_1():
    assert lol_runes.check_champion_name("v1") is None

def test_invalid_champion_name_2():
    assert lol_runes.check_champion_name("SpaghettiMonster") is None

def test_valid_champion_role_1():
    assert lol_runes.check_champion_role("support") == "SUPPORT"

def test_invalid_champion_role_1():
    assert lol_runes.check_champion_name("bot") is None
