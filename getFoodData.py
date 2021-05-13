import csv
import pandas as pd
from collections import Counter
from nltk.tokenize import RegexpTokenizer
import time



def getFoodIdDf(description, foodIdFilePath="foodData/input_food.csv"):
    colList = ["sr_description", "fdc_id"]
    df = pd.read_csv(foodIdFilePath, usecols=colList)

    tokenizer = RegexpTokenizer(r'\w+')
    inputDescriptionTokensCount = Counter(
        tokenizer.tokenize(description.lower()))
    maxMatches = 0
    bestMatch = "No Match"

    for _, row in df.iterrows():
        descriptionTokensCount = Counter(tokenizer.tokenize(row["sr_description"].lower()))
        matches = descriptionTokensCount & inputDescriptionTokensCount
        if len(descriptionTokensCount) > 0:
            numMatches = sum(matches.values()) / len(descriptionTokensCount)
            if numMatches > maxMatches:
                maxMatches = numMatches
                bestMatch = row["fdc_id"]

    return bestMatch


def getFoodIdCsv(description, foodIdFilePath="foodData/input_food.csv"):
    openFoodIdFile = open(foodIdFilePath)

    tokenizer = RegexpTokenizer(r'\w+')
    inputDescriptionTokensCount = Counter(
        tokenizer.tokenize(description.lower()))
    maxMatches = 0
    bestMatch = "No Match"

    for row in csv.reader(openFoodIdFile):
        descriptionTokensCount = Counter(tokenizer.tokenize(row[6].lower()))
        matches = descriptionTokensCount & inputDescriptionTokensCount
        if len(descriptionTokensCount) > 0:
            numMatches = sum(matches.values()) / len(descriptionTokensCount)
            if numMatches > maxMatches:
                maxMatches = numMatches
                bestMatch = row[1]
                
    return bestMatch


def getNutrientAmount(foodId, nutrientId=1008, nutrientFilePath="foodData/food_nutrient.csv"):
    df = pd.read_csv(nutrientFilePath, low_memory=False)
    food_row = df.loc[(df['fdc_id'] == foodId) & (df['nutrient_id'] == nutrientId)]
    nutrientAmt = food_row["amount"].iloc[0]
    return nutrientAmt

def getNutrientAmount2(foodId, nutrientId='1008', nutrientFilePath="foodData/food_nutrient.csv"):
    openNutrientFile = open(nutrientFilePath)
    for row in csv.reader(openNutrientFile):
        if row[1] == foodId and row[2] == nutrientId:
            nutrientAmt = row[3]
            return float(nutrientAmt)
