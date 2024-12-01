import streamlit as st
import pandas as pd
import plotly.express as px

from api_wrappers.clubs import find_minimal_coalitions

def loadView():
    """
    Streamlit app to visualize minimal parliamentary coalitions
    
    This app provides an interactive exploration of minimal coalitions 
    in the Polish parliament, showing how different political clubs 
    can form majority alliances.
    """
    
    st.title("🏛️ Polskie Potencjalne Koalicje Sejmowe")
    
    # Find minimal coalitions
    term_number = st.number_input("kadencja sejmu", min_value=7, value=10)
    
    coalitions = find_minimal_coalitions(term_number)
    
    # Prepare coalition data
    coalition_data = []
    for i, coalition in enumerate(coalitions, 1):
        coalition_info = {
            'Procent jaki stanowi największy klub': round(max(club['membersCount'] for club in coalition)/sum(club['membersCount'] for club in coalition)*100,2),
            'Kluby': ', '.join(club['id'] for club in coalition),
            'Łączna ilość posłów': sum(club['membersCount'] for club in coalition),
            'Ilość klubów': len(coalition)
        }
        coalition_data.append(coalition_info)
    
    # Create DataFrame
    df = pd.DataFrame(coalition_data)
    
    # Streamlit interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Tabela")
        st.dataframe(df, use_container_width=True)
    
    with col2:
        st.header("Statystyki Koalicji")
        st.metric("Ilość potencjalnych koalicji", len(coalitions))
        st.metric("Minimalna ilość posłów", df['Łączna ilość posłów'].min())
        st.metric("Maksymalna ilość posłów", df['Łączna ilość posłów'].max())
    
    # Coalition selection
    st.header("Szczegóły")
    
    # Add default option for coalition selection
    coalition_options = ["Wybierz koalicję"] + [str(i) for i in range(len(coalitions))]
    selected_coalition_str = st.selectbox(
        "Wybierz koalicję", 
        options=coalition_options
    )
    
    if selected_coalition_str == "Wybierz koalicję":
        st.info("Wybierz koalicję aby zobaczyć szczegóły")
        return
        
    # Convert selection back to integer for indexing
    selected_coalition = int(selected_coalition_str)
    
    # Display selected coalition details
    coalition = coalitions[selected_coalition]
    club_df = pd.DataFrame([
        {'Club': club['id'], 'MPs': club['membersCount']} 
        for club in coalition
    ])
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Wykres Liniowy")
        fig = px.bar(
            club_df, 
            x='Club', 
            y='MPs', 
            title=f'Koalicja nr {selected_coalition}'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Wykres Kołowy")
        fig = px.pie(
            club_df, 
            values='MPs', 
            names='Club', 
            title=f'Koalicja nr {selected_coalition}'
        )
        st.plotly_chart(fig, use_container_width=True)
