import streamlit as st

# TODO: Show information from Reports folder about avalibility of information
st.set_page_config(layout="wide")


def loadView():
    st.title("🇵🇱 Internetowa Analiza Polskiej Polityki (IAPP) 🇵🇱")
    st.markdown(f"""
        **Aktualna Kadencja Sejmu**: 10 \n
        • Rozpoczęta: 13 listopada
        """)

    st.header("Obecny Stan Projektu")

    st.markdown("""
    IAPP to platforma analizy danych parlamentarnych, obecnie w fazie aktywnego rozwoju.
    Jej nadrzędnym celem jest popularyzacja informacji na temat organu ustawodawczego naszego kraju.
    Dzięki nowoczesnym technologiom integruje ona strumienie API i przetwarza w sposób kompleksowy by dostarczyć wgląd w dynamikę polityczną.
    Oto przegląd aktualnych funkcjonalności i komponentów:
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔍 Aktualne Funkcjonalności")
        st.markdown("""
        - **Komisje Sejmowe**: 
            - Analiza składu komisji według klubów parlamentarnych i nie tylko
            - Kompaktowe podsumowanie zakresu działania jak i władz komisji
            - Szczegóły na temat ostatnich posiedzień danej komisji
        - **Interpelacje Poselskie**:
            - Prezentacja informacji o autorach w tym ich klubu i profesji.
            - Wyświetlanie w sposób przystępny odpowiedzi nadesłane.
        - **Procesy Legislacyjne**: 
            - Śledzenie etapów procesu legislacyjnego
            - Prezentacja najnowszych aktów prawnych z podziałem na ich typ
        - **Posłowie**:
            - Historia posła na przestrzeni kadencji
            - Statystyki dot. wykształcenia i profesji z podziałem na klub parlamentarny.
            - Prezentacja głosów danego posła wg dnia
        - **Political Fiction**:
            - Znajdywanie alternatywnych koalicji rządowych w poszczególnych kadencjach Sejmu
            - Sprawdzanie jak inna metoda dzielenia mandatów wpłynęłaby na wyniki wyborów
        """)
    with col2:
        # Sekcja technologii
        st.subheader("🛠 Technologie i Biblioteki")
        st.markdown("""
        - **Framework Web**: Streamlit
        - **Analiza Danych**: Pandas, NumPy, Statistics
        - **Wizualizacja**: Plotly, Matplotlib, Streamlit-aggrid
        - **Zapytania HTTP**: Requests
        - **Boty**: Telebot
        """)

        # Sekcja integracji
        st.subheader("🔗 Integracje Zewnętrzne")
        st.markdown("""
        - **API Sejmu RP**: Pobieranie danych o komisjach, posłach, posiedzeniach i procesach legislacyjnych
        - **Dane z Państwowej Komisji Wyborczej**: Surowe dane o wynikach wyborów do Sejmu RP w latach 2011-2024
        """)

        # Sekcja struktury projektu
        st.subheader("📂 Struktura Projektu")
        st.markdown("""
        - **View**: Interfejs użytkownika
        - **api_wrappers**: Komunikacja z API Sejmu
        - **Controller**: 
        - **Model**: Definicje modeli danych 
        """)

    # Sekcja w trakcie rozwoju
    st.subheader("🚧 Funkcje w Trakcie Rozwoju")
    st.markdown("""
    - Implementacja powiadomień na temat nowych ustaw, głosowań etc poprzez komunikator Telegram
    - Porównanie głosowań posła z głosowaniem ogółu klubu
    """)

    st.info("Projekt jest aktywnie rozwijany. Niektóre funkcje mogą być niekompletne lub podlegać zmianom.")


if __name__ == "__main__":
    loadView()
