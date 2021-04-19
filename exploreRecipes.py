import os
import os.path
import shutil
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
    legal_measurements = ["gram", "grams", "cup", "tablespoon", "tablespoons", "teaspoon", "teaspoons", "kilogram", "kilograms", "pound", "pounds", "lbs", "milligram", "milligrams", "ounce", "ounces", "oz", "fl", "litre", "litres", "liter", "liters"]

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
        amt = getNutrientAmount(int(food_id))
        calories += amt * (amount/100)

    return calories

if True:
    """ overall script that runs examples """

    # sign on
    print("[[ Start! ]]\n")

    print(calorie_count("recipes/savory_recipes/vegetarian_recipes/recipe38.txt"))

    print("\n[[ Fin. ]]")
