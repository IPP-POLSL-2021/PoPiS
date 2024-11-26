import streamlit as st
from View import main_page, coalition_viewer, ustawy, view_interpelation
# Ocenić przydatność, dopracować
from View import correlation, watch_interpelation, benford_view

# Do potencjalnego złączenia razem
from View import statystykiKomisji, komisje
from View import calculator
from View import statystykiPoslow, view_vote

#st.set_page_config(page_title="IAPP - Internetowa Analiza Polskiej Polityki", page_icon="🇵🇱", layout="wide")
st.sidebar.title("🏛️ IAPP Nawigacja")

def ViewSelection():
    # Define base navigation categories
    navigation_categories = {
        "🏠 Strona Główna": {
            "Strona Główna": main_page.loadView
        },
        "📊 Statystyki": {
            "Komisje - Statystyki": statystykiKomisji.loadView,
            "Posłowie - Statystyki": statystykiPoslow.loadView
        },
        "🗳️ Procesy Parlamentarne": {
            "Interpelacje": view_interpelation.loadView,
            "Ustawy": ustawy.loadView,
            "Komisje": komisje.loadView,
            "Głosowania Posłów": view_vote.loadView
        },
        "🔮 Analiza Polityczna": {
            "Potencjalne Koalicje": coalition_viewer.loadView,
            "Kalkulator Wyborczy": calculator.loadView,
        },
        "🚧 W budowie": {
            "Korelacje": correlation.loadView,
            "Obserwuj Interpelacje": watch_interpelation.loadView,
            "Rozkład Benforda": benford_view.loadView
        }
    }

    # Dynamically generate "Wszystkie" category
    wszystkie_pages = {}
    for category_pages in navigation_categories.values():
        wszystkie_pages.update(category_pages)
    
    # Add dynamically generated "Wszystkie" category
    navigation_categories["📋 Wszystkie"] = wszystkie_pages

    # Create sidebar navigation with categories
    #selected_category = st.sidebar.radio(" ","📋 Wszystkie")
    # Wystarczy zamienić zakomentowane linie by zmienić widzialną wersję
    selected_category = st.sidebar.radio("Kategorie", list(navigation_categories.keys()))
    
    # Create subnavigation for the selected category
    selected_page = st.sidebar.selectbox(
        "Wybierz stronę", 
        list(navigation_categories[selected_category].keys())
    )

    # Load the corresponding view
    navigation_categories[selected_category][selected_page]()

ViewSelection()
