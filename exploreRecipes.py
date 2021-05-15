import os
import os.path
import shutil
import argparse
import numpy as np
from getFoodData import getFoodIdCsv, getNutrientAmount, getNutrientAmount2


def organize_recipes(path):
    """ walks a whole directory structure
        and organizes recipes
    """

    AllFiles = list(os.walk(path))
    try:
        os.mkdir("recipes")
        os.mkdir("recipes/savory_recipes")
        os.mkdir("recipes/sweet_recipes")
        os.mkdir("recipes/savory_recipes/vegetarian_recipes")
    except:
        # they already exist!
        print("folders already exist!")

    for item in AllFiles:
        foldername, _, LoFiles = item   # cool unpacking!
        if foldername != "recipes" and "recipes\\" not in foldername:  # don't look into our already sorted recipes!
            for filename in LoFiles:
                if filename[-3:] == "txt":
                    fullfilename = foldername + "/" + filename
                    f = open(fullfilename, "r", encoding="latin1")
                    contents = f.read()
                    if "Savory Pie" in contents:
                        if "pork" in contents or "beef" in contents or "chicken" in contents:
                            shutil.copy(
                                fullfilename, f"recipes/savory_recipes/{filename}")
                        else:
                            shutil.copy(
                                fullfilename, f"recipes/savory_recipes/vegetarian_recipes/{filename}")
                    else:
                        shutil.copy(
                            fullfilename, f"recipes/sweet_recipes/{filename}")
                    f.close()


def walk_ingredients(path):
    f = open(path, "r", encoding="latin1")
    contents = f.read()
    words = contents.split("\n")

    # Grab bounds of enumeration
    ingredients_index = words.index("Ingredients:")
    instructions_index = words.index("Instructions:")

    # Stores food items and grams
    food_and_weights = []
    # walk through all ingredients
    for i in range(ingredients_index+2, instructions_index):
        line = words[i].split()
        # we only want actual ingredients, not instructions
        if len(line) == 0 or "of" not in line:
            continue

        amt = parse_amount(line)
        if amt is not None:
            food_and_weights.append(parse_amount(line))
    f.close()
    return food_and_weights


def parse_amount(line):
    # for volume measurements, I'm assuming density of water for now
    # food_portion has actual volume-to-gram conversions but that might be difficult
    measurement_to_grams = {"gram": 1, "cup": 236.59, "tablespoon": 14.787, "teaspoon": 4.929, "kilogram": 1000, "pound": 453.592, "lbs": 453.592, "milligram": 0.001, "ounce": 28.3495, "oz": 28.3495, "fl": 28.3495, "litre": 1000, "liter": 1000}
    legal_measurements = ["gram", "grams", "cup", "cups", "tablespoon", "tablespoons", "teaspoon", "teaspoons", "kilogram", "kilograms", "pound", "pounds", "lbs", "milligram", "milligrams", "ounce", "ounces", "oz", "fl", "litre", "litres", "liter", "liters"]

    for i, word in enumerate(line):
        if word in legal_measurements and line[i-1].isdigit():
            of_index = line.index("of")
            ingredient = " ".join(line[of_index+1:])
            if word[-1] == 's':
                return (ingredient, float(line[i-1])*measurement_to_grams[word[:-1]])
            else:
                return (ingredient, float(line[i-1])*measurement_to_grams[word])

    return None


def calorie_count(path):
    ingredients_and_amounts = walk_ingredients(path)

    calories = 0
    for ingredient, amount in ingredients_and_amounts:
        food_id = getFoodIdCsv(ingredient)
        if food_id == "No Match":
            pass
        else:
            amt = getNutrientAmount(int(food_id))
            calories += amt * (amount/100)

    return calories


def count_all_recipes(path):
    """
    input: a directory to scrape for recipe.txt files
    output: .npz file containing {recipe: calorie count} pairs
    """
    all_files = list(os.walk(path))
    results = {}

    for item in all_files:
        foldername, _, lo_Files = item
        for filename in lo_Files:
                if filename[-3:] == "txt":
                    results[filename] = (calorie_count(foldername + "\\" + filename), walk_ingredients(foldername + "\\" + filename))
                    print(f"recipe counted {filename}")

    np.savez_compressed("allCounts", **results)

def filter_by_calorie(range):
    """
    input: List of size 2 with desired calorie range ex. [100, 2000]
    output: list of all recipes in the desired calorie range
    """
    try:
        calorie_counts = np.load("allCounts.npz", allow_pickle=True)
    except:
        print("Cannot find file allCounts.npz \n Please run python .\exploreRecipes.py -s to generate allCounts.npz")

    out = [] 
    for key, value in calorie_counts.items():
        calorieCount = int(value[0])
        if calorieCount >= int(range[0]) and calorieCount <= int(range[1]):
            out.append(key)
    return out


def print_recipes():
    try:
        calorie_counts = np.load("allCounts.npz", allow_pickle=True)
    except:
        print("Cannot find file allCounts.npz \n Please run python .\exploreRecipes.py -s to generate allCounts.npz")

    out = [] 
    for key, value in calorie_counts.items():
        out.append((key, value))
    return out


def filter_by_ingredients(ingredients, subset=False):
    """
    input: list of desired ingredients to filter by and whether or not the recipe must only contain those ingredients
    output: list of all recipes that either include at least one filtered ingredient, or consists of only filtered ingredients
    """

    try:
        calorie_counts = np.load("allCounts.npz", allow_pickle=True)
    except:
        print("Cannot find file allCounts.npz \n Please run python .\exploreRecipes.py -s to generate allCounts.npz")

    recipes = []

    if subset:
        for key, value in calorie_counts.items():
            include = True
            for ingredient, _ in value[1]:
                if ingredient not in ingredients:
                    include = False
                    break
            if include:
                recipes.append(key)
    else:
        for key, value in calorie_counts.items():
            for ingredient, _ in value[1]:
                if ingredient in ingredients:
                    recipes.append(key)
                    break
    return recipes


def main(args):
    if args.saveFile is not None:
        count_all_recipes(".\\problem3")
    if args.recipeName is not None:
        print(calorie_count(f"{args.recipeName}"))
    if args.filterByCalorie is not None:
        print(filter_by_calorie(args.filterByCalorie))
    if args.filterByIngredients is not None:
        l,b = args.filterByIngredients
        l = l.split(',')
        b = b.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
        print(filter_by_ingredients(l, b))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument(
        '--saveFile',
        '-s',
        action='store_true',
        help='Count calories and ingredients of all recipes',
    )
    parser.add_argument(
        '--recipeName',
        '-n',
        type=str,
        help="Name of recipe file"
    )
    parser.add_argument(
        '--filterByCalorie',
        '-f',
        type=int,
        nargs=2,
        help="Integers with desired calorie range (inclusive) of recipes ex. 100 2000 for range 100cal to 2000cal"
    )
    parser.add_argument(
        '--filterByIngredients',
        '-i',
        nargs=2,
        help="List of ingredients to filter by, and whether or not the list is exhaustive. eg <\"potato,garlic,onions\" True> will search for recipes that only contain potato,garlic,onions (or a subset) and nothing else"

    )
    args = parser.parse_args()
    main(args)    

# Examples:
#   To find all recipes that contain between 100 and 200 calories inclusively 
#   To save time this uses a precomputable calorie and ingredient count file called allCounts.npz
#   run: python .\exploreRecipes.py -f 100 200
#   returns: ['recipe25.txt', 'recipe37.txt', 'recipe127.txt', 'recipe159.txt', 'recipe169.txt', 'recipe201.txt']
#
#
#   To find all recipes that contain cumin, among other ingredients 
#   To save time this uses a precomputable calorie and ingredient count file called allCounts.npz
#   run: python .\exploreRecipes.py -i "cumin" False
#   returns: ['recipe14.txt', 'recipe15.txt', 'recipe6.txt', 'recipe7.txt']
#
#   
#   To find all recipes that contain a subset of chicken, tofu, parsley, chili powder, cumin, garlic, onions and shortening
#   To save time this uses a precomputable calorie and ingredient count file called allCounts.npz
#   run: python .\exploreRecipes.py -i "chicken,tofu,parsley,chili powder,cumin,garlic,onions,shortening" True
#   returns: ['recipe14.txt']
#
#
#   To find the calorie count of all recipes and store in allCounts.npz file 
#   run: python .\exploreRecipes.py -s
# 
#   To find the calorie count of a given recipe
#   run: python .\exploreRecipes.py -n recipes/savory_recipes/vegetarian_recipes/recipe38.txt
#   returns: 6960.94584
#