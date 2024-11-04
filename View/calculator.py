import streamlit as st
from Controller import seastCalculators
import json


def clearJSON(clearDict):
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(clearDict, json_file,
                  ensure_ascii=False, indent=4)


def loadView():
    # print("huj")
    clublist = []
    votesDict = {'PiS': 0, 'KO': 0, 'Trzecia Droga': 0, 'Lewica': 0,
                 'Konfederacja': 0, 'Frekwencja': 0, 'Miejsca do zdobycia': 0}
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
    st.write("pusto")
    i = 0

    for dist in districtsDict:
        votesDict['Miejsca do zdobycia'] = seats[i]
        districtsDict[dist] = votesDict.copy()
        i += 1
    seatsDistricstsDict = districtsDict
    loaded_data = {}
    type = st.selectbox("rodzaj głosów", ["ilościowy", "procętowy"])
    with st.form("kalkulaotr miejsc w sejmie"):
        st.write("wybierz okrąg który chcesz uzupełnić")

        # if resestAll:
        #     clearJSON(seatsDistricstsDict)
        district = st.selectbox("wybierz okrąg który chcesz uzupełnić",
                                districtsDict.keys())
        val = districtsDict[district]
        seatsNum = val['Miejsca do zdobycia']
        st.write(f"w tym okręgu jest do rozdania {seatsNum} miejsc")
        st.write("Uzupełnij ilośc głosów otrzymanych przez partie")
        pis = st.number_input("mijesca parti PiS", 0)
        ko = st.number_input("mijesca parti KO", 0)
        td = st.number_input("mijesca parti Trzecia Droga", 0)
        lw = st.number_input("mijesca parti Lewica", 0)
        kf = st.number_input("mijesca parti Konfederacja", 0)
        if type == "procętowy":
            frequency = st.number_input("frekwencja", 0)

        submitted = st.form_submit_button("Licz")
        if submitted:
            val = districtsDict[district]
            val['PiS'] = pis
            val['KO'] = ko
            val['Trzecia Droga'] = td
            val['Lewica'] = lw
            val['Konfederacja'] = kf
            if type == "procętowy":
                val['Frekwencja'] = frequency
                if pis+ko+td+lw+kf != 100:
                    st.warning("Wyniki powinny sumować się do 100%")
                else:
                    procent = frequency/100
                    newSeats = seastCalculators.dhont(
                        pis*procent, ko*procent, td*procent, lw*procent, kf*procent, val['Frekwencja'], "ilościowy", seatsNum)
                    with open("data.json", "r", encoding="utf-8") as json_file:
                        loaded_data = json.load(json_file)
                        loaded_data[district]['PiS'] = newSeats['PiS']
                        loaded_data[district]['KO'] = newSeats['KO']
                        loaded_data[district]['Trzecia Droga'] = newSeats['Trzecia Droga']
                        loaded_data[district]['Lewica'] = newSeats['Lewica']
                        loaded_data[district]['Konfederacja'] = newSeats['Konfederacja']
                    with open("data.json", "w", encoding="utf-8") as json_file:
                        json.dump(loaded_data, json_file,
                                  ensure_ascii=False, indent=4)
                    st.write(newSeats)

            else:
                val['Frekwencja'] = pis+ko+td+lw+kf
                newSeats = seastCalculators.dhont(
                    pis, ko, td, lw, kf, val['Frekwencja'], "ilościowy", seatsNum)
                # districtResults = seatsDistricstsDict[district]
                # trzeba by to gdzeiś przekazać np do pliku aby nie tracić danych
                # seatsDistricstsDict[district]['PiS'] = newSeats['PiS']
                # seatsDistricstsDict[district]['KO'] = newSeats['KO']
                # seatsDistricstsDict[district]['Trzecia Droga'] = newSeats['Trzecia Droga']
                # seatsDistricstsDict[district]['Lewica'] = newSeats['Lewica']
                # seatsDistricstsDict[district]['Konfederacja'] = newSeats['Konfederacja']
                # seatsDistricstsDict[district] = districtResults
                # districtsDict[district] = val
                # print("dupa")
                with open("data.json", "r", encoding="utf-8") as json_file:
                    loaded_data = json.load(json_file)
                loaded_data[district]['PiS'] = newSeats['PiS']
                loaded_data[district]['KO'] = newSeats['KO']
                loaded_data[district]['Trzecia Droga'] = newSeats['Trzecia Droga']
                loaded_data[district]['Lewica'] = newSeats['Lewica']
                loaded_data[district]['Konfederacja'] = newSeats['Konfederacja']
                with open("data.json", "w", encoding="utf-8") as json_file:
                    json.dump(loaded_data, json_file,
                              ensure_ascii=False, indent=4)
                st.write(newSeats)
    resestAll = st.button("wyczyść wszystkie dane")
    if resestAll:
        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump(seatsDistricstsDict, json_file,
                      ensure_ascii=False, indent=4)
    # print(seatsDistricstsDict['Gliwice'])

    # print(districtsDict)
    votesDict = {'PiS': 0, 'KO': 0, 'Trzecia Droga': 0, 'Lewica': 0,
                 'Konfederacja': 0, 'Frekwencja': 0, 'Miejsca do zdobycia': 0}
    for region in loaded_data:

        votesDict['KO'] += loaded_data[region]['KO']
        votesDict['PiS'] += loaded_data[region]['PiS']
        votesDict['Trzecia Droga'] += loaded_data[region]['Trzecia Droga']
        votesDict['Lewica'] += loaded_data[region]['Lewica']
        votesDict['Konfederacja'] += loaded_data[region]['Konfederacja']
    st.write(votesDict)
