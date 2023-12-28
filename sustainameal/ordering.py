from .utils import create_dict_ing_cfp_wfp
from .utils import get_recipes_index
import numpy as np
import ast
import pandas as pd


def sort_recipes_by_healthiness_score(nearest_recipes_df, recipes_df, score_field):
    """
    Sorts recipes based on a specified score field.

    Args:
    nearest_recipes_df (pd.DataFrame): DataFrame containing the nearest recipes.
    recipes_df (pd.DataFrame): DataFrame containing the original recipes with score fields.
    score_field (str): The field name of the score to sort by (e.g., 'who_score').

    Returns:
    pd.DataFrame: A DataFrame of the sorted nearest recipes, including their titles and scores.
    """

    # Ensure the recipe IDs are in the correct format for indexing
    recipe_ids = nearest_recipes_df['recipe_id'].tolist()

    # Filter the main recipes DataFrame to only include the nearest recipes
    filtered_recipes_df = recipes_df[recipes_df['recipe_id'].isin(recipe_ids)]

    # Sort the filtered DataFrame based on the score field
    sorted_recipes_df = filtered_recipes_df.sort_values(by=score_field, ascending=False)

    # Select only relevant columns and the top 10 recipes
    top_sorted_recipes = sorted_recipes_df[['title', score_field]]

    # Return the sorted and filtered DataFrame
    return top_sorted_recipes


def calculate_iss(ingredient, ingredient_dict):
    a = 0.8
    b = 0.2

    min_co2 = float(ingredient_dict['co2'][np.argmin(ingredient_dict['co2'])])
    max_co2 = float(ingredient_dict['co2'][np.argmax(ingredient_dict['co2'])])
    min_wfp = float(ingredient_dict['wfp'][np.argmin(ingredient_dict['wfp'])])
    max_wfp = float(ingredient_dict['wfp'][np.argmax(ingredient_dict['wfp'])])

    try:
        index = ingredient_dict['name'].index(ingredient)

        ncfp = (float(ingredient_dict['co2'][index]) - min_co2) / (max_co2 - min_co2)
        nwfp = (float(ingredient_dict['wfp'][index]) - min_wfp) / (max_wfp - min_wfp)

        return ingredient_dict['name'][index], a * ncfp + b * nwfp
    except:
        return None


def calculate_dss_score_recipe(recipe_index, recipes_df, ingredient_dict):
    sum = 0
    e = 2.71
    iss_recipe = []
    unique_ings = set()

    dati_dict = ast.literal_eval(recipes_df.iloc[recipe_index]['ingredients'])

    for value in dati_dict.values():
        for item in value:
            first_word = item[0].split(',')[0] if ',' in str(item[0]) else str(item[0])
            unique_ings.add(first_word)

    for ing in unique_ings:
        iss = calculate_iss(ing, ingredient_dict)

        if iss is not None:
            iss_recipe.append(iss)

    iss_recipe.sort(key=lambda x: x[1], reverse=True)

    for i in range(len(iss_recipe) - 1):
        sum = sum + iss_recipe[i][1] * (e ** (-i))

    return sum


def calculate_ss_recipe(dss, recipe_index):
    return (dss[recipe_index] - dss[np.argmin(dss)]) / (dss[np.argmax(dss)] - dss[np.argmin(dss)])


def sort_recipes_by_sustainability_score(nearest_recipes_df, recipes_df, ingredients_df):
    dss = []
    nearest_recipes_titles = nearest_recipes_df['title'].tolist()
    index_list = get_recipes_index(nearest_recipes_titles, recipes_df)
    ingredient_dict = create_dict_ing_cfp_wfp(recipes_df, ingredients_df, index_list)
    recipes_with_sustainability = {}

    for i in range(len(index_list)):
        dss.append(calculate_dss_score_recipe(index_list[i], recipes_df, ingredient_dict))

    for i in range(len(nearest_recipes_titles)):
        recipes_with_sustainability[nearest_recipes_titles[i]] = calculate_ss_recipe(dss, i)

    # Ordina il dizionario in base ai valori di sostenibilità (punteggi)
    sorted_recipes = dict(sorted(recipes_with_sustainability.items(), key=lambda item: item[1], reverse=True))

    df = pd.DataFrame(list(sorted_recipes.items()), columns=['Recipe', 'Sustainability Score'])

    return df
