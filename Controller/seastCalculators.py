def chooseMethod(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum, method):
    match method:
        case "d'Hondt":
            return dhont(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum)

        case "Sainte-Laguë":
            return SainteLague(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum)


def dhont(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum):
    i = 2
    SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                 "Lewica": 0, "Konfederacja": 0}
    reversedSeatsDict = {PiS: "PiS", KO: "KO", TD: "Trzecia Droga",
                         Lewica: "Lewica", Konf: "Konfederacja"}
    VoteDict = {"PiS": PiS, "KO": KO, "Trzecia Droga": TD,
                "Lewica": Lewica, "Konfederacja": Konf}
    gatheredSeats = {"PiS": [], "KO": [], "Trzecia Droga": [],
                     "Lewica": [], "Konfederacja": []}
    currentMax = ""
    newMax = ""
    lastVoteNum = 0
    nextPotentialVoteNum = 0
    if type == "ilościowy":

        for seat in range(0, seatsNum, 1):
            SeatsDict[reversedSeatsDict.get(max(reversedSeatsDict))] += 1
            currentMax = reversedSeatsDict.get(max(reversedSeatsDict))
            lastVoteNum = VoteDict[reversedSeatsDict.get(
                max(reversedSeatsDict))]
            VoteDict[reversedSeatsDict.get(max(reversedSeatsDict))] /= i
            gatheredSeats[currentMax].append(i)
            reversedSeatsDict = {}
            reversedSeatsDict = {VoteDict['PiS']: "PiS", VoteDict['KO']: "KO", VoteDict['Trzecia Droga']: "Trzecia Droga",
                                 VoteDict["Lewica"]: "Lewica", VoteDict["Konfederacja"]: "Konfederacja"}
            newMax = reversedSeatsDict.get(max(reversedSeatsDict))
            nextPotentialVoteNum = VoteDict[reversedSeatsDict.get(
                max(reversedSeatsDict))]
            i += 1

    # print(SeatsDict)
    diff = lastVoteNum-nextPotentialVoteNum
    for seatNum in gatheredSeats[newMax]:
        diff *= seatNum
    print(
        f"do zdobycia mijesca zabrałko {int(diff)} głosów")
    return SeatsDict, currentMax, newMax


def SainteLague(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum):
    SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                 "Lewica": 0, "Konfederacja": 0}
    reversedSeatsDict = {PiS: "PiS", KO: "KO", TD: "Trzecia Droga",
                         Lewica: "Lewica", Konf: "Konfederacja"}
    VoteDict = {"PiS": PiS, "KO": KO, "Trzecia Droga": TD,
                "Lewica": Lewica, "Konfederacja": Konf}
    gatheredSeats = {"PiS": [], "KO": [], "Trzecia Droga": [],
                     "Lewica": [], "Konfederacja": []}
    currentMax = ""
    newMax = ""
    lastVoteNum = 0
    nextPotentialVoteNum = 0
    for seat in range(0, seatsNum, 1):
        SeatsDict[reversedSeatsDict.get(max(reversedSeatsDict))] += 1
        val = SeatsDict[reversedSeatsDict.get(max(reversedSeatsDict))]
        currentMax = reversedSeatsDict.get(max(reversedSeatsDict))
        lastVoteNum = VoteDict[reversedSeatsDict.get(
            max(reversedSeatsDict))]
        VoteDict[reversedSeatsDict.get(max(reversedSeatsDict))] /= ((val*2)+1)
        gatheredSeats[currentMax].append(((val*2)+1))
        reversedSeatsDict = {}
        reversedSeatsDict = {VoteDict['PiS']: "PiS", VoteDict['KO']: "KO", VoteDict['Trzecia Droga']: "Trzecia Droga",
                             VoteDict["Lewica"]: "Lewica", VoteDict["Konfederacja"]: "Konfederacja"}
        newMax = reversedSeatsDict.get(max(reversedSeatsDict))
        nextPotentialVoteNum = VoteDict[reversedSeatsDict.get(
            max(reversedSeatsDict))]
    diff = lastVoteNum-nextPotentialVoteNum
    for seatNum in gatheredSeats[newMax]:
        diff *= seatNum
    print(
        f"do zdobycia mijesca zabrałko {int(diff)} głosów")
    return SeatsDict, currentMax, newMax
