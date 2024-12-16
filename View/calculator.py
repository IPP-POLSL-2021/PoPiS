import streamlit as st
from Controller import seatsCalculator
import json
import pandas as pd
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import os
from shapely.geometry import Point
from math import radians, cos, sin, asin, sqrt
from Controller import electionCalc
# import numpy as np


def clearJSON(clearDict):
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(clearDict, json_file,
                  ensure_ascii=False, indent=4)


def loadView():
    # print("huj")
    # districtcMap = "Legnica"
    tab1, tab2 = st.tabs(
        ["Wyniki rzeczywiste", "Wyniki własne"])
    with tab2:

        lastParty = ""
        nextParty = ""
        diff = 0

        frequency = 0

        # val = ""
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
        val = ""
        for dist in districtsDict:
            votesDict['Miejsca do zdobycia'] = seats[i]
            districtsDict[dist] = votesDict.copy()
            i += 1
        seatsDistricstsDict = districtsDict
        votesNumber = seatsDistricstsDict
        loaded_data = {}
        loaded_votes = seatsDistricstsDict
        # Don't bloat the terminal
        # print(loaded_votes)
        pis = 0
        ko = 0
        td = 0
        lw = 0
        kf = 0

        political_parties = ["PiS", "KO",
                             "Trzecia Droga", "Konfederacja", "Lewica"]

        with st.form("kalkulator mandatów do Sejmu"):
            type = st.selectbox(
                "rodzaj głosów", ["ilościowy", "procentowy"])
            st.write("wybierz okręg który chcesz uzupełnić")
            method = st.selectbox("metoda liczenia głosów", [
                "d'Hondta", "Sainte-Laguë", "Kwota Hare’a (metoda największych reszt)", "Kwota Hare’a (metoda najmniejszych reszt)"])
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
                # val = districtsDict[district]
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
                        newSeats, lastParty, nextParty = seatsCalculator.chooseMethods(
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
                    seatsResult = seatsCalculator.chooseMethods(
                        pis, ko, td, lw, kf, val['Frekwencja'], "ilościowy", seatsNum, method)
                    newSeats = seatsResult[0]
                    lastParty = seatsResult[1]
                    nextParty = seatsResult[2]
                    with open("data.json", "r", encoding="utf-8") as json_file:
                        loaded_data = json.load(json_file)
                    with open("votes.json", "r", encoding="utf-8") as json_file:
                        loaded_votes = json.load(json_file)
                    for element in political_parties:
                        if element != 'Frekwencja':
                            loaded_data[district][element] = newSeats[element]

                            loaded_votes[district][element] = votesNumber[district][element]

                    # loaded_data[district]['PiS'] = newSeats['PiS']
                    # loaded_data[district]['KO'] = newSeats['KO']
                    # loaded_data[district]['Trzecia Droga'] = newSeats['Trzecia Droga']
                    # loaded_data[district]['Lewica'] = newSeats['Lewica']
                    # loaded_data[district]['Konfederacja'] = newSeats['Konfederacja']
                    loaded_data[district]['Frekwencja'] = frequency
                    # loaded_votes[district]['PiS'] = votesNumber[district]['PiS']
                    # loaded_votes[district]['KO'] = votesNumber[district]['KO']
                    # loaded_votes[district]['Trzecia Droga'] = votesNumber[district]['Trzecia Droga']
                    # loaded_votes[district]['Lewica'] = votesNumber[district]['Lewica']
                    # loaded_votes[district]['Konfederacja'] = votesNumber[district]['Konfederacja']

                    # print(frequency)
                    loaded_data[district]['Uzupełniono'] = True
                    with open("data.json", "w", encoding="utf-8") as json_file:
                        json.dump(loaded_data, json_file,
                                  ensure_ascii=False, indent=4)
                    with open("votes.json", "w", encoding="utf-8") as json_file:
                        json.dump(loaded_votes, json_file,
                                  ensure_ascii=False, indent=4)
                    st.dataframe(newSeats)
                    st.write(
                        f"Partia która zdobyła ostatni mandat w okręgu to {str(lastParty).removeprefix('{').removesuffix('}')} a kolejny zdobyła by partia {str(nextParty).removeprefix('{').removesuffix('}')}")

            # if "observables_initialized" not in st.session_state:
            #     setup_observers()
            #     st.session_state["observables_initialized"] = True

        resestAll = st.button("Wyczyść wszystkie dane")
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
            for element in political_parties:
                if element != 'Frekwencja':
                    votesDict[element] += loaded_data[region][element]

                    votesDictProcent[element] += loaded_votes[region][element]

            # votesDict['KO'] += loaded_data[region]['KO']
            # votesDict['PiS'] += loaded_data[region]['PiS']
            # votesDict['Trzecia Droga'] += loaded_data[region]['Trzecia Droga']
            # votesDict['Lewica'] += loaded_data[region]['Lewica']
            # votesDict['Konfederacja'] += loaded_data[region]['Konfederacja']
            votesDict['Frekwencja'] += loaded_data[region]['Frekwencja']
            # votesDictProcent['KO'] += loaded_votes[region]['KO']
            # votesDictProcent['PiS'] += loaded_votes[region]['PiS']
            # votesDictProcent['Trzecia Droga'] += loaded_votes[region]['Trzecia Droga']
            # votesDictProcent['Lewica'] += loaded_votes[region]['Lewica']
            # votesDictProcent['Konfederacja'] += loaded_votes[region]['Konfederacja']
            if loaded_data[region]['Uzupełniono'] is False:
                emptyDistrictDict[region] = 1
                # print(region)
        for element in political_parties:
            if votesDictProcent[element] > 0:
                votesDictProcent[element] /= votesDict['Frekwencja']/100
                votesDictProcent[element] = round(votesDictProcent[element], 2)
        # if votesDictProcent['KO'] > 0:
        #     votesDictProcent['KO'] /= votesDict['Frekwencja']/100
        #     votesDictProcent['KO'] = round(votesDictProcent['KO'], 2)
        # if votesDictProcent['PiS'] > 0:
        #     votesDictProcent['PiS'] /= votesDict['Frekwencja']/100
        #     votesDictProcent['PiS'] = round(votesDictProcent['PiS'], 2)
        # if votesDictProcent['Trzecia Droga'] > 0:
        #     votesDictProcent['Trzecia Droga'] /= votesDict['Frekwencja']/100
        #     votesDictProcent['Trzecia Droga'] = round(
        #         votesDictProcent['Trzecia Droga'], 2)

        # if votesDictProcent['Lewica'] > 0:
        #     votesDictProcent['Lewica'] /= votesDict['Frekwencja']/100
        #     votesDictProcent['Lewica'] = round(votesDictProcent['Lewica'], 2)

        # if votesDictProcent['Konfederacja'] > 0:
        #     votesDictProcent['Konfederacja'] /= votesDict['Frekwencja']/100
        #     votesDictProcent['Konfederacja'] = round(
        #         votesDictProcent['Konfederacja'], 2)
        col1, col2 = st.columns(2)
        with col1:

            st.dataframe(votesDict)
        with col2:
            for key in votesDictProcent.keys():
                st.write(
                    f"Na podstawie wprowadzonych wyników partia: {key} uzyskała wynik na poziomie: {votesDictProcent[key]}%")
        # st.write(f"wyniki w skali kraju: {votesDictProcent}")
        keys = str(list(emptyDistrictDict.keys())).removeprefix(
            "[").removesuffix("]").replace("'", "")

        st.write(
            f"regiony pozostające do uzupełnienia to {keys}")
    with tab1:
        threshold, methodSelect, parties = st.columns(3)
        with threshold:
            voteingThreshold = st.number_input("próg wyborczy", 0, 100)
            voteingThresholdForCoaliton = st.number_input(
                "próg wyborczy dla koalicji", 0, 100)
        # st.write(electionCalc.calculateVotes(voteingThreshold))
        with methodSelect:
            # method = st.selectbox("metoda liczenia głosów", [
            #     "d'Hondt", "Sainte-Laguë", "Zmodyfikowany Sainte-Laguë", "Kwota Hare’a (metoda największych reszt)", "Kwota Hare’a (metoda najmniejszych reszt)"])
            year = st.selectbox("Wybierz rok wyborów", [
                                "2023", "2019", "2015", "2011", "2007", "2005", "2001"])

        qulifiedParties, allParitesDict, voteForDistrict = electionCalc.calculateVotes(
            voteingThreshold, voteingThresholdForCoaliton, year)
        allPrtiesDict2 = allParitesDict.copy()
        with parties:
            st.write(
                "Wybierz które partie mają być zwolnione z progu wyborczego (wg prawa komitety mniejszości narodowych i etnicznych)")
            with st.container(height=300):
                for key in allParitesDict:
                    if key != "Frekwencja":
                        allParitesDict[key] = st.checkbox(f"{key}", False)
                # Don't bloat terminal
                # print(allParitesDict)
                # w przyszłości jak zrobię lub ktoś zorobi słownik z wszysttkimi nazwami koitetów i ich krótami to się zastąpi

        # st.write(electionCalc.calculateVotes(voteingThreshold))
        for key in allParitesDict:
            if key != "Frekwencja" and allParitesDict[key] is True and key not in qulifiedParties:
                qulifiedParties.append(key)
                # ilość głosów tylko jej narzie nigdzie nie zwracam
        results = electionCalc.chooseMethod(
            qulifiedParties, voteForDistrict, year)

        # for party in results[key]:
        # if results[key][party] > 0:
        #     st.write(f" {party}: {results[key][party]}")

        filtered_results = {}
        for key in results.keys():
            filtered_results[key] = {party: votes for party,
                                     votes in results[key].items() if votes != 0}
            # st.write(f"{key}: ")

        FiltredResultsDF = pd.DataFrame.from_dict(filtered_results)
        FiltredResultsDF = FiltredResultsDF.fillna(value=" ")
        FiltredResultsDF = FiltredResultsDF.astype(str)
        FiltredResultsDF = FiltredResultsDF.replace(r'\.0$', ' ', regex=True)

        # st.table(FiltredResultsDF)

        FiltredResultsDF = FiltredResultsDF.transpose()
        FiltredResultsDF = FiltredResultsDF.rename(index={'dhont': "D'hondt"})
        st.table(FiltredResultsDF)
