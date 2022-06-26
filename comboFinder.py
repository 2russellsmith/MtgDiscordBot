import json
import sys
import os

COMBO_LOCATION = os.getcwd() + "/combo-data.json"
comboDataFile = open(COMBO_LOCATION)
data = json.load(comboDataFile)


def combo_finder(file: str):
    with open("analyzeResults.txt", 'w') as output:
        sys.stdout = output
        cardsInDeck = get_only_cards(file)
        results = ""
        count = 0
        for combo in data:
            validCombo = True
            for card in combo["c"]:
                if (card not in cardsInDeck):
                    validCombo = False
            if (validCombo):
                results += str(combo['c']) + " - " + str(combo['r']) + "\n"
                count += 1
        comboDataFile.close()
        print("Combo count:" + str(count) + "\n\n" + results)
    return "***Combo count:" + str(count) + "***\n\n" + results


def get_only_cards(file: str):
    result = []
    for line in file.splitlines():
        if len(line.split()) > 0 and line.split()[0].isnumeric():
            result.append("".join(list(map(str, line[1:]))).strip())
        else:
            result.append(line)
    return result
