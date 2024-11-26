import streamlit as st
import os

# TODO: Show information from Reports folder about avalibility of information 
# Przetwarza surowe dane z API i wyświetla ich wizualizacje w formie strony internetowej.
# Integruje wiele strumieni danych API za pomocą abstrakcyjnych wrapperów.
# Interpelacje
# Komisje
# Rozpiska członków komisji względem klubu, profesji, wykształcenia i województwa.
# Śledzenie Procesu Legislacyjnego
# Pokazuje nowe akty prawne z podziałem na ich typ
# Analiza wyników wyborów względem różnych metod podziału mandatów
# Koalicje
#     Kompleksowa platforma analizy danych parlamentarnych, 
#     dostarczająca wglądu w procesy wyborcze, działalność parlamentarną i dynamikę polityczną.

def loadView():
    st.title("🇵🇱 Internetowa Analiza Polskiej Polityki (IAPP) 🇵🇱")
    st.markdown(f"""
        **Aktualna Kadencja Sejmu**: 10 \n
        • Rozpoczęta: 13 listopada
        """)
    
    st.header("Obecny Stan Projektu")
    
    st.markdown("""
    IAPP to platforma analizy danych parlamentarnych, obecnie w fazie aktywnego rozwoju. 
    Oto przegląd aktualnych funkcjonalności i komponentów:
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔍 Aktualne Funkcjonalności")

        st.markdown(f"""
        - **Analiza Komisji Sejmowych**: 
            - Wyświetlanie informacji o komisjach dla wybranej kadencji
            - Prezentacja przyszłych i przeszłych posiedzeń komisji
            - Dostęp do transkrypcji posiedzeń (jeśli dostępne)
        """)

        st.markdown(f"""
        - **Analiza Ustaw i Rozporządzeń**: 
            - Prezentacja najnowszych aktów prawnych
            """)

        st.markdown("""
        - **Statystyki Komisji**: 
            - Analiza składu komisji według klubów parlamentarnych
            - Wizualizacja danych o złonkach komisji
        - **Interpelacje Poselskie**: 
            - Wyświetlanie szczegółów interpelacji, w tym autorów i odpowiedzi
        - **Procesy Legislacyjne**: 
            - Śledzenie etapów procesu legislacyjnego
            - Informacje o nowych aktach prawnych
        - **Analiza Ustaw i Rozporządzeń**: 
            - Prezentacja list ustaw i rozporządzeń z bieżącego roku
        """)
    with col2:
        # Sekcja technologii
        st.subheader("🛠 Technologie i Biblioteki")
        st.markdown("""
        - **Framework Web**: Streamlit
        - **Analiza Danych**: Pandas, NumPy
        - **Wizualizacja**: Plotly, Matplotlib
        - **Zapytania HTTP**: Requests
        - **Boty**: Telegram
        """)

        # Sekcja integracji
        st.subheader("🔗 Integracje Zewnętrzne")
        st.markdown("""
        - **API Sejmu RP**: Pobieranie danych o komisjach, posłach, posiedzeniach i procesach legislacyjnych
        """)

        # Sekcja struktury projektu
        st.subheader("📂 Struktura Projektu")
        st.markdown("""
        - **View**: Interfejs użytkownika Streamlit (główne komponenty: komisje, statystyki komisji, interpelacje, procesy legislacyjne)
        - **api_wrappers**: Moduły do komunikacji z API Sejmu
        - **Controller**: Logika biznesowa (w trakcie rozwoju)
        - **Model**: Definicje modeli danych (w trakcie rozwoju)
        """)

    # Sekcja w trakcie rozwoju
    st.subheader("🚧 Funkcje w Trakcie Rozwoju")
    st.markdown("""
    - Rozbudowa analizy statystycznej
    - Udoskonalenie wizualizacji danych
    - Implementacja funkcjonalności botów Discord i Telegram
    - Rozszerzenie analizy procesów legislacyjnych
    """)

    st.info("Projekt jest aktywnie rozwijany. Niektóre funkcje mogą być niekompletne lub podlegać zmianom.")
