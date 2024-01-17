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

def sort_recipes_by_sustainability_score(nearest_recipes_df, recipes_df, score_field, secondary_sort_field='who_score'):

    """
    Sorts recipes based on a specified score field with a secondary field.

    Args:
    nearest_recipes_df (pd.DataFrame): DataFrame containing the nearest recipes.
    recipes_df (pd.DataFrame): DataFrame containing the original recipes with score fields.
    score_field (str): The field name of the score to sort by (e.g., 'sustainability_label','sustainability_score').

    Returns:
    pd.DataFrame: A DataFrame of the sorted nearest recipes, including their titles and scores.
    """

    # Ensure the recipe IDs are in the correct format for indexing
    recipe_ids = nearest_recipes_df['recipe_id'].tolist()

    # Filter the main recipes DataFrame to only include the nearest recipes
    filtered_recipes_df = recipes_df[recipes_df['recipe_id'].isin(recipe_ids)]



    # Sort the filtered DataFrame based on the score field, and then by the secondary_sort_field
    sorted_recipes_df = filtered_recipes_df.sort_values(by=[score_field, secondary_sort_field], ascending=[True, False])

    sorted_recipes_df['percentage_sustainability_increment'] = ((filtered_recipes_df['sustainability_score'] - input_recipe_sus_score) / input_recipe_sus_score) * -100
    sorted_recipes_df['percentage_healthiness_increment'] = ((filtered_recipes_df['who_score'] - input_recipe_heal_score) / input_recipe_heal_score) * -100

    # Select only relevant columns and the top recipes
    top_sorted_recipes = sorted_recipes_df[['title', score_field, secondary_sort_field, 'final_score', 'percentage_sustainability_increment', 'percentage_healthiness_increment', 'percentage_final_score_increment']]

    # Return the sorted and filtered DataFrame
    return top_sorted_recipes


