import json
import sys
import pathlib

COMBO_LOCATION = str(pathlib.Path(__file__).parent.resolve()) + "/combo-data.json"
comboDataFile = open(COMBO_LOCATION)
data = json.load(comboDataFile)


def combo_finder(file: str, verbose: bool):
    cards_in_deck = get_only_cards(file)
    results = ""
    count = 0
    for combo in data:
        valid_combo = True
        for card in combo["c"]:
            if card not in cards_in_deck:
                valid_combo = False
        if valid_combo:
            if verbose:
                results += str(combo['c']) + " - " + str(combo['r']) + "\n"
            else:
                results += str(combo['c']) + "\n"
            count += 1
    comboDataFile.close()
    if count == 0:
        return "AN HONEST MAGIC PLAYER! NOT ONE COMBO FOUND!!"
    return "***Combo count:" + str(count) + "***\n\n" + results


def get_only_cards(file: str):
    result = []
    for line in file.splitlines():
        if len(line.split()) > 0 and line.split()[0].isnumeric():
            result.append("".join(list(map(str, line[1:]))).strip())
        else:
            result.append(line)
    return result
