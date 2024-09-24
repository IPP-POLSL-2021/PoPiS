# Library
import pandas as pd

# Reading data
df = pd.read_csv('data.csv')
# Column Formatting
# Political Parties | Votes

dict = df.to_dict()
#print(dict)
votes = dict["LICZBA_GLOSOW"]
parties = dict["KOMITET"]
#print(parties)
#print(votes)

# Seats
seats = 9
score = {0: 0, 1: 0, 2: 0, 3: 0}

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
    score[index] += 1
    votes[index] = dict["LICZBA_GLOSOW"][index] / score[index] + 1
    #print(votes)

print(score)

# Function calculation of votes by D’Hondta Method


# Visualitation of scores
