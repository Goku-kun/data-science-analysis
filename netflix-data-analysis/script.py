import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import re

# To display all columns and all rows
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)


data = pd.read_csv("./archive/netflix_titles.csv")
# print(data.head())
# print(data.dtypes)

# Only movies
movies = data[data.type == 'Movie'].copy()
# print(movies.head())

# Only TV Shows
shows = data[data.type == 'TV Show'].copy()
# print(shows.head())


# average movies length
movies.duration = movies.duration.replace(r" min","", regex=True)
# print(movies.dtypes)
movies.duration = pd.to_numeric(movies.duration)
# print(movies.info())
print(movies.duration.mean(), "is the average length considering all the movies in this dataset.")
print("The statistical analysis of movies' duration is:")
print("*"*50)
print(movies.duration.describe())
print("*"*50)
print()
print()

# average TV Shows length
shows.duration = shows.duration.replace(r"(\d*) [Ss]easons?",r"\1", regex=True)
shows.duration = pd.to_numeric(shows.duration)
print(shows.duration.mean(), "is the average number of seasons per show.")
print(shows.duration.describe())
print("*"*50)
print()
print()

# group movies by year and finding their average
movies_groupby_year = movies.groupby('release_year').duration.mean()
print(movies_groupby_year)
print("*"*50)
print()
print()


# Filtering the shows listed as Anime Series or Anime Features
shows_copy_anime = shows.copy()
movies_copy_anime = movies.copy()
anime_list = pd.concat([shows_copy_anime, movies_copy_anime])
anime_list.listed_in = anime_list.listed_in.apply(lambda x: "Anime" if re.search(r".*Anime (Series|Features).*", x) else "")
# Alternatively, we can also use shows_copy_anime.listed_in = shows_copy_anime.listed_in.replace(r".*Anime (Series|Features).*", "Anime Series", regex = True)
convertor = anime_list[anime_list.listed_in == 'Anime'].reset_index(drop=True).rename_axis("index").to_csv('./anime-available-on-netflix    .csv')


# Extracting all the genres Netflix has available

genres = data['listed_in'].unique()
list_unique_genres = []
for genre in genres:
    for gen in genre.split(","):
        if gen.strip() not in list_unique_genres:
            list_unique_genres.append(gen.strip())
print(list_unique_genres)

with open("unique-genres.txt","w") as f:
    for genre in list_unique_genres:
        f.write(genre.strip()+"\n")
    f.close()



# Extracting titles with country India
titles_made_in_india = data[data['country'].apply(lambda x: "India" if re.search(r".*India.*", str(x)) else x) == "India"].reset_index(drop=True).rename_axis("index")
# print(titles_made_in_india.head())
titles_made_in_india.to_csv("./titles-made-in-India.csv")



# Extracting all the titles with Korean TV shows as genre
data_copy = data.copy()
korean_tv_shows = data_copy[data_copy['listed_in'].apply(lambda x: "Korean" if re.search(r".*Korean TV Shows", x) else x) == "Korean"].reset_index(drop=True).rename_axis("index")
korean_tv_shows.to_csv('./Korean-tv-shows.csv')