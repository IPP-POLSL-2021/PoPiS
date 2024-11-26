import pandas as pd
import math


def calculateVotes(VotesNeeded, VotesNeededForCoalition, year):
    sep = ";"
    if year == "2011":
        sep = ","
    year = "_"+year
    if year == "_2023":
        year = ""
    csvFile = pd.read_csv(
        f"./Data/wyniki_gl_na_listy_po_okregach_sejm_utf8{year}.csv", sep=sep,  decimal=",")
    votes = {"Frekwencja": 0}
    ClubsWithSeats = []
    recivedVotes = []
    # csvFile.info()
    parties = {}
    dataframe = pd.DataFrame(csvFile)
    dataframe = dataframe.fillna(0.0)
    dataframe = dataframe.replace("nan", 0.0)
    for element in dataframe.keys():
        if "KOMITET" in element.upper():
            votes[element] = 0

    for _, distric in dataframe.iterrows():
        for element in dataframe.keys():
            if "KOMITET" in element.upper():
                votes[element] += distric[element]
        # votes["KOMITET WYBORCZY BEZPARTYJNI SAMORZĄDOWCY"] += distric["KOMITET WYBORCZY BEZPARTYJNI SAMORZĄDOWCY"]
        # votes["KOALICYJNY KOMITET WYBORCZY TRZECIA DROGA POLSKA 2050 SZYMONA HOŁOWNI - POLSKIE STRONNICTWO LUDOWE"] += distric[
        #     "KOALICYJNY KOMITET WYBORCZY TRZECIA DROGA POLSKA 2050 SZYMONA HOŁOWNI - POLSKIE STRONNICTWO LUDOWE"]
        # votes["KOMITET WYBORCZY NOWA LEWICA"] += distric["KOMITET WYBORCZY NOWA LEWICA"]
        # votes["KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ"] += distric["KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ"]
        # votes["KOMITET WYBORCZY KONFEDERACJA WOLNOŚĆ I NIEPODLEGŁOŚĆ"] += distric["KOMITET WYBORCZY KONFEDERACJA WOLNOŚĆ I NIEPODLEGŁOŚĆ"]
        # votes["KOALICYJNY KOMITET WYBORCZY KOALICJA OBYWATELSKA PO .N IPL ZIELONI"] += distric["KOALICYJNY KOMITET WYBORCZY KOALICJA OBYWATELSKA PO .N IPL ZIELONI"]
        recivedVotes.append(
            distric["Liczba głosów ważnych oddanych łącznie na wszystkie listy kandydatów"])
        votes["Frekwencja"] += distric["Liczba głosów ważnych oddanych łącznie na wszystkie listy kandydatów"]
    for key in votes.keys():
        result = votes[key]*100/votes["Frekwencja"]
        # print(votes)
        if result >= VotesNeeded and key != "Frekwencja":
            if "KOALICYJNY" in key.upper() and result >= VotesNeededForCoalition:
                ClubsWithSeats.append(key)
            elif "KOALICYJNY" not in key.upper():
                ClubsWithSeats.append(key)

    return ClubsWithSeats, votes, recivedVotes


def chooseMethod(qulifiedDictionary, numberOfVotes, year):
    seatDict = {}
    seatDictAll = {}
    voteDict = {}
    reversedVoteDict = {}
    if len(qulifiedDictionary) == 0:
        return seatDictAll
    sep = ";"
    if year == "2011":
        sep = ","
    year = "_"+year
    if year == "_2023":
        year = ""
    csvFile = pd.read_csv(
        f"./Data/wyniki_gl_na_listy_po_okregach_sejm_utf8{year}.csv", sep=sep,  decimal=",")
    for element in qulifiedDictionary:
        seatDict[element] = 0
        voteDict[element] = 0
        seatDictAll[element] = 0

    csvFile = csvFile.fillna(0.0)
    csvFile = csvFile.replace("nan", 0.0)

    # ClubsWithSeats = []
    methodDict = {"dhont": {}, "Zmodyfikowany Sainte-Laguë": {},
                  "Sainte-Laguë": {}, "Kwota Kwota Hare’a (metoda największych reszt)": {}, "Kwota Hare’a (metoda najmniejszych reszt)": {}}
    distict = 0
    seats = [12, 8, 14, 12, 13, 15, 12, 12, 10, 9, 12, 8, 14, 10, 9, 10,
             9, 12, 20,
             12, 12, 11, 15, 14, 12, 14, 9, 7, 9, 9, 12, 9, 16,
             8, 10, 12, 9, 9, 10, 8, 12]
    yearInt = year[1:]
    if len(yearInt) > 0:
        if int(yearInt) <= 2007:
            seats[12] -= 1
            seats[13] -= 1
            seats[18] -= 1
            seats[19] -= 1
            seats[20] += 1
            seats[23] += 1
            seats[28] += 1
            seats[40] += 1
            if int(yearInt) <= 2001:
                seats[1] += 1
                seats[8] += 1
                seats[11] -= 1
                seats[12] -= 1
                seats[14] += 1
                seats[19] -= 1
                seats[30] += 1
                seats[34] -= 1
    for _, row in csvFile.iterrows():
        for key in voteDict.keys():
            voteDict[key] = row[key]
            reversedVoteDict[row[key]] = key

        # Metoda d'Hondta
        tempDict = seatDict.copy()
        recivedSetats = dhont(tempDict, voteDict, seats[distict])
        for element in qulifiedDictionary:
            methodDict["dhont"][element] = methodDict["dhont"].get(
                element, 0) + recivedSetats[element]

        # Metoda Sainte-Laguë
        tempDict = seatDict.copy()
        recivedSetats = SainteLaguë(tempDict, voteDict, seats[distict])
        for element in qulifiedDictionary:
            methodDict["Sainte-Laguë"][element] = methodDict["Sainte-Laguë"].get(
                element, 0) + recivedSetats[element]

        # Kwota Hare’a (metoda największych reszt)
        tempDict = seatDict.copy()
        recivedSetats = HareDrop(
            tempDict, voteDict, seats[distict], numberOfVotes[distict])
        for element in qulifiedDictionary:
            methodDict["Kwota Kwota Hare’a (metoda największych reszt)"][element] = methodDict["Kwota Kwota Hare’a (metoda największych reszt)"].get(
                element, 0) + recivedSetats[element]

        # Kwota Hare’a (metoda najmniejszych reszt)
        tempDict = seatDict.copy()
        recivedSetats = HareDrop(
            tempDict, voteDict, seats[distict], numberOfVotes[distict], False)
        for element in qulifiedDictionary:
            methodDict["Kwota Hare’a (metoda najmniejszych reszt)"][element] = methodDict["Kwota Hare’a (metoda najmniejszych reszt)"].get(
                element, 0) + recivedSetats[element]

        # Zmodyfikowany Sainte-Laguë
        tempDict = seatDict.copy()
        recivedSetats = ModifiedSainteLaguë(tempDict, voteDict, seats[distict])
        for element in qulifiedDictionary:
            methodDict["Zmodyfikowany Sainte-Laguë"][element] = methodDict["Zmodyfikowany Sainte-Laguë"].get(
                element, 0) + recivedSetats[element]

        distict += 1

    return methodDict


def ModifiedSainteLaguë(SeatsDict,  VoteDict, seatsNum):
    i = 2
    currentMax = ""
    newMax = ""
    lastVoteNum = 0
    nextPotentialVoteNum = 0
    for key in VoteDict.keys():
        VoteDict[key] /= 1.4
    VoteDict2 = VoteDict.copy()

    for _ in range(seatsNum):

        max_party = max(VoteDict2, key=VoteDict2.get)

        SeatsDict[max_party] += 1

        VoteDict2[max_party] = VoteDict[max_party] / \
            (2*SeatsDict[max_party] + 1)
        i += 1
    # print(SeatsDict)
    return SeatsDict


def SainteLaguë(SeatsDict,  VoteDict, seatsNum):
    i = 2
    currentMax = ""
    newMax = ""
    lastVoteNum = 0
    nextPotentialVoteNum = 0

    VoteDict2 = VoteDict.copy()

    for _ in range(seatsNum):

        max_party = max(VoteDict2, key=VoteDict2.get)

        SeatsDict[max_party] += 1

        VoteDict2[max_party] = VoteDict[max_party] / \
            (2*SeatsDict[max_party] + 1)
        i += 1
    # print(SeatsDict)
    return SeatsDict


def dhont(SeatsDict,  VoteDict, seatsNum):
    i = 2
    currentMax = ""
    newMax = ""
    lastVoteNum = 0
    nextPotentialVoteNum = 0

    VoteDict2 = VoteDict.copy()

    for _ in range(seatsNum):

        max_party = max(VoteDict2, key=VoteDict2.get)

        SeatsDict[max_party] += 1

        VoteDict2[max_party] = VoteDict[max_party] / (SeatsDict[max_party] + 1)
        i += 1
    # print(SeatsDict)
    return SeatsDict


def HareDrop(SeatsDict,  VoteDict, seatsNum, Freq, biggest=True):
    VoteDict2 = VoteDict.copy()
    remainingSeats = seatsNum
    for key in VoteDict.keys():

        VoteDict2[key] = (VoteDict[key]*seatsNum)/Freq
        SeatsDict[key] = (int(VoteDict2[key]))
        VoteDict2[key] = VoteDict2[key]-int(VoteDict2[key])
        remainingSeats -= SeatsDict[key]

    if remainingSeats == 0:
        return SeatsDict

    for a in range(0, remainingSeats, 1):
        if biggest is True:
            max_party = max(VoteDict2, key=VoteDict2.get)

            SeatsDict[max_party] += 1

            VoteDict2[max_party] = 0
        else:
            min_party = min(VoteDict2, key=VoteDict2.get)

            SeatsDict[min_party] += 1

            VoteDict2[min_party] = math.inf

    return SeatsDict
