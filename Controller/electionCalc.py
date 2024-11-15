import pandas as pd


def calculateVotes(VotesNeeded):
    csvFile = pd.read_csv(
        "./Data/wyniki_gl_na_listy_po_okregach_sejm_utf8.csv", sep=";",  decimal=",")
    votes = {"KOMITET WYBORCZY BEZPARTYJNI SAMORZĄDOWCY": 0, "KOALICYJNY KOMITET WYBORCZY KOALICJA OBYWATELSKA PO .N IPL ZIELONI": 0, "KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ": 0,
             "KOMITET WYBORCZY NOWA LEWICA": 0, "KOMITET WYBORCZY KONFEDERACJA WOLNOŚĆ I NIEPODLEGŁOŚĆ": 0, "KOALICYJNY KOMITET WYBORCZY TRZECIA DROGA POLSKA 2050 SZYMONA HOŁOWNI - POLSKIE STRONNICTWO LUDOWE": 0, "Frekwencja": 0}
    ClubsWithSeats = []
    # csvFile.info()
    dataframe = pd.DataFrame(csvFile)
    for _, distric in dataframe.iterrows():

        votes["KOMITET WYBORCZY BEZPARTYJNI SAMORZĄDOWCY"] += distric["KOMITET WYBORCZY BEZPARTYJNI SAMORZĄDOWCY"]
        votes["KOALICYJNY KOMITET WYBORCZY TRZECIA DROGA POLSKA 2050 SZYMONA HOŁOWNI - POLSKIE STRONNICTWO LUDOWE"] += distric[
            "KOALICYJNY KOMITET WYBORCZY TRZECIA DROGA POLSKA 2050 SZYMONA HOŁOWNI - POLSKIE STRONNICTWO LUDOWE"]
        votes["KOMITET WYBORCZY NOWA LEWICA"] += distric["KOMITET WYBORCZY NOWA LEWICA"]
        votes["KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ"] += distric["KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ"]
        votes["KOMITET WYBORCZY KONFEDERACJA WOLNOŚĆ I NIEPODLEGŁOŚĆ"] += distric["KOMITET WYBORCZY KONFEDERACJA WOLNOŚĆ I NIEPODLEGŁOŚĆ"]
        votes["KOALICYJNY KOMITET WYBORCZY KOALICJA OBYWATELSKA PO .N IPL ZIELONI"] += distric["KOALICYJNY KOMITET WYBORCZY KOALICJA OBYWATELSKA PO .N IPL ZIELONI"]
        votes["Frekwencja"] += distric["Liczba głosów ważnych oddanych łącznie na wszystkie listy kandydatów"]
    for key in votes.keys():
        result = votes[key]*100/votes["Frekwencja"]
        # print(votes)
        if result >= VotesNeeded and key != "Frekwencja":
            ClubsWithSeats.append(key)
    return ClubsWithSeats, votes["Frekwencja"]


def chooseMethod(selectedMethod, qulifiedDictionary, numberOfVotes):
    seatDict = {}
    voteDict = {}
    reversedVoteDict = {}

    for element in qulifiedDictionary:
        seatDict[element] = 0
        voteDict[element] = 0
    csvFile = pd.read_csv(
        "./Data/wyniki_gl_na_listy_po_okregach_sejm_utf8.csv", sep=";",  decimal=",")

    # ClubsWithSeats = []
    distict = 0
    seats = [12, 8, 14, 12, 13, 15, 12, 12, 10, 9, 12, 8, 14, 10, 9, 10, 9, 12, 20,
             12, 12, 11, 15, 14, 12, 14, 9, 7, 9, 9, 12, 9, 16, 8, 10, 12, 9, 9, 10, 8, 12]
    for _, row in csvFile.iterrows():
        for key in voteDict.keys():
            # print(key)
            voteDict[key] = row[key]
            reversedVoteDict[row[key]] = key
            # print("+++++++++++")
            # print(voteDict[key])
            # print(reversedVoteDict)
        match selectedMethod:
            case "d'Hondt":
                print("=====================")
                # print(voteDict)
                a, b, c = dhont(seatDict, reversedVoteDict,
                                voteDict, seats[distict])
                print(a)
                # return dhont(seatDict, reversedVoteDict, voteDict, distict)

            case "Sainte-Laguë":
                return
            case "Kwota Hare’a (metoda największych reszt)":
                # print(HareDrop(PiS, KO, TD, Lewica,
                #       Konf, Freq, type, seatsNum)[:2])
                # print(HareDrop(PiS, KO, TD, Lewica,
                #       Konf, Freq, type, seatsNum+1)[1])
                return
            case "Kwota Hare’a (metoda najmniejszych reszt)":
                return
    distict += 1


def dhont(SeatsDict, reversedSeatsDict, VoteDict, seatsNum):
    i = 2
    currentMax = ""
    newMax = ""
    lastVoteNum = 0
    nextPotentialVoteNum = 0

    for seat in range(0, seatsNum, 1):
        SeatsDict[reversedSeatsDict.get(max(reversedSeatsDict))] += 1
        currentMax = reversedSeatsDict.get(max(reversedSeatsDict))

        VoteDict[reversedSeatsDict.get(max(reversedSeatsDict))] = int(
            VoteDict[reversedSeatsDict.get(max(reversedSeatsDict))]/i)

        reversedSeatsDict = {}
        # reversedSeatsDict = {VoteDict['PiS']: "PiS", VoteDict['KO']: "KO", VoteDict['Trzecia Droga']: "Trzecia Droga",
        #                     VoteDict["Lewica"]: "Lewica", VoteDict["Konfederacja"]: "Konfederacja"}
        for key in VoteDict.keys():
            # voteDict[key] = row[key]
            reversedSeatsDict[VoteDict[key]] = key
        newMax = reversedSeatsDict.get(max(reversedSeatsDict))

        i += 1

    return SeatsDict, currentMax, newMax
