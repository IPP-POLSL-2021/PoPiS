import streamlit as st
import os

# Konfiguracja strony
st.set_page_config(
        page_title="Platforma Analizy Danych Parlamentarnych", 
        page_icon=":bar_chart:", 
        layout="wide"
    )
def loadView():

    # Główny tytuł i wprowadzenie
    # Polskiej albo Parlamenarnej
    st.title("🇵🇱 Internetowa Analiza Polskiej Polityki (IAPP) 🇵🇱 ")
    
    # Podtytuł z opisem projektu
    st.markdown("""
    ## Przegląd Projektu
    Kompleksowa platforma analizy danych parlamentarnych, 
    dostarczająca wglądu w procesy wyborcze, działalność parlamentarną i dynamikę polityczną.
    """)

    # Sekcja Funkcji
    st.header("🔍 Kluczowe Funkcje")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Analiza Wyborcza")
        st.markdown("""
        - Obliczenia wyników wyborów
        - Analiza wzorów głosowania
        - Wgląd w podział mandatów
        """)
    
    with col2:
        st.subheader("Wgląd Parlamentarny")
        st.markdown("""
        - Śledzenie aktywności komisji
        - Monitoring interpelacji
        - Statystyki posłów
        """)
    
    with col3:
        st.subheader("Wizualizacja Danych")
        st.markdown("""
        - Interaktywne wykresy
        - Reprezentacje statystyczne
        - Analiza prawa Benforda
        """)

    # Przegląd Struktury Projektu
    st.header("📂 Struktura Projektu")
    
    # Rozwijana sekcja struktury projektu
    with st.expander("Wyświetl Moduły Projektu"):
        modules = {
            "Interfejsy API": ["Kluby", "Komisje", "Grupy", "Posłowie", "Obrady", "Głosowania"],
            "Kontrolery": ["Obliczenia Wyborcze", "Statystyki", "Boty"],
            "Zarządzanie Danymi": ["Import Danych", "Kontekst Bazy Danych"],
            "Widoki": ["Widoki Statystyczne", "Kalkulatory Wyborcze", "Przeglądarka Interpelacji"]
        }
        
        for category, items in modules.items():
            st.markdown(f"**{category}:**")
            st.markdown(", ".join(items))

    # Szczegóły Techniczne
    st.header("🛠 Szczegóły Techniczne")
    
    tech_cols = st.columns(2)
    
    with tech_cols[0]:
        st.metric("Język Programowania", "Python")
        st.metric("Przetwarzanie Danych", "Pandas, NumPy")
    
    with tech_cols[1]:
        st.metric("Framework Webowy", "Streamlit")
        #st.metric("Baza Danych", "MySQL")

    # Stopka
    #st.markdown("---")
    #st.markdown("*Napędzane zaawansowanymi technikami analizy danych i otwartymi danymi parlamentarnymi*")
