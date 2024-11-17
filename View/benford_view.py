import streamlit as st
from Controller.benford_analysis import analyze_benford_law
import scipy.stats as stats

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
                plot, chi_square, ks_statistic, p_value = analyze_benford_law(election_level, data_type)
                
                # Display results
                st.pyplot(plot.gcf())
                
                # Display statistics in a clean format
                st.subheader("Statystyki")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label="Wartość testu chi-square",
                        value=f"{chi_square:.4f}"
                    )
                with col2:
                    st.metric(
                        label="Stopnie swobody",
                        value="8"
                    )
                
                st.metric(
                    label="P-wartość (chi-square)",
                    #value=stats.chi2.sf(chi_square, 8)
                    value=f"{stats.chi2.sf(chi_square, 8):.4f}"
                )

                st.metric(
                    label="Statystyka Kołmogorowa-Smirnowa",
                    value=f"{ks_statistic:.4f}"
                )
                
                st.metric(
                    label="P-wartość (KS test)",
                    value=f"{p_value:.4f}"
                )
                # Add interpretation in a clean format
                st.subheader("Interpretacja")
                st.info("""
                Rozkład Benforda to teoretyczny rozkład pierwszych cyfr w zbiorach danych liczbowych.
                - Wyższe wartości chi-square wskazują na większe odchylenie od rozkładu Benforda.
                - Niższe p-wartości (< 0.05) sugerują statystycznie istotne odchylenie od rozkładu Benforda.
                - Statystyka Kołmogorowa-Smirnowa mierzy maksymalną różnicę między obserwowanym a oczekiwanym rozkładem kumulatywnym.
                - Znaczące odchylenia mogą wskazywać na nietypowe wzorce w danych, ale nie zawsze oznaczają nieprawidłowości.
                """)
                
                # Clear matplotlib figure to free memory
                plot.clf()
        except Exception as e:
            st.error(f"Wystąpił błąd podczas analizy: {str(e)}")