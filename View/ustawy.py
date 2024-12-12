import requests
# from streamlit_notifications import send_push
from datetime import datetime, date
import streamlit as st
# from sentimentpl.models import SentimentPLModel
from Controller.acts import get_all_acts_this_year, get_titles_of_record, is_the_new_act_in_effect_today,  get_process_details, get_legislative_processes
# import pdfplumber
# from io import BytesIO,StringIO
# import re
# from collections import defaultdict
# import pandas as pd

BASE_URL = "https://api.sejm.gov.pl"

# sentiment_analyzer_pl = SentimentPLModel(from_pretrained='latest')
#
# def load_pdf_text_with_pdfplumber(file_path):
#    text = ""
#    with pdfplumber.open(file_path) as pdf:
#        for page in pdf.pages:
#            page_text = page.extract_text()
#            if page_text:
#                text += page_text + "\n"
#    text = re.sub(r'\(.*?\)', '', text)
#    return text
#
#
# def find_unique_names(text):
#    polish_letters = "A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż"
#    names = re.findall(rf'(Poseł\s+[{polish_letters}]+ [{polish_letters}]+)', text)
#    unique_names = set(names)
#    return unique_names
#
#
# def extract_speeches(text, unique_names):
#    polish_letters = "A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż"
#    speeches = defaultdict(list)
#    for name in unique_names:
#        pattern = rf'{name}:(.*?)(?=(Poseł\s+[{polish_letters}]+\s+[{polish_letters}]+:|$))'
#        matches = re.findall(pattern, text, re.DOTALL)
#        speeches[name].extend(matches)
#    return speeches
#
# def analyze_sentiment(text):
#
#    if not isinstance(text, str):
#        raise ValueError("Oczekiwano ciągu tekstowego, ale otrzymano obiekt typu: {}".format(type(text)))
#
#    if not text.strip():
#        return "Neutralny", 0
#
#    fragments = [text[i:i+512] for i in range(0, len(text), 512)]
#    scores = []
#    for fragment in fragments:
#        try:
#            score = sentiment_analyzer_pl(fragment).item()
#            scores.append(score)
#        except IndexError:
#            scores.append(0)
#
#    avg_score = sum(scores) / len(scores) if scores else 0
#   label = "Pozytywny" if avg_score > 0 else "Negatywny"
#    return label, abs(avg_score)


def loadView():

    TERM = st.number_input(
        "Kadencja sejmu", min_value=1, value=10, key='term_input_stats')

    # Create two columns for the layout
    col1, col2 = st.columns([3, 2])

    processes = get_legislative_processes(TERM)
    with col1:
        st.title("Śledzenie Procesu Legislacyjnego")

        if processes:
            process_titles = ["Wybierz proces"]  # Add default option
            process_titles.extend(
                [f"{p['number']} - {p['title']}" for p in processes])
            selected_process = st.selectbox(
                "Wybierz proces legislacyjny", process_titles)

            if selected_process == "Wybierz proces":
                st.info("Wybierz proces legislacyjny aby zobaczyć szczegóły")
            else:
                selected_process_number = selected_process.split(" - ")[0]
                process_details = get_process_details(
                    TERM, selected_process_number)

                if process_details:
                    st.subheader("Szczegóły procesu legislacyjnego")
                    st.write(
                        f"**Tytuł:** {process_details.get('title', 'Brak tytułu')}")
                    st.write(
                        f"**Opis:** {process_details.get('description', 'Brak opisu')}")
                    st.write(
                        f"**Data rozpoczęcia:** {process_details.get('processStartDate', 'Brak daty')}")

                    stages = process_details.get('stages', [])
                    if stages:
                        st.subheader("Etapy procesu")
                        for stage in stages:
                            st.write(f"**Etap:** {stage['stageName']}")
                            try:
                                st.write(f"**Data:** {stage['dates']}")
                            except:
                                print("no date")
                            try:
                                st.write(f"**Decyzja:** {stage['decision']}")
                            except:
                                print("no decision")
                            st.write("---")
                            temp = stage
                    else:
                        st.write("Brak dostępnych etapów.")
        else:
            st.write("Brak dostępnych procesów legislacyjnych.")

    with col2:
        st.title("Akty Prawne")

        st.write("Był dziś nowy akt prawny?")
        if is_the_new_act_in_effect_today():
            st.write("Tak")
        else:
            st.write("Nie")

        st.subheader("Ostatnie 10 ustaw danego roku")
        year = st.number_input(
            "Rok", min_value=1, value=2024, key='wanted_year')

        acts = get_all_acts_this_year(year)
        if acts:
            result = get_titles_of_record(acts)

            st.subheader("Ustawy")
            st.table([{"Tytuł ustawy": title} for title in result['ustawy']])

            st.subheader("Rozporządzenia")
            st.table([{"Tytuł rozporządzenia": title}
                     for title in result['rozporzadzenia']])
        else:
            st.error("Nie udało się pobrać danych.")
