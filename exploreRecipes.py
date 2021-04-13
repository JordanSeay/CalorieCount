import os
import os.path
import shutil
from getFoodData import getFoodId


def do_recipes(path):
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


def most_kilograms(path):
    """
        Walks through all recipes in a given path,
        returning the recipe, ingredient and amount of ingredient
        that uses the most kilograms
    """
    AllFiles = list(os.walk(path))

    most = 0
    recipe = None
    ingredient = None

    for item in AllFiles:
        foldername, _, LoFiles = item   # cool unpacking!
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                f = open(fullfilename, "r", encoding="latin1")
                contents = f.read()
                if " kilograms " in contents:
                    words = contents.split()   # list of words in the contents
                    # index of the word "kilograms"
                    kilograms_index = words.index("kilograms")
                    if float(words[kilograms_index-1]) > float(most):
                        most = words[kilograms_index-1]
                        recipe = fullfilename
                        ingredient = f"{words[kilograms_index+2]}"
                f.close()
    return most, recipe, ingredient


def ingredient_count(path):
    """
    Walks through all recipes in a path, returning a dictionary
    of all ingredient occurances and how many times they occur
    """
    AllFiles = list(os.walk(path))

    ingredients = dict()
    for item in AllFiles:
        foldername, _, LoFiles = item   # cool unpacking!
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                f = open(fullfilename, "r", encoding="latin1")
                contents = f.read()
                words = contents.split("\n")   # list of words in the contents
                # index of the word "Ingredients"
                ingredientsIndex = words.index("Ingredients:")
                instructionsIndex = words.index("Instructions:")
                # walk through all ingredients
                for i in range(ingredientsIndex+2, instructionsIndex):
                    line = words[i].split()
                    # we only want actual ingredients, not instructions
                    if len(line) == 0 or "of" not in line:
                        continue
                    ofIndex = line.index("of")
                    ingredient = " ".join(line[ofIndex+1:])
                    if ingredient not in ingredients:
                        ingredients[ingredient] = 1
                    else:
                        ingredients[ingredient] += 1
                f.close()
    return ingredients


def average_ingredient_list(path):
    """
    Walks through all recipes in a path, returning the average
    number of ingredients per recipe
    """
    AllFiles = list(os.walk(path))

    numIngredients = 0
    count = 0
    for item in AllFiles:
        foldername, _, LoFiles = item   # cool unpacking!
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                f = open(fullfilename, "r", encoding="latin1")
                contents = f.read()
                words = contents.split("\n")   # list of WORDS in the contents
                # index of the word "Ingredients"
                ingredientsIndex = words.index("Ingredients:")
                instructionsIndex = words.index("Instructions:")
                # walk through all ingredients
                count += 1
                for i in range(ingredientsIndex+2, instructionsIndex):
                    line = words[i].split()
                    if len(line) == 0 or "of" not in line:
                        continue
                    numIngredients += 1
                f.close()
    return numIngredients / count


def average_bake_time(path):
    """
    Walks through all recipes in a path, returning the average
    bake time per recipe
    """
    AllFiles = list(os.walk(path))

    time = 0
    count = 0
    for item in AllFiles:
        foldername, _, LoFiles = item   # cool unpacking!
        for filename in LoFiles:
            if filename[-3:] == "txt":
                fullfilename = foldername + "/" + filename
                f = open(fullfilename, "r", encoding="latin1")
                contents = f.read()
                words = contents.split("\n")   # list of words in the contents
                count += 1
                baking = words[-2].split()
                # if the time is in hours we gotta convert
                if "hours" not in baking:
                    time += int(baking[-2])
                else:
                    time += int(baking[baking.index("hours")-1])*60
                    time += int(baking[baking.index("minutes")-1])
                f.close()
    return time / count


if True:
    """ overall script that runs examples """

    # sign on
    print("[[ Start! ]]\n")

    # do it
    do_recipes("./problem3")

    # most kilogs
    most = most_kilograms("./problem3")
    print(
        f"The {most[1]} recipe calls for {most[0]} kg of {most[2]}, which is the most kg of any recipe")

    # most frequent ingredient
    ingredientDict = ingredient_count("./problem3")
    print(
        f"The most frequent ingredient is {max(ingredientDict, key=lambda x: ingredientDict[x])}, occuring {max(ingredientDict.values())} times")

    # average ingredients per recipe
    avgIngred = average_ingredient_list("./problem3")
    print(f"The average recipe includes {avgIngred} ingredients")

    # average bake time
    avgBake = average_bake_time("./problem3")
    print(f"The average recipe takes {avgBake} minutes to bake")

    # TEST Ingredient Lookup 
    for ingred in ingredientDict.keys():
        print(ingred)
        print(getFoodId(ingred))

    # sign off
    print("\n[[ Fin. ]]")

# Investigation Questions
# What is the most frequent ingredient, and how often doe sit occur?
#   The most frequent ingredient is salt, occuring 164 times
# What is the average number of ingredients per recipe?
#   The average recipe includes 8.386454183266933 ingredients
# How long does it take to bake our pies, on average?
#   The average recipe takes 54.02390438247012 minutes to bake
