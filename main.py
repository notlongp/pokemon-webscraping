# Pokemon WebScraping Project

# Creating a sub-folder for the images
import os
os.mkdir('images')

# Making Web Request
import requests

URL = 'https://pokemondb.net/pokedex/national'
page = requests.get(URL)

# Parsing HTML with BeautifulSoup package
from bs4 import BeautifulSoup

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all("div", {"class": "infocard"})

# Multiplier function
# This function will take a string that indicate a multiplier in the HTML file and return the respective multiplier
def replace_multiplier(string):
    if string == 'type-fx-25':
        return 0.25
    elif string == 'type-fx-50':
        return 0.50
    elif string == 'type-fx-200':
        return 2
    elif string == 'type-fx-400':
        return 4
    else:
        return 1

# Scraping images
# Scraping all images into sub-folder 'images'
from PIL import Image

for result in results:
    imageName = result.find("a", {"class": "ent-name"}).text
    imageName = imageName.replace("\'", "")
    imageName = imageName.replace(":", "")
    imageName = imageName.replace(" ", "")
    imageName = imageName.replace("♀", "F")
    imageName = imageName.replace("♂", "M")
    imageURL = result.find("span",{"class": "img-fixed img-sprite"})["data-src"]
    img = Image.open(requests.get(imageURL, stream = True).raw)
    img.save(os.path.join("images", imageName + ".png"))

# Scraping Pokemon data
import re
meta = []
mainURL = "https://pokemondb.net"
for result in results:
    pokeCurrent = []
    # Extract national number
    pokeNo = result.find_all("small")[0].text
    # Extract name
    pokeName = result.find("a", {"class": "ent-name"}).text
    pokeName = pokeName.replace("\'", "")
    pokeName = pokeName.replace(":", "")
    pokeName = pokeName.replace(" ", "")
    pokeName = pokeName.replace("♀", "F")
    pokeName = pokeName.replace("♂", "M")
    # Extract Type
    pokeType1 = result.find_all("small")[1].find_all("a")[0].text
    try:
        pokeType2 = result.find_all("small")[1].find_all("a")[1].text
    except IndexError:
        pokeType2 = ""
    # Extract Type defense effectiveness
    subURL = result.find("a", {"class": "ent-name"})["href"]
    bindURL = mainURL + subURL
    subPage = requests.get(bindURL)
    subSoup = BeautifulSoup(subPage.content, 'html.parser')
    subResults = subSoup.find_all("table", {"class": "type-table type-table-pokedex"})
    nor = replace_multiplier(subResults[0].find_all("tr")[1].find_all("td")[0]["class"][1])
    fir = replace_multiplier(subResults[0].find_all("tr")[1].find_all("td")[1]["class"][1])
    wat = replace_multiplier(subResults[0].find_all("tr")[1].find_all("td")[2]["class"][1])
    ele = replace_multiplier(subResults[0].find_all("tr")[1].find_all("td")[3]["class"][1])
    gra = replace_multiplier(subResults[0].find_all("tr")[1].find_all("td")[4]["class"][1])
    ice = replace_multiplier(subResults[0].find_all("tr")[1].find_all("td")[5]["class"][1])
    fig = replace_multiplier(subResults[0].find_all("tr")[1].find_all("td")[6]["class"][1])
    poi = replace_multiplier(subResults[0].find_all("tr")[1].find_all("td")[7]["class"][1])
    gro = replace_multiplier(subResults[0].find_all("tr")[1].find_all("td")[8]["class"][1])
    fly = replace_multiplier(subResults[1].find_all("tr")[1].find_all("td")[0]["class"][1])
    psy = replace_multiplier(subResults[1].find_all("tr")[1].find_all("td")[1]["class"][1])
    bug = replace_multiplier(subResults[1].find_all("tr")[1].find_all("td")[2]["class"][1])
    roc = replace_multiplier(subResults[1].find_all("tr")[1].find_all("td")[3]["class"][1])
    gho = replace_multiplier(subResults[1].find_all("tr")[1].find_all("td")[4]["class"][1])
    dra = replace_multiplier(subResults[1].find_all("tr")[1].find_all("td")[5]["class"][1])
    dar = replace_multiplier(subResults[1].find_all("tr")[1].find_all("td")[6]["class"][1])
    ste = replace_multiplier(subResults[1].find_all("tr")[1].find_all("td")[7]["class"][1])
    fai = replace_multiplier(subResults[1].find_all("tr")[1].find_all("td")[8]["class"][1])
    pokeCurrent.extend((pokeNo, pokeName, pokeType1, pokeType2, 
                        nor, fir, wat, ele, gra, ice, fig, poi, gro, 
                        fly, psy, bug, roc, gho, dra, dar, ste, fai))
    meta.append(pokeCurrent)

# Creating a dataframe
import pandas as pd
df = pd.DataFrame.from_records(meta)
df.columns = ['NationalNumber', 'Pokemon', 'Type_1', 'Type_2', 
             'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison', 'Ground',
             'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']

# Export CSV file
df.to_csv('pokemons.csv', index = False)











