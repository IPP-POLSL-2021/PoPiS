from Controller import electionCalc


def chooseMethods(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum, method):
    SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                 "Lewica": 0, "Konfederacja": 0}
    VoteDict = {"PiS": PiS, "KO": KO, "Trzecia Droga": TD,
                "Lewica": Lewica, "Konfederacja": Konf}
    match method:
        case "d'Hondta":
            recivedVotes = electionCalc.dhont(
                SeatsDict, VoteDict, seatsNum)
            SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                         "Lewica": 0, "Konfederacja": 0}
            nextSeat = electionCalc.dhont(SeatsDict, VoteDict, seatsNum+1)
            SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                         "Lewica": 0, "Konfederacja": 0}
            prevSeat = electionCalc.dhont(SeatsDict, VoteDict, seatsNum-1)
            # return dhont(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum)
            differencesNxt = {key
                              for key in nextSeat if recivedVotes[key] != nextSeat[key]}
            differencesPrev = {key
                               for key in recivedVotes if recivedVotes[key] != prevSeat[key]}
            return recivedVotes, differencesNxt, differencesPrev
        case "Sainte-Laguë":
            recivedVotes = electionCalc.SainteLaguë(
                SeatsDict, VoteDict, seatsNum)
            SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                         "Lewica": 0, "Konfederacja": 0}
            nextSeat = electionCalc.SainteLaguë(
                SeatsDict, VoteDict, seatsNum+1)
            SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                         "Lewica": 0, "Konfederacja": 0}
            prevSeat = electionCalc.SainteLaguë(
                SeatsDict, VoteDict, seatsNum-1)
            # return dhont(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum)
            differencesNxt = {key
                              for key in nextSeat if recivedVotes[key] != nextSeat[key]}
            differencesPrev = {key
                               for key in recivedVotes if recivedVotes[key] != prevSeat[key]}
            return recivedVotes, differencesNxt, differencesPrev
        case "Kwota Hare’a (metoda największych reszt)":
            recivedVotes = electionCalc.HareDrop(
                SeatsDict, VoteDict, seatsNum, Freq)
            SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                         "Lewica": 0, "Konfederacja": 0}
            nextSeat = electionCalc.HareDrop(
                SeatsDict, VoteDict, seatsNum+1, Freq)
            SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                         "Lewica": 0, "Konfederacja": 0}
            prevSeat = electionCalc.HareDrop(
                SeatsDict, VoteDict, seatsNum-1, Freq)
            # return dhont(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum)
            differencesNxt = {key
                              for key in nextSeat if recivedVotes[key] != nextSeat[key]}
            differencesPrev = {key
                               for key in recivedVotes if recivedVotes[key] != prevSeat[key]}
            return recivedVotes, differencesNxt, differencesPrev
        case "Kwota Hare’a (metoda najmniejszych reszt)":
            recivedVotes = electionCalc.HareDrop(
                SeatsDict, VoteDict, seatsNum, Freq, False)
            SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                         "Lewica": 0, "Konfederacja": 0}
            nextSeat = electionCalc.HareDrop(
                SeatsDict, VoteDict, seatsNum+1, Freq, False)
            SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
                         "Lewica": 0, "Konfederacja": 0}
            prevSeat = electionCalc.HareDrop(
                SeatsDict, VoteDict, seatsNum-1, Freq, False)
            # return dhont(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum)
            differencesNxt = {key
                              for key in nextSeat if recivedVotes[key] != nextSeat[key]}
            differencesPrev = {key
                               for key in recivedVotes if recivedVotes[key] != prevSeat[key]}
            return recivedVotes, differencesNxt, differencesPrev


# def HareDrop(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum, biggest=True):
#     SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
#                  "Lewica": 0, "Konfederacja": 0}
#     orgPiS = PiS
#     orgKO = KO
#     orgTD = TD
#     orgLw = Lewica
#     orgKf = Konf
#     VoteDict = {"PiS": PiS, "KO": KO, "Trzecia Droga": TD,
#                 "Lewica": Lewica, "Konfederacja": Konf}
#     reversedSeatsDict = {PiS: "PiS", KO: "KO", TD: "Trzecia Droga",
#                          Lewica: "Lewica", Konf: "Konfederacja"}
#     PiS = (PiS*seatsNum)/Freq
#     KO = (KO*seatsNum)/Freq
#     TD = (TD*seatsNum)/Freq
#     Lewica = (Lewica*seatsNum)/Freq
#     Konf = (Konf*seatsNum)/Freq
#     SeatsDict["PiS"] = int(PiS)
#     SeatsDict["KO"] = int(KO)
#     SeatsDict["Trzecia Droga"] = int(TD)
#     SeatsDict["Lewica"] = int(Lewica)
#     SeatsDict["Konfederacja"] = int(Konf)
#     remainingSeats = seatsNum-(int(PiS)+int(KO)+int(TD)+int(Lewica)+int(Konf))
#     if remainingSeats == 0:
#         return SeatsDict,  SeatsDict[reversedSeatsDict.get(max(reversedSeatsDict))], " jeszcze nie zaimplementowano"
#     PiS -= int(PiS)
#     KO -= int(KO)
#     Konf -= int(Konf)
#     Lewica -= int(Lewica)
#     TD -= int(TD)
#     VoteDict = {"PiS": PiS, "KO": KO, "Trzecia Droga": TD,
#                 "Lewica": Lewica, "Konfederacja": Konf}
#     reversedSeatsDict = {PiS: "PiS", KO: "KO", TD: "Trzecia Droga",
#                          Lewica: "Lewica", Konf: "Konfederacja"}
#     currentMax = ""

#     for a in range(0, remainingSeats, 1):
#         if biggest is True:
#             SeatsDict[reversedSeatsDict.get(max(reversedSeatsDict))] += 1
#             currentMax = reversedSeatsDict.get(max(reversedSeatsDict))
#             VoteDict[reversedSeatsDict.get(max(reversedSeatsDict))] = 0
#         else:
#             SeatsDict[reversedSeatsDict.get(min(reversedSeatsDict))] += 1
#             currentMax = reversedSeatsDict.get(min(reversedSeatsDict))
#             VoteDict[reversedSeatsDict.get(min(reversedSeatsDict))] = 0
#         reversedSeatsDict = {VoteDict['PiS']: "PiS", VoteDict['KO']: "KO", VoteDict['Trzecia Droga']: "Trzecia Droga",
#                              VoteDict["Lewica"]: "Lewica", VoteDict["Konfederacja"]: "Konfederacja"}
#     return SeatsDict,  currentMax, " jeszcze nie zaimplementowano"


# def dhont(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum):
#     i = 2
#     SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
#                  "Lewica": 0, "Konfederacja": 0}
#     reversedSeatsDict = {PiS: "PiS", KO: "KO", TD: "Trzecia Droga",
#                          Lewica: "Lewica", Konf: "Konfederacja"}
#     VoteDict = {"PiS": PiS, "KO": KO, "Trzecia Droga": TD,
#                 "Lewica": Lewica, "Konfederacja": Konf}
#     gatheredSeats = {"PiS": [], "KO": [], "Trzecia Droga": [],
#                      "Lewica": [], "Konfederacja": []}
#     currentMax = ""
#     newMax = ""
#     lastVoteNum = 0
#     nextPotentialVoteNum = 0
#     if type == "ilościowy":

#         for seat in range(0, seatsNum, 1):
#             SeatsDict[reversedSeatsDict.get(max(reversedSeatsDict))] += 1
#             currentMax = reversedSeatsDict.get(max(reversedSeatsDict))
#             lastVoteNum = VoteDict[reversedSeatsDict.get(
#                 max(reversedSeatsDict))]

#             VoteDict[reversedSeatsDict.get(max(reversedSeatsDict))] /= i
#             gatheredSeats[currentMax].append(i)
#             reversedSeatsDict = {}
#             reversedSeatsDict = {VoteDict['PiS']: "PiS", VoteDict['KO']: "KO", VoteDict['Trzecia Droga']: "Trzecia Droga",
#                                  VoteDict["Lewica"]: "Lewica", VoteDict["Konfederacja"]: "Konfederacja"}
#             newMax = reversedSeatsDict.get(max(reversedSeatsDict))
#             nextPotentialVoteNum = VoteDict[reversedSeatsDict.get(
#                 max(reversedSeatsDict))]
#             i += 1

#     # print(SeatsDict)
#     diff = lastVoteNum-nextPotentialVoteNum
#     for seatNum in gatheredSeats[newMax]:
#         diff *= seatNum
#     print(
#         f"Do zdobycia mandatu zabrakło {int(diff)} głosów")
#     return SeatsDict, currentMax, newMax


# def SainteLague(PiS, KO, TD, Lewica, Konf, Freq, type, seatsNum):
#     SeatsDict = {"PiS": 0, "KO": 0, "Trzecia Droga": 0,
#                  "Lewica": 0, "Konfederacja": 0}
#     reversedSeatsDict = {PiS: "PiS", KO: "KO", TD: "Trzecia Droga",
#                          Lewica: "Lewica", Konf: "Konfederacja"}
#     VoteDict = {"PiS": PiS, "KO": KO, "Trzecia Droga": TD,
#                 "Lewica": Lewica, "Konfederacja": Konf}
#     gatheredSeats = {"PiS": [], "KO": [], "Trzecia Droga": [],
#                      "Lewica": [], "Konfederacja": []}
#     currentMax = ""
#     newMax = ""
#     lastVoteNum = 0
#     nextPotentialVoteNum = 0
#     for seat in range(0, seatsNum, 1):
#         SeatsDict[reversedSeatsDict.get(max(reversedSeatsDict))] += 1
#         val = SeatsDict[reversedSeatsDict.get(max(reversedSeatsDict))]
#         currentMax = reversedSeatsDict.get(max(reversedSeatsDict))
#         lastVoteNum = VoteDict[reversedSeatsDict.get(
#             max(reversedSeatsDict))]
#         VoteDict[reversedSeatsDict.get(max(reversedSeatsDict))] /= ((val*2)+1)
#         gatheredSeats[currentMax].append(((val*2)+1))
#         reversedSeatsDict = {}
#         reversedSeatsDict = {VoteDict['PiS']: "PiS", VoteDict['KO']: "KO", VoteDict['Trzecia Droga']: "Trzecia Droga",
#                              VoteDict["Lewica"]: "Lewica", VoteDict["Konfederacja"]: "Konfederacja"}
#         newMax = reversedSeatsDict.get(max(reversedSeatsDict))
#         nextPotentialVoteNum = VoteDict[reversedSeatsDict.get(
#             max(reversedSeatsDict))]
#     diff = lastVoteNum-nextPotentialVoteNum
#     for seatNum in gatheredSeats[newMax]:
#         diff *= seatNum
#     print(
#         f"Do zdobycia mandatu zabrakło {int(diff)} głosów")
#     return SeatsDict, currentMax, newMax
