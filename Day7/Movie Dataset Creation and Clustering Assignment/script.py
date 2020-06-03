import pandas as pd
import json, os

df = pd.read_csv("./tmdb_5000_movies.csv")

data = {}
num_choices = 5

try:
    with open("final.json", "r") as f:
        data = json.load(f)
except:
    ip = input("Enter your name: ").strip()
    while ip == "":
        ip = input("Enter your name: ")
        
    data["username"] = ip
    data["movie_ids"] = []
    data["genre_freq"] = {}
    data["genre_freq_divided"] = {}
    
    for i in range(df.shape[0]):
        genres = json.loads(df["genres"].iloc[i])
        for genre in genres:
            data["genre_freq"][genre["name"]] = 0
            data["genre_freq_divided"][genre["name"]] = 0
            
while len(data["movie_ids"]) != df.shape[0]:
    num_idxs = min(df.shape[0]-len(data["movie_ids"]), num_choices)
    idxs = np.random.choice(df.shape[0], size=num_idxs, replace=False)
    
    print("-"*100)
    for i,idx in enumerate(idxs.tolist()):
        while df["id"].iloc[idx] in data["movie_ids"]: 
            idx = np.random.randint(0, df.shape[0])

        print("{}) {}".format(i, df["title"].iloc[idx]))

    ip = int(input("Preferred Movie: "))
    if not 0<=ip<num_choices:
        print("No option selected. Skipping...")
        continue
    
    chosen_loc = idxs[i]
    genres = json.loads(df["genres"].iloc[chosen_loc])
    for genre in genres:
        data["genre_freq"][genre["name"]] += 1
        data["genre_freq_divided"][genre["name"]] += 1/len(genres)

    data["movie_ids"].append(int(df["id"].iloc[chosen_loc]))

    with open("final.json", "w") as f:
        json.dump(data, f)