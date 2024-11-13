import streamlit as st
from Controller import seatsCalculator
import json


def clearJSON(clearDict):
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(clearDict, json_file,
                  ensure_ascii=False, indent=4)


def loadView():
    # print("huj")
    lastParty = ""
    nextParty = ""
    diff = 0
    frequency = 0
    clublist = []
    votesDict = {'PiS': 0, 'KO': 0, 'Trzecia Droga': 0, 'Lewica': 0,
                 'Konfederacja': 0, 'Frekwencja': 0, 'Miejsca do zdobycia': 0, 'Uzupełniono': False}
    districtsDict = {'Legnica': {}, 'Wałbrzych': {},
                     'Wrocław': {}, 'Bydgoszcz': {}, 'Toruń': {}, 'Lublin': {}, 'Chełm': {}, 'Zielona Góra': {}, 'Łódź': {},
                     'Piotrków Trybunalski': {}, 'Sieradz': {}, 'Chrzanów': {}, 'Kraków': {}, 'Nowy Sącz': {},
                     'Tarnów': {}, 'Płock': {}, 'Radom': {}, 'Siedlce': {}, 'Warszawa': {}, 'Warszawa 2': {}, 'Opole': {},
                     'Krosno': {}, 'Rzeszów': {}, 'Białystok': {}, 'Gdańsk': {},
                     'Słupsk': {}, 'Bielsko-Biała': {}, 'Częstochowa': {},
                     'Gliwice': {}, 'Rybnik': {}, 'Katowice': {}, 'Sosnowiec': {}, 'Kielce': {}, 'Elbląg': {}, 'Olsztyn': {},
                     'Kalisz': {}, 'Konin': {}, 'Piła': {}, 'Poznań': {}, 'Koszalin': {}, 'Szczecin': {}}
    seats = [12, 8, 14, 12, 13, 15, 12, 12, 10, 9, 12, 8, 14, 10, 9, 10, 9, 12, 20,
             12, 12, 11, 15, 14, 12, 14, 9, 7, 9, 9, 12, 9, 16, 8, 10, 12, 9, 9, 10, 8, 12]

    i = 0

    for dist in districtsDict:
        votesDict['Miejsca do zdobycia'] = seats[i]
        districtsDict[dist] = votesDict.copy()
        i += 1
    seatsDistricstsDict = districtsDict
    votesNumber = seatsDistricstsDict
    loaded_data = {}
    loaded_votes = seatsDistricstsDict

    print(loaded_votes)
    pis = 0
    ko = 0
    td = 0
    lw = 0
    kf = 0
    type = st.selectbox("rodzaj głosów", ["ilościowy", "procentowy"])
    with st.form("kalkulator mandatów w sejmie"):
        st.write("wybierz okrąg który chcesz uzupełnić")
        method = st.selectbox("metoda liczenia głosów", [
                              "d'Hondt", "Sainte-Laguë", "Kwota Hare’a (metoda największych reszt)", "Kwota Hare’a (metoda najmniejszych reszt)"])
        # if resestAll:
        #     clearJSON(seatsDistricstsDict)
        district = st.selectbox("wybierz okręg który chcesz uzupełnić",
                                districtsDict.keys())
        val = districtsDict[district]
        seatsNum = val['Miejsca do zdobycia']
        st.write(f"w tym okręgu jest do rozdania {seatsNum} mandatów")
        st.write("Uzupełnij ilość głosów otrzymanych przez partie")
        pis = st.number_input("głosy parti PiS", 0)
        ko = st.number_input("głosy parti KO", 0)
        td = st.number_input("głosy parti Trzecia Droga", 0)
        lw = st.number_input("głosy  parti Lewica", 0)
        kf = st.number_input("głosy parti Konfederacja", 0)
        if type == "procentowy":
            frequency = st.number_input("frekwencja", 0)
        else:
            frequency = pis+ko+td+lw+kf

        submitted = st.form_submit_button("Licz")
        if submitted:
            val = districtsDict[district]
            val['PiS'] = pis
            val['KO'] = ko
            val['Trzecia Droga'] = td
            val['Lewica'] = lw
            val['Konfederacja'] = kf
            if type == "procentowy":
                val['Frekwencja'] = frequency
                if pis+ko+td+lw+kf != 100:
                    st.warning("Wyniki powinny sumować się do 100%")
                else:
                    procent = frequency/100
                    newSeats, lastParty, nextParty = seatsCalculator.chooseMethod(
                        pis*procent, ko*procent, td*procent, lw*procent, kf*procent, val['Frekwencja'], "ilościowy", seatsNum, method)
                    votesNumber[district]['PiS'] = pis*procent
                    votesNumber[district]['KO'] = ko*procent
                    votesNumber[district]['Trzecia Droga'] = td*procent
                    votesNumber[district]['Lewica'] = lw*procent
                    votesNumber[district]['Konfederacja'] = kf*procent
                    with open("data.json", "r", encoding="utf-8") as json_file:
                        loaded_data = json.load(json_file)
                        loaded_data[district]['PiS'] = newSeats['PiS']
                        loaded_data[district]['KO'] = newSeats['KO']
                        loaded_data[district]['Trzecia Droga'] = newSeats['Trzecia Droga']
                        loaded_data[district]['Lewica'] = newSeats['Lewica']
                        loaded_data[district]['Konfederacja'] = newSeats['Konfederacja']

                    with open("votes.json", "r", encoding="utf-8") as json_file:
                        loaded_votes = json.load(json_file)
                        loaded_votes[district]['PiS'] = votesNumber[district]['PiS']
                        loaded_votes[district]['KO'] = votesNumber[district]['KO']
                        loaded_votes[district]['Trzecia Droga'] = votesNumber[district]['Trzecia Droga']
                        loaded_votes[district]['Lewica'] = votesNumber[district]['Lewica']
                        loaded_votes[district]['Konfederacja'] = votesNumber[district]['Konfederacja']

                    with open("data.json", "w", encoding="utf-8") as json_file:
                        json.dump(loaded_data, json_file,
                                  ensure_ascii=False, indent=4)
                    with open("votes.json", "w", encoding="utf-8") as json_file:
                        json.dump(loaded_votes, json_file,
                                  ensure_ascii=False, indent=4)
                    st.write(newSeats)

            else:
                val['Frekwencja'] = pis+ko+td+lw+kf
                newSeats, lastParty, nextParty = seatsCalculator.chooseMethod(
                    pis, ko, td, lw, kf, val['Frekwencja'], "ilościowy", seatsNum, method)

                with open("data.json", "r", encoding="utf-8") as json_file:
                    loaded_data = json.load(json_file)
                with open("votes.json", "r", encoding="utf-8") as json_file:
                    loaded_votes = json.load(json_file)
                loaded_data[district]['PiS'] = newSeats['PiS']
                loaded_data[district]['KO'] = newSeats['KO']
                loaded_data[district]['Trzecia Droga'] = newSeats['Trzecia Droga']
                loaded_data[district]['Lewica'] = newSeats['Lewica']
                loaded_data[district]['Konfederacja'] = newSeats['Konfederacja']
                loaded_data[district]['Frekwencja'] = frequency
                loaded_votes[district]['PiS'] = votesNumber[district]['PiS']
                loaded_votes[district]['KO'] = votesNumber[district]['KO']
                loaded_votes[district]['Trzecia Droga'] = votesNumber[district]['Trzecia Droga']
                loaded_votes[district]['Lewica'] = votesNumber[district]['Lewica']
                loaded_votes[district]['Konfederacja'] = votesNumber[district]['Konfederacja']

                # print(frequency)
                loaded_data[district]['Uzupełniono'] = True
                with open("data.json", "w", encoding="utf-8") as json_file:
                    json.dump(loaded_data, json_file,
                              ensure_ascii=False, indent=4)
                with open("votes.json", "w", encoding="utf-8") as json_file:
                    json.dump(loaded_votes, json_file,
                              ensure_ascii=False, indent=4)
                st.write(newSeats)
                st.write(
                    f"Partia która zdobyła ostatni mandat w okręgu to {lastParty} a kolejny zdobyła by partia {nextParty}")
    resestAll = st.button("wyczyść wszystkie dane")
    if resestAll:
        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump(seatsDistricstsDict, json_file,
                      ensure_ascii=False, indent=4)
        with open("votes.json", "w", encoding="utf-8") as json_file:
            json.dump(loaded_votes, json_file,
                      ensure_ascii=False, indent=4)
    # print(seatsDistricstsDict['Gliwice'])

    # print(districtsDict)
    votesDict = {'PiS': 0, 'KO': 0, 'Trzecia Droga': 0, 'Lewica': 0,
                 'Konfederacja': 0, 'Frekwencja': 0}
    votesDictProcent = {'PiS': 0, 'KO': 0, 'Trzecia Droga': 0, 'Lewica': 0,
                        'Konfederacja': 0}
    emptyDistrictDict = {}
    for region in loaded_data:

        votesDict['KO'] += loaded_data[region]['KO']
        votesDict['PiS'] += loaded_data[region]['PiS']
        votesDict['Trzecia Droga'] += loaded_data[region]['Trzecia Droga']
        votesDict['Lewica'] += loaded_data[region]['Lewica']
        votesDict['Konfederacja'] += loaded_data[region]['Konfederacja']
        votesDict['Frekwencja'] += loaded_data[region]['Frekwencja']
        votesDictProcent['KO'] += loaded_votes[region]['KO']
        votesDictProcent['PiS'] += loaded_votes[region]['PiS']
        votesDictProcent['Trzecia Droga'] += loaded_votes[region]['Trzecia Droga']
        votesDictProcent['Lewica'] += loaded_votes[region]['Lewica']
        votesDictProcent['Konfederacja'] += loaded_votes[region]['Konfederacja']
        if loaded_data[region]['Uzupełniono'] is False:
            emptyDistrictDict[region] = 1
            # print(region)
    st.write(votesDict)
    if votesDictProcent['KO'] > 0:
        votesDictProcent['KO'] /= votesDict['Frekwencja']/100
        votesDictProcent['KO'] = round(votesDictProcent['KO'], 2)
    if votesDictProcent['PiS'] > 0:
        votesDictProcent['PiS'] /= votesDict['Frekwencja']/100
        votesDictProcent['PiS'] = round(votesDictProcent['PiS'], 2)
    if votesDictProcent['Trzecia Droga'] > 0:
        votesDictProcent['Trzecia Droga'] /= votesDict['Frekwencja']/100
        votesDictProcent['Trzecia Droga'] = round(
            votesDictProcent['Trzecia Droga'], 2)

    if votesDictProcent['Lewica'] > 0:
        votesDictProcent['Lewica'] /= votesDict['Frekwencja']/100
        votesDictProcent['Lewica'] = round(votesDictProcent['Lewica'], 2)

    if votesDictProcent['Konfederacja'] > 0:
        votesDictProcent['Konfederacja'] /= votesDict['Frekwencja']/100
        votesDictProcent['Konfederacja'] = round(
            votesDictProcent['Konfederacja'], 2)
    for key in votesDictProcent.keys():
        st.write(
            f"Na podstawie wprowadzonych wyników partia: {key} uzyskała wynik na poziomie: {votesDictProcent[key]}%")
    # st.write(f"wyniki w skali kraju: {votesDictProcent}")
    keys = str(list(emptyDistrictDict.keys())).removeprefix(
        "[").removesuffix("]").replace("'", "")

    st.write(
        f"regiony pozostające do uzupełnienia to {keys}")
