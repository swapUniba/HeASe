# test_sustainameal.py
import pandas as pd
from sustainameal import SustainaMeal

def test_find_similar_recipes():

    recipes_df = pd.read_csv("data/recipes.csv")

    ingredients_df = pd.read_csv("data/cfp_wfp_ingredients.csv", sep=';')
    ingredients_df = ingredients_df.dropna()

    # Creazione dell'istanza di SustainaMeal
    sustainameal = SustainaMeal(
        recipes_df,
        ingredients_df,
        ['calories [cal]', 'totalFat [g]', 'protein [g]', 'sodium [mg]', 'saturatedFat [g]', 'sugars [g]'],
        'davanstrien/autotrain-recipes-2451975973'
    )

    # Test del metodo find_similar_recipes
    similar_recipes = sustainameal.find_similar_recipes('Pasta with tomato sauce', 5)

    print(similar_recipes)

    # Verifica che i risultati siano del tipo corretto e abbiano il numero atteso di elementi
    assert isinstance(similar_recipes, list), "Il risultato dovrebbe essere una lista"
    assert len(similar_recipes) == 5, "La lista dovrebbe contenere 5 ricette simili"

    # Qui puoi aggiungere ulteriori asserzioni per testare aspetti specifici dei risultati

# Esecuzione del test
if __name__ == "__main__":
    test_find_similar_recipes()
    print("Test completato con successo!")


