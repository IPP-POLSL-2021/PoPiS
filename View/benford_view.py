import streamlit as st
from Controller.benford_analysis import analyze_benford_law

def loadView():
    st.title("Analiza rozkładu Benforda")
    
    # Selection for data granularity with unique key
    election_level = st.selectbox(
        "Wybierz poziom analizy",
        ["województwa", "okręgi", "powiaty", "gminy", "obwody"],
        key="benford_level"
    )
    
    # Selection for data type with unique key
    data_type = st.selectbox(
        "Wybierz typ danych",
        ["procentowe", "liczbowe"],
        key="benford_type"
    )
    
    if st.button("Przeprowadź analizę", key="benford_analyze"):
        try:
            with st.spinner('Trwa analiza danych...'):
                # Perform analysis
                plot, chi_square = analyze_benford_law(election_level, data_type)
                
                # Display results
                st.pyplot(plot.gcf())
                
                # Display statistics in a clean format
                st.subheader("Statystyki")
                st.metric(
                    label="Wartość testu chi-square",
                    value=f"{chi_square:.2f}"
                )
                
                # Add interpretation in a clean format
                st.subheader("Interpretacja")
                st.info("""
                Rozkład Benforda to teoretyczny rozkład pierwszych cyfr w zbiorach danych liczbowych.
                - Wyższe wartości chi-square wskazują na większe odchylenie od rozkładu Benforda
                - Znaczące odchylenia mogą wskazywać na nietypowe wzorce w danych
                """)
                
                # Clear matplotlib figure to free memory
                plot.clf()
        except Exception as e:
            st.error(f"Wystąpił błąd podczas analizy: {str(e)}")
