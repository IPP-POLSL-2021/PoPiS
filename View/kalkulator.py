import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import Point
from math import radians, cos, sin, asin, sqrt


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


SHAPEFILE_PATH = ".\Data\ne_10m_admin_0_countries.shp"
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
        st.error(f"Error loading shapefile: {e}")
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


def loadView():

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

    with main_col1:
        st.header("Rozkład Procentowy")
        for i in range(5):
            label = f"{political_parties[i]}"
            number_key = f"input_{i}"
            slider_key = f"slider_{i}"

            party_col1, party_col2, party_col3 = st.columns(
                [1, 1, 3], gap="small")

            with party_col1:
                st.markdown(
                    f'<span class="party-label">{label}</span>', unsafe_allow_html=True)

            with party_col2:
                st.number_input(
                    "", min_value=0.0, max_value=100.0,
                    value=float(st.session_state.get(number_key, 0.0)),
                    step=0.1, format="%.2f", key=number_key,
                    on_change=update_slider, args=(number_key, slider_key)
                )

            with party_col3:
                st.slider("", 0.0, 100.0, st.session_state.get(slider_key, 0.0), 0.1, key=slider_key,
                          on_change=update_number_input, args=(
                              slider_key, number_key)
                          )

        buttons_col1, buttons_col2 = st.columns([1, 1])
        with buttons_col1:
            st.button("Wyczyść", on_click=clear_inputs)
        with buttons_col2:
            st.button("Dodaj", on_click=calculate)
        with buttons_col2:
            st.button("Oblicz", on_click=summary)

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
        elif st.session_state["selected_cities"]:
            st.write(", ".join(st.session_state["selected_cities"]))
        else:
            st.write("Nie wybrano żadnych miast.")

    if "observables_initialized" not in st.session_state:
        setup_observers()
        st.session_state["observables_initialized"] = True


def setup_observers():
    observer = InputObserver()
    for i in range(5):
        observables[f"input_{i}"] = Observable()
        observables[f"slider_{i}"] = Observable()
        observables[f"input_{i}"].add_observer(observer)
        observables[f"slider_{i}"].add_observer(observer)


def update_number_input(slider_key, input_key):
    st.session_state[input_key] = min(st.session_state[slider_key], 100)
    observables[input_key].notify_observers(st.session_state[input_key])


def update_slider(input_key, slider_key):
    st.session_state[slider_key] = min(st.session_state[input_key], 100)
    observables[slider_key].notify_observers(st.session_state[slider_key])


def clear_inputs():
    for i in range(5):
        st.session_state[f"input_{i}"] = 0.0
        st.session_state[f"slider_{i}"] = 0.0


def calculate():
    total_percentage = sum(st.session_state[f"slider_{i}"] for i in range(5))
    if not (99.99 <= total_percentage <= 100.01):
        st.warning(
            f"Łączna wartość procentowa wynosi {total_percentage:.2f}%, a powinna wynosić 100%. Proszę dostosować wartości.")
    else:
        st.success(
            "Łączna wartość procentowa wynosi dokładnie 100%. Kalkulacja wykonana poprawnie.")
        st.write("Kalkulator D'Hondta")


observables = {}

loadView()
