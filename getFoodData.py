import csv
import pandas as pd
from collections import Counter
from nltk.tokenize import RegexpTokenizer


def getFoodId(description, foodIdFilePath="foodData/input_food.csv"):
    openFoodIdFile = open(foodIdFilePath)
    # print(description)
    tokenizer = RegexpTokenizer(r'\w+')
    inputDescriptionTokensCount = Counter(
        tokenizer.tokenize(description.lower()))
    maxMatches = 0
    bestMatch = "No Match"

    for row in csv.reader(openFoodIdFile):
        # descriptionTokens = re.split("_|, | |-|!", row[2]) #Reg ex tokenizer
        descriptionTokensCount = Counter(tokenizer.tokenize(row[6].lower()))
        # print(descriptionTokensCount)
        matches = descriptionTokensCount & inputDescriptionTokensCount
        if len(descriptionTokensCount) > 0:
            numMatches = sum(matches.values()) / len(descriptionTokensCount)
            if numMatches > maxMatches:
                maxMatches = numMatches
                bestMatch = row[0]
                # print("\n")
                # print(description)
                # print(bestMatch)
                # print(descriptionTokensCount)
                # print("\n")

    return bestMatch


def getNutrientAmount(foodId, nutrientId=2048, nutrientFilePath="foodData/food_nutrient.csv"):
    df = pd.read_csv(nutrientFilePath)
    food_row = df.loc[(df['fdc_id'] == foodId) & (df['nutrient_id'] == nutrientId)]
    nutrientAmt = food_row['amount'][:,0]
    return nutrientAmt
