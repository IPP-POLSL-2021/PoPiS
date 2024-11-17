import pandas as pd


def calculateVotes(VotesNeeded, VotesNeededForCoalition):
    csvFile = pd.read_csv(
        "./Data/wyniki_gl_na_listy_po_okregach_sejm_utf8.csv", sep=";",  decimal=",")
    votes = {"KOMITET WYBORCZY BEZPARTYJNI SAMORZĄDOWCY": 0, "KOALICYJNY KOMITET WYBORCZY KOALICJA OBYWATELSKA PO .N IPL ZIELONI": 0, "KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ": 0,
             "KOMITET WYBORCZY NOWA LEWICA": 0, "KOMITET WYBORCZY KONFEDERACJA WOLNOŚĆ I NIEPODLEGŁOŚĆ": 0, "KOALICYJNY KOMITET WYBORCZY TRZECIA DROGA POLSKA 2050 SZYMONA HOŁOWNI - POLSKIE STRONNICTWO LUDOWE": 0, "Frekwencja": 0}
    ClubsWithSeats = []
    recivedVotes = []
    # csvFile.info()
    parties = {}
    dataframe = pd.DataFrame(csvFile)
    dataframe = dataframe.fillna(0.0)
    dataframe = dataframe.replace("nan", 0.0)
    for element in dataframe.keys():
        if "KOMITET" in element:
            votes[element] = 0

    for _, distric in dataframe.iterrows():
        for element in dataframe.keys():
            if "KOMITET" in element:
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
            if "KOALICYJNY" in key and result >= VotesNeededForCoalition:
                ClubsWithSeats.append(key)
            elif "KOALICYJNY" not in key:
                ClubsWithSeats.append(key)

    return ClubsWithSeats, votes, recivedVotes


def chooseMethod(selectedMethod, qulifiedDictionary, numberOfVotes):
    seatDict = {}
    seatDictAll = {}
    voteDict = {}
    reversedVoteDict = {}

    for element in qulifiedDictionary:
        seatDict[element] = 0
        voteDict[element] = 0
        seatDictAll[element] = 0
    csvFile = pd.read_csv(
        "./Data/wyniki_gl_na_listy_po_okregach_sejm_utf8.csv", sep=";",  decimal=",")

    # ClubsWithSeats = []
    distict = 0
    seats = [12, 8, 14, 12, 13, 15, 12, 12, 10, 9, 12, 8, 14, 10, 9, 10,
             9, 12, 20,
             12, 12, 11, 15, 14, 12, 14, 9, 7, 9, 9, 12, 9, 16,
             8, 10, 12, 9, 9, 10, 8, 12]
    for _, row in csvFile.iterrows():
        for key in voteDict.keys():

            voteDict[key] = row[key]
            reversedVoteDict[row[key]] = key

        match selectedMethod:
            case "d'Hondt":
                for element in qulifiedDictionary:
                    seatDict[element] = 0

                recivedSetats = dhont(seatDict,
                                      voteDict, seats[distict])

                for element in qulifiedDictionary:
                    seatDictAll[element] += recivedSetats[element]

                # print(seatDictAll)
            case "Sainte-Laguë":
                for element in qulifiedDictionary:
                    seatDict[element] = 0

                recivedSetats = SainteLaguë(seatDict,
                                            voteDict, seats[distict])

                for element in qulifiedDictionary:
                    seatDictAll[element] += recivedSetats[element]
            case "Kwota Hare’a (metoda największych reszt)":

                for element in qulifiedDictionary:
                    seatDict[element] = 0

                recivedSetats = HareDrop(seatDict,
                                         voteDict, seats[distict], numberOfVotes[distict])

                for element in qulifiedDictionary:
                    seatDictAll[element] += recivedSetats[element]
            case "Kwota Hare’a (metoda najmniejszych reszt)":
                for element in qulifiedDictionary:
                    seatDict[element] = 0
                # print(numberOfVotes[distict])
                recivedSetats = HareDrop(seatDict,
                                         voteDict, seats[distict], numberOfVotes[distict], False)

                for element in qulifiedDictionary:
                    seatDictAll[element] += recivedSetats[element]
        distict += 1
    return seatDictAll


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

            VoteDict2[min_party] = 0

    return SeatsDict
