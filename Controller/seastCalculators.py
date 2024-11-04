def dhont(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum):
    i = 2
    SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                 "Lewica": 0, "Konfederacja": 0}
    reversedSeatsDict = {PiS: "PiS", KO: "KO", TD: "Trzecia Droga",
                         Lewica: "Lewica", Konf: "Konfederacja"}
    VoteDict = {"PiS": PiS, "KO": KO, "Trzecia Droga": TD,
                "Lewica": Lewica, "Konfederacja": Konf}
    if type == "ilościowy":

        for seat in range(0, seatsNum, 1):
            SeatsDict[reversedSeatsDict.get(max(reversedSeatsDict))] += 1
            VoteDict[reversedSeatsDict.get(max(reversedSeatsDict))] /= i
            reversedSeatsDict = {}
            reversedSeatsDict = {VoteDict['PiS']: "PiS", VoteDict['KO']: "KO", VoteDict['Trzecia Droga']: "Trzecia Droga",
                                 VoteDict["Lewica"]: "Lewica", VoteDict["Konfederacja"]: "Konfederacja"}
            i += 1
    # print(SeatsDict)
    return SeatsDict
