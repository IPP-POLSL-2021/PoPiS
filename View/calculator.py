import streamlit as st
from Controller import seatsCalculator
import json
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import os
from shapely.geometry import Point
from math import radians, cos, sin, asin, sqrt
import streamlit as st
from Controller import electionCalc
import pandas as pd
# import numpy as np


class Observer:
    def update(self, observable, value):
        raise NotImplementedError("Subclass must implement 'update' method.")


class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, value):
        for observer in self._observers:
            observer.update(self, value)


class InputObserver(Observer):
    def update(self, observable, value):
        pass


print(os.getcwd())
SHAPEFILE_PATH = os.path.join("Data", "ne_10m_admin_0_countries.shp")
POLAND_NAME = "Poland"

CITY_COORDS = {
    'Legnica': (51.2070, 16.1551), 'Wałbrzych': (50.7717, 16.2843), 'Wrocław': (51.1079, 17.0385),
    'Bydgoszcz': (53.1235, 18.0104), 'Toruń': (53.0138, 18.5984), 'Lublin': (51.2465, 22.5684),
    'Chełm': (51.1431, 23.4751), 'Zielona Góra': (51.9356, 15.5058), 'Łódź': (51.7592, 19.4559),
    'Piotrków Trybunalski': (51.4059, 19.6799), 'Sieradz': (51.5951, 18.7306), 'Chrzanów': (50.1357, 19.3964),
    'Kraków': (50.0647, 19.9450), 'Nowy Sącz': (49.6212, 20.7034), 'Tarnów': (50.0139, 20.9860),
    'Płock': (52.5463, 19.6834), 'Radom': (51.4027, 21.1562), 'Siedlce': (52.1677, 22.2864),
    # Blisko oryginalnej Warszawy
    'Warszawa': (52.2097, 21.0022), 'Warszawa 2': (52.2407, 21.0280),
    'Opole': (50.6751, 17.9266), 'Krosno': (49.6883, 21.7681),
    'Rzeszów': (50.0413, 22.0017), 'Białystok': (53.1325, 23.1688), 'Gdańsk': (54.3520, 18.6466),
    'Słupsk': (54.4641, 17.0299), 'Bielsko-Biała': (49.8224, 19.0489), 'Częstochowa': (50.8118, 19.1223),
    'Gliwice': (50.2945, 18.6783), 'Rybnik': (50.1002, 18.5418), 'Katowice': (50.2649, 19.0258),
    'Sosnowiec': (50.2863, 19.1233), 'Kielce': (50.8661, 20.6275), 'Elbląg': (54.1522, 19.4064),
    'Olsztyn': (53.7784, 20.4942), 'Kalisz': (51.7612, 18.0910), 'Konin': (52.2236, 18.2514),
    'Piła': (53.1517, 16.7383), 'Poznań': (52.4064, 16.9252), 'Koszalin': (54.1944, 16.1814),
    'Szczecin': (53.4285, 14.5528)
}


def summary():
    print(0)


@st.cache_data
def load_shapefile(path):
    try:
        world = gpd.read_file(path)
        return world
    except Exception as e:
        # Nie pokazuj użytkownikom swoim błędów
        print(f"Error loading shapefile: {e}")
        # st.error(f"Error loading shapefile: {e}")
        return None


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * \
        cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


def get_nearest_city(click_lat, click_lng, threshold=5000):
    nearest_city = None
    min_distance = float('inf')
    for city, (lat, lng) in CITY_COORDS.items():
        distance = haversine_distance(click_lat, click_lng, lat, lng)
        if distance < min_distance and distance <= threshold:
            min_distance = distance
            nearest_city = city
    return nearest_city


def create_map(selected_cities, poland):
    m = folium.Map(location=[52.0, 19.0], zoom_start=6)

    if poland is not None:
        poland_geojson = poland.to_crs("EPSG:4326").__geo_interface__
        folium.GeoJson(poland_geojson, style_function=lambda x: {
                       'fillColor': 'skyblue', 'color': 'black'}).add_to(m)

    buffer_radius = 5000

    for city, coords in CITY_COORDS.items():
        is_selected = city in selected_cities
        folium.Circle(
            location=coords,
            radius=buffer_radius,
            color='orange' if is_selected else 'green',
            fill=True,
            fill_color='orange' if is_selected else 'lightgreen',
            fill_opacity=0.6 if is_selected else 0.4,
            tooltip=city,
            popup=city
        ).add_to(m)

        if is_selected:
            folium.Marker(
                location=coords,
                icon=folium.DivIcon(
                    html=f"""<div style="font-size: 12pt; color : red; background-color: white; padding: 2px; border-radius: 3px;">{city}</div>"""
                )
            ).add_to(m)

    return m


def clearJSON(clearDict):
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(clearDict, json_file,
                  ensure_ascii=False, indent=4)


def loadView():
    # print("huj")
    # districtcMap = "Legnica"
    tab1, tab2 = st.tabs(
        ["Wyniki wyborów z popreddnich lat", "Wyniki własne"])
    with tab2:

        lastParty = ""
        nextParty = ""
        diff = 0

        frequency = 0
        if st.session_state.get("last_clicked_city"):
            st.write(st.session_state["last_clicked_city"])
            districtcMap = st.session_state["last_clicked_city"]
        # elif st.session_state["selected_cities"]:
        #     st.write(", ".join(st.session_state["selected_cities"]))
        #     districtcMap = st.session_state["last_clicked_city"]

        else:
            st.write("Nie wybrano żadnych miast.")
            districtcMap = "Legnica"
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
        if "initialized" not in st.session_state:
            st.session_state["initialized"] = True
            st.session_state["votes"] = 0
            for i in range(5):
                st.session_state[f"input_{i}"] = 0.0
                st.session_state[f"slider_{i}"] = 0.0
        if "selected_cities" not in st.session_state:
            st.session_state["selected_cities"] = []
        if "last_clicked_city" not in st.session_state:
            st.session_state["last_clicked_city"] = None

        political_parties = ["PiS", "KO",
                             "Trzecia Droga", "Konfederacja", "Lewica"]

        main_col1, main_col2 = st.columns([3, 4])
        type = st.selectbox("rodzaj głosów", ["ilościowy", "procentowy"])
        with main_col1:
            with st.form("kalkulator mandatów w sejmie"):
                st.write("wybierz okrąg który chcesz uzupełnić")
                method = st.selectbox("metoda liczenia głosów", [
                    "d'Hondt", "Sainte-Laguë", "Kwota Hare’a (metoda największych reszt)", "Kwota Hare’a (metoda najmniejszych reszt)"])
                # if resestAll:
                #     clearJSON(seatsDistricstsDict)
                district = st.selectbox("wybierz okręg który chcesz uzupełnić",
                                        districtsDict.keys())
                selection = st.selectbox(
                    "Wybrałeś okrąg z listy czy z mapy", ["mapy", "listy"])
                if selection == "mapy":
                    val = districtsDict[districtcMap]
                    district = districtcMap
                else:
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
                        st.write(newSeats)
                        st.write(
                            f"Partia która zdobyła ostatni mandat w okręgu to {lastParty} a kolejny zdobyła by partia {nextParty}")
        with main_col2:
            world = load_shapefile(SHAPEFILE_PATH)
            if world is not None:
                poland = world[world.NAME == POLAND_NAME]
            else:
                poland = None

            m = create_map(st.session_state["selected_cities"], poland)

            map_result = st_folium(m, width=700, height=500)

            st.session_state["last_clicked_city"] = map_result['last_object_clicked_tooltip']

            st.subheader("Wybrane Miasto:")
            if st.session_state.get("last_clicked_city"):
                st.write(st.session_state["last_clicked_city"])
                districtcMap = st.session_state["last_clicked_city"]
            elif st.session_state["selected_cities"]:
                st.write(", ".join(st.session_state["selected_cities"]))
                districtcMap = st.session_state["last_clicked_city"]

            else:
                st.write("Nie wybrano żadnych miast.")
                districtcMap = "Legnica"

            # if "observables_initialized" not in st.session_state:
            #     setup_observers()
            #     st.session_state["observables_initialized"] = True

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
        st.write(votesDict)
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
        year = st.selectbox("wybierz interesujące cię wybory", [
                            "2023", "2019", "2015", "2011", "2007", "2005", "2001"])

    qulifiedParties, allParitesDict, voteForDistrict = electionCalc.calculateVotes(
        voteingThreshold, voteingThresholdForCoaliton, year)
    allPrtiesDict2 = allParitesDict.copy()
    with parties:
        st.write("Wybierz czy partia ma być zwolniona z progu wyborczgo")
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
    st.table(FiltredResultsDF)
