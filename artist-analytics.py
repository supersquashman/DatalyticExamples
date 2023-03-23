import os

artists = {}
nationalities = {}
genders = {}

artist_file = open("data\\Artists.csv")
for artist_info in artist_file.readlines():
    artist = artist_info.split(',')
    artists.append(
        {"name":artist[0],
        "nationality": artist[1],
        "gender": artist[2],
        "birth_year": artist[3],
        "death_year": artist[4],
        "wikiQID": artist[5],
        "gettyULANID": artist[6]}
    )
#name, nationality, gender, birth year, death year, Wiki QID, and Getty ULAN ID.

for artist in artists:
    if artist["nationality"] in nationalities:
        nationalities[artist[nationalities]]