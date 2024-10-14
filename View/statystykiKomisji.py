from Controller.Commitees import ComitteStats, CommiteesList, CommitteeAge
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


def loadView():
    term_number = st.number_input(
        "kadencja sejmu", min_value=1, value=10)
    # print("puki co psuto")

    codes = [committee['code'] for committee in CommiteesList(term_number)]
    codes.append("łącznie")
    selectedCommittee = st.selectbox(
        "komijsja której statyski cię intersują (niektóre dostępne tylko dla obecnej kadecji)", options=list(codes)
    )

    clubs, MPs, clubsButBetter = ComitteStats(term_number, selectedCommittee)
    # with st.container(height=400):
    #     for MP in MPs:
    #         st.markdown(MP)
    # wyświetlanie informacji o ilości członkó i ilości komijsi
    ClubsCount = clubs.apply(lambda x: x.count(), axis=1)
    fig, ax = plt.subplots(figsize=(10, 6))
    ClubsCount.plot(kind='bar', ax=ax)
    ax.set_title('Liczba członków w komisjach', fontsize=16)

    ax.set_xlabel('Partie', fontsize=14)
    ax.set_ylabel('Liczba członków', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    st.dataframe(clubs)
    if selectedCommittee is "łącznie":
        st.dataframe(MPs)
    # wykresy wieku
    DataframeAges = CommitteeAge(clubsButBetter)
    all_ages = DataframeAges.values.flatten()
    all_ages = pd.Series(all_ages).dropna()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(all_ages, bins=10, color='red', edgecolor='black')
    ax.set_title('Ogólny rozkład wiekowy członków komisji', fontsize=16)
    ax.set_xlabel('Wiek', fontsize=14)
    ax.set_ylabel('Liczba członków', fontsize=14)
    st.pyplot(fig)
