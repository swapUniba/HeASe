import numpy as np
import ast
import pandas as pd


def sort_recipes_by_healthiness_score(nearest_recipes_df, recipes_df, score_field, input_recipe_heal_score):
    """
    Sorts recipes based on a specified score field.

    Args:
    nearest_recipes_df (pd.DataFrame): DataFrame containing the nearest recipes.
    recipes_df (pd.DataFrame): DataFrame containing the original recipes with score fields.
    score_field (str): The field name of the score to sort by (e.g., 'who_score').
    input_recipe_heal_score (float): who_score of the input recipe

    Returns:
    pd.DataFrame: A DataFrame of the sorted nearest recipes, including their titles and scores.
    """

    # Ensure the recipe IDs are in the correct format for indexing
    recipe_ids = nearest_recipes_df['recipe_id'].tolist()

    # Filter the main recipes DataFrame to only include the nearest recipes
    filtered_recipes_df = recipes_df[recipes_df['recipe_id'].isin(recipe_ids)]

    # Sort the filtered DataFrame based on the score field
    sorted_recipes_df = filtered_recipes_df.sort_values(by=score_field, ascending=False)
    sorted_recipes_df['healthiness_increment'] = ((filtered_recipes_df[
                                                       'who_score'] - input_recipe_heal_score) / input_recipe_heal_score) * 100

    # Select only relevant columns and the top 10 recipes
    top_sorted_recipes = sorted_recipes_df[['title', score_field, 'healthiness_increment']]

    # Return the sorted and filtered DataFrame
    return top_sorted_recipes


def sort_recipes_by_sustainability_score(nearest_recipes_df, recipes_df, score_field, secondary_sort_field,
                                         input_recipe_sus_score):
    """
    Sorts recipes based on a specified score field with a secondary field.

    Args:
    nearest_recipes_df (pd.DataFrame): DataFrame containing the nearest recipes.
    recipes_df (pd.DataFrame): DataFrame containing the original recipes with score fields.
    score_field (str): The field name of the score to sort by (e.g., 'sustainability_label','sustainability_score').
    secondary_sort_field (str): The field name of the secondary score to sort by
    input_recipe_heal_score (float): sustainability_score of the input recipe

    Returns:
    pd.DataFrame: A DataFrame of the sorted nearest recipes, including their titles and scores.
    """

    # Ensure the recipe IDs are in the correct format for indexing
    recipe_ids = nearest_recipes_df['recipe_id'].tolist()

    # Filter the main recipes DataFrame to only include the nearest recipes
    filtered_recipes_df = recipes_df[recipes_df['recipe_id'].isin(recipe_ids)]

    # Sort the filtered DataFrame based on the score field, and then by the secondary_sort_field
    sorted_recipes_df = filtered_recipes_df.sort_values(by=[score_field, secondary_sort_field], ascending=[True, False])

    sorted_recipes_df['sustainability_increment'] = ((filtered_recipes_df[
                                                          'sustainability_score'] - input_recipe_sus_score) / input_recipe_sus_score) * 100

    # Select only relevant columns and the top recipes
    top_sorted_recipes = sorted_recipes_df[['title', score_field, secondary_sort_field, 'sustainability_increment']]

    # Return the sorted and filtered DataFrame
    return top_sorted_recipes


def sort_recipes_by_sustainameal_score(nearest_recipes_df, recipes_df, input_recipe_sus_score, input_recipe_heal_score,
                                       alpha, beta):
    """
    Sorts recipes based on a specified score field with a secondary field.

    Args:
    nearest_recipes_df (pd.DataFrame): DataFrame containing the nearest recipes.
    recipes_df (pd.DataFrame): DataFrame containing the original recipes with score fields.
    score_field (str): The field name of the score to sort by (e.g., 'sustainability_label','sustainability_score').
    secondary_sort_field (str): The field name of the secondary score to sort by
    input_recipe_heal_score (float): sustainability_score of the input recipe

    Returns:
    pd.DataFrame: A DataFrame of the sorted nearest recipes, including their titles and scores.
    """

    # Ensure the recipe IDs are in the correct format for indexing
    recipe_ids = nearest_recipes_df['recipe_id'].tolist()

    # Filter the main recipes DataFrame to only include the nearest recipes
    filtered_recipes_df = recipes_df[recipes_df['recipe_id'].isin(recipe_ids)]

    filtered_recipes_df['sustainameal_score'] = filtered_recipes_df.apply(
        lambda row: calculate_sustainameal_score(row, alpha, beta), axis=1)

    # Sort the filtered DataFrame based on the score field, and then by the secondary_sort_field
    sorted_recipes_df = filtered_recipes_df.sort_values(by=['sustainameal_score'], ascending=[False])

    sorted_recipes_df['sustainability_increment'] = ((filtered_recipes_df[
                                                          'sustainability_score'] - input_recipe_sus_score) / input_recipe_sus_score) * 100

    sorted_recipes_df['healthiness_increment'] = ((filtered_recipes_df[
                                                       'who_score'] - input_recipe_heal_score) / input_recipe_heal_score) * 100

    # Select only relevant columns and the top recipes
    top_sorted_recipes = sorted_recipes_df[
        ['title', 'who_score', 'healthiness_increment', 'sustainability_score', 'sustainability_increment','sustainameal_score']]

    # Return the sorted and filtered DataFrame
    return top_sorted_recipes


def calculate_sustainameal_score(row, alpha, beta):

    sustainameal_score = (1-row['sustainability_score']) * alpha + row['who_score'] * beta
    return sustainameal_score
