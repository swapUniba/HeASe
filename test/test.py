# test_sustainameal.py
import pandas as pd
from sustainameal import SustainaMeal


def test_find_similar_recipes():
    recipes_df = pd.read_csv("data/final_recipes_set.csv")

    # Creazione dell'istanza di SustainaMeal
    sustainameal = SustainaMeal(
        recipes_df[:100],
        ['calories [cal]', 'totalFat [g]', 'saturatedFat [g]', 'cholesterol [mg]', 'sodium [mg]', 'dietaryFiber [g]',
         'sugars [g]', 'protein [g]'],
        'davanstrien/autotrain-recipes-2451975973'
    )

    similar_recipes_by_title = sustainameal.get_similar_by_title('Beef', 10)
    print(similar_recipes_by_title)
    similar_recipes = sustainameal.find_similar_recipes('Cukes and Onions', 10,
                                                        acceptable_tags=['appetizers', 'main-dish', 'side-dishes',
                                                                         'fruits', 'desserts',
                                                                         'breakfast', 'pasta-rice-and-grains',
                                                                         'beverages', 'drinks', 'pasta'],
                                                        match_all_tags=False, check_sustainability=False)

    #print(similar_recipes)

    # ordered_recipes = sustainameal.order_recipe_by_healthiness()
    # ordered_recipes_sus = sustainameal.order_recipe_by_sustainability()
    #order_recipes_final = sustainameal.order_recipe_by_sustainameal()

    #sustainameal.setup_key("your_api_key")
    #best_choice_by_llm = sustainameal.choose_best_recipe_with_gpt()

    #print(order_recipes_final)
    #print(best_choice_by_llm)


# Esecuzione del test
if __name__ == "__main__":
    test_find_similar_recipes()
    print("Test completato con successo!")
