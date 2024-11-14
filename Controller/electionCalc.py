import pandas


def calculateVotes(VotesNeeded):
    csvFile = pandas.read_csv(
        ' f"./Data/wyniki_gl_na_listy_po_okregach_sejm_utf8.csv", sep=";",  decimal=","')
    votes = {"Bezpartyjani Samorządowcy": 0, "KO": 0, "PiS": 0,
             "Lewica": 0, "Konfedereacja": 0, "Trzecia Droga": 0, "Frekwencja": 0}
    ClubsWithSeats = []
    for distric in csvFile:
        votes["Bezpartyjani Samorządowcy"] += csvFile["KOMITET WYBORCZY BEZPARTYJNI SAMORZĄDOWCY"]
        votes["Trzecia Droga"] += csvFile["KOALICYJNY KOMITET WYBORCZY TRZECIA DROGA POLSKA 2050 SZYMONA HOŁOWNI - POLSKIE STRONNICTWO LUDOWE"]
        votes["Lewica"] += csvFile["KOMITET WYBORCZY NOWA LEWICA"]
        votes["PiS"] += csvFile["KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ"]
        votes["Konfedereacja"] += csvFile["KOMITET WYBORCZY KONFEDERACJA WOLNOŚĆ I NIEPODLEGŁOŚĆ"]
        votes["KO"] += csvFile["KOALICYJNY KOMITET WYBORCZY KOALICJA OBYWATELSKA PO .N IPL ZIELONI"]
        votes["Frekwencja"] += csvFile["Liczba głosów ważnych oddanych łącznie na wszystkie listy kandydatów"]
    for key in votes.keys():
        result = votes[key]*100/votes
        if result >= VotesNeeded and key != "Frekwencja":
            ClubsWithSeats.append(key)
    return ClubsWithSeats
