import streamlit as st
from Controller import MPsStats
from api_wrappers import votings, MP
import datetime
import pandas as pd
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def loadView():
    st.title("Głosowania Posła")

    # Select term and sitting
    term_number = st.number_input("Kadencja Sejmu", min_value=1, value=10)

    # Get MPs for the selected term
    MpGroupedList, MpsList, MpNamesByClub = MPsStats.groupMpsByClub(
        term_number)

    # Select MP
    selected_mp = st.selectbox("Wybierz posła", list(
        mp['lastFirstName'] for mp in MpsList))

    # Find selected MP's ID
    selected_mp_data = next(
        (mp for mp in MpsList if mp['lastFirstName'] == selected_mp), None)

    if selected_mp_data:
        mp_id = selected_mp_data['id']

        try:
            # Get proceedings for the term
            votings_response = votings.get_votings(term_number)
            if votings_response.status_code == 200:
                votings_data = votings_response.json()
                proceeding_numbers = sorted(
                    list(set(int(v['proceeding']) for v in votings_data)))

                # Select proceeding
                proceeding_number = st.selectbox(
                    "Numer posiedzenia", proceeding_numbers)

                # Filter dates for selected proceeding
                proceeding_dates = sorted(set(
                    v['date'] for v in votings_data
                    if int(v['proceeding']) == proceeding_number
                ))

                # Date selection from available dates
                selected_date = st.selectbox(
                    "Wybierz datę głosowania",
                    proceeding_dates,
                    format_func=lambda x: datetime.datetime.strptime(
                        x, '%Y-%m-%d').strftime('%d-%m-%Y')
                )

                if st.button("Pokaż głosowania"):
                    # Get all votes for the proceeding first
                    with st.spinner('Pobieranie danych o głosowaniach...'):
                        proceeding_votes_response = votings.get_proceeding_votings(
                            term_number, proceeding_number)

                        if proceeding_votes_response.status_code == 200:
                            proceeding_votes = proceeding_votes_response.json()

                            # Get MP's voting details
                            voting_response = votings.get_mp_voting_details(
                                term_number, mp_id, proceeding_number, selected_date
                            )

                            if voting_response.status_code == 200:
                                voting_details = voting_response.json()

                                if voting_details:
                                    st.subheader(
                                        f"Głosowania z dnia {datetime.datetime.strptime(selected_date, '%Y-%m-%d').strftime('%d-%m-%Y')}")

                                    # Create tabs for different views
                                    tab1, tab2 = st.tabs(
                                        ["Szczegóły głosowań", "Statystyki"])

                                    with tab1:
                                        # Create a progress bar
                                        progress_bar = st.progress(0)
                                        total_votes = len(voting_details)

                                        # Display individual voting details
                                        for i, vote in enumerate(voting_details):
                                            voting_num = vote['votingNumber']

                                            # Find full voting details from proceeding votes
                                            full_voting = next(
                                                (v for v in proceeding_votes if str(
                                                    v.get('votingNumber')) == str(voting_num)),
                                                {}

                                            )

                                            with st.expander(f"Głosowanie nr {voting_num} - {vote.get('topic', 'Brak tematu')}"):
                                                st.write(
                                                    f"**Przedmiot głosowania:** {vote.get('topic', 'Brak')}")
                                                st.write(
                                                    f"**Oddany głos:** {vote.get('vote', 'Brak')}")
                                                st.write(
                                                    f"**Czas głosowania:** {vote.get('date', 'Brak')}")

                                                # full_voting = True

                                                if full_voting:

                                                    st.write(
                                                        "**Wyniki głosowania:**")
                                                    col1, col2, col3, col4 = st.columns(
                                                        4)
                                                    with col1:
                                                        st.metric(
                                                            "Za", full_voting.get('yes', 0))
                                                    with col2:
                                                        st.metric(
                                                            "Przeciw", full_voting.get('no', 0))
                                                    with col3:
                                                        st.metric(
                                                            "Wstrzymało się", full_voting.get('abstain', 0))
                                                    with col4:
                                                        st.metric("Nieobecni", full_voting.get(
                                                            'notParticipating', 0))

                                            # Update progress
                                            progress_bar.progress(
                                                (i + 1) / total_votes)

                                    with tab2:
                                        # Calculate and display voting statistics
                                        total_votes = len(voting_details)
                                        if total_votes > 0:
                                            votes_count = defaultdict(int)
                                            # needed to get current MPs clubs
                                            mpList = MP.get_MPs(
                                                term_number).json()

                                            # Log raw voting data for debugging
                                            logger.info("Raw voting details:")
                                            for i, vote in enumerate(voting_details):
                                                originalDict, currDict = votings.clubs_votes(
                                                    term=term_number, proceedingNum=proceeding_number, voteNum=i, MPslist=mpList)
                                                vote_value = vote.get(
                                                    'vote', '')
                                                logger.info(
                                                    f"Vote value: {vote_value}")
                                                if pd.DataFrame.from_dict(originalDict).empty:

                                                    continue
                                                with st.expander(f"Głosowanie nr {i+1} - {vote.get('topic', 'Brak tematu')}"):

                                                    if pd.DataFrame.from_dict(originalDict).equals(pd.DataFrame.from_dict(currDict)):
                                                        orgFrame = pd.DataFrame.from_dict(
                                                            originalDict)
                                                        orgFrame.index = [
                                                            "Za", "Przeciw", "Wstrzymało się", "Nieobecni"]
                                                        st.write(
                                                            "Głosy oddane przez kluby przy ich składzie w momencie głosowania")
                                                        st.dataframe(
                                                            originalDict)
                                                    elif not pd.DataFrame.from_dict(originalDict).empty:
                                                        st.write(
                                                            "Głosy oddane przez kluby przy ich składzie w momencie głosowania")
                                                        orgFrame = pd.DataFrame.from_dict(
                                                            originalDict)
                                                        orgFrame.index = [
                                                            "Za", "Przeciw", "Wstrzymało się", "Nieobecni"]
                                                        st.dataframe(
                                                            orgFrame)
                                                        currFrame = pd.DataFrame.from_dict(
                                                            currDict)
                                                        currFrame.index = [
                                                            "Za", "Przeciw", "Wstrzymało się", "Nieobecni"]
                                                        st.write(
                                                            "Głosy oddane przez kluby przy ich składzie w obecnym momencie lub pod koniec kadencji")

                                                        st.dataframe(currFrame)
                                                    # Map vote values
                                                    # print(vote_value)
                                                    if vote_value.lower() in ['yes']:
                                                        votes_count['Za'] += 1
                                                    elif vote_value.lower() in ['no']:
                                                        votes_count['Przeciw'] += 1
                                                    elif vote_value.lower() in ['abstain']:
                                                        votes_count['Wstrzymał się'] += 1
                                                    elif vote_value.lower() in ['absent']:
                                                        votes_count['Nieobecny'] += 1

                                            # Log calculated statistics
                                            logger.info(
                                                "Calculated vote counts:")
                                            for vote_type, count in votes_count.items():
                                                logger.info(
                                                    f"{vote_type}: {count}")

                                            st.subheader("Statystyki głosowań")

                                            # Display statistics in columns
                                            cols = st.columns(4)
                                            vote_types = [
                                                'Za', 'Przeciw', 'Wstrzymał się', 'Nieobecny']
                                            for i, vote_type in enumerate(vote_types):
                                                with cols[i]:
                                                    count = votes_count[vote_type]
                                                    percentage = (
                                                        count / total_votes) * 100
                                                    st.metric(
                                                        vote_type,
                                                        f"{count} ({percentage:.1f}%)"
                                                    )
                                        else:
                                            st.info(
                                                "Brak głosowań w wybranym dniu")
                                else:
                                    st.info(
                                        "Brak głosowań dla wybranego posła w tym dniu")
                            else:
                                st.error(
                                    "Nie udało się pobrać danych o głosowaniach posła")
                        else:
                            st.error(
                                "Nie udało się pobrać danych o posiedzeniu")
            else:
                st.error("Nie udało się pobrać listy posiedzeń")
        except Exception as e:
            st.error(f"Wystąpił błąd: {str(e)}")
            logger.exception("Error in loadView")
