# Library
import pandas as pd
import matplotlib.pyplot as plt

# Reading data
df = pd.read_csv('Data/data.csv')
# Column Formatting
# Political Parties | Votes

dict = df.to_dict()
votes = dict["LICZBA_GLOSOW"]
parties = dict["KOMITET"]
party_name_map = {
    "KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ": "PiS",
    "KOALICYJNY KOMITET WYBORCZY KOALICJA OBYWATELSKA PO .N IPL ZIELONI": "PO",
    "KOALICYJNY KOMITET WYBORCZY TRZECIA DROGA POLSKA 2050 SZYMONA HOŁOWNI - POLSKIE STRONNICTWO LUDOWE": "Polska 2050",
    "KOMITET WYBORCZY NOWA LEWICA": "Lewica"
}
party_colors = {
    "PiS": "blue",
    "PO": "orange",
    "Polska 2050": "yellow",
    "Lewica": "red"
}


# Seats
seats = 9
score = {party: 0 for party in parties.values()}
arr = []

# Function find maximum value
def max_value(d):
    max_key = list(d.keys())[0]
    max_val = d[max_key]
    for k, v in d.items():
        if max_val < v:
            max_val = v
            max_key = k
    return max_key, max_val


votes = dict["LICZBA_GLOSOW"].copy()
for _ in range(seats):
    index = max_value(votes)[0]
    score[parties[index]] += 1
    arr.append(parties[index])
    votes[index] = dict["LICZBA_GLOSOW"][index] / (score[parties[index]] + 1)



# Visualitation of scores

score_short = {party_name_map.get(party, party): seats for party, seats in score.items()}

partie_names = list(score_short.keys())
assigned_seats = list(score_short.values())
colors = [party_colors.get(party, 'gray') for party in partie_names]

plt.figure(figsize=(6, 4))
plt.bar(partie_names, assigned_seats, color=colors)

plt.title('Przydzielone miejsca dla partii', fontsize=12)
plt.xlabel('Partie', fontsize=10)
plt.ylabel('Liczba przydzielonych miejsc', fontsize=10)
plt.xticks(rotation=20, ha='right', fontsize=8)

plt.tight_layout()
plt.show()

arr_df = pd.DataFrame(arr, columns=['Przydzielona Partia'])
arr_df['Miejsce'] = arr_df.index + 1
arr_df = arr_df[['Miejsce', 'Przydzielona Partia']]

print(arr_df)

