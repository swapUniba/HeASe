# test_sustainameal.py
import pandas as pd
from sustainameal import SustainaMeal


def test_find_similar_recipes():
    recipes_df = pd.read_csv("data/final_recipes_set.csv")

    # Creazione dell'istanza di SustainaMeal
    sustainameal = SustainaMeal(
        recipes_df[:1000],
        ['calories [cal]', 'totalFat [g]', 'saturatedFat [g]', 'cholesterol [mg]', 'sodium [mg]', 'dietaryFiber [g]',
         'sugars [g]', 'protein [g]'],
        False,
        'davanstrien/autotrain-recipes-2451975973'
    )

    similar_recipes = sustainameal.find_similar_recipes('Boiled Radishes', 10,
                                                        acceptable_tags=['appetizers', 'main-dish', 'side-dishes',
                                                                         'drinks', 'beverages', 'fruits', 'desserts',
                                                                         'breakfast', 'pasta-rice-and-grains', 'rice',
                                                                         'pasta', 'pizza', 'breads', 'meat', 'fish',
                                                                         'seafood', 'beef', 'chicken', 'vegetarian'],
                                                        match_all_tags=False, check_sustainability=False)

    print(similar_recipes)

    ordered_recipes = sustainameal.order_recipe_by_healthiness()
    print(ordered_recipes)
    ordered_recipes_sus = sustainameal.order_recipe_by_sustainability()
    print(ordered_recipes_sus)
    order_recipes_final = sustainameal.order_recipe_by_sustainameal()
    print(order_recipes_final)

    # sustainameal.setup_openai_key("open-ai-key")
    # best_choice_by_llm = sustainameal.choose_best_recipe_with_gpt()
    # print(sustainameal.original_scores[0]['who_score'])

    # print(order_recipes_final)
    # print(best_choice_by_llm)
    #sustainameal.setup_openai_key("your-openai-key")
    #sustainameal.create_agent()
    #print(sustainameal.agent_ask("Can you suggest an alternative recipe to Pasta alla carbonara?"))


# Esecuzione del test
if __name__ == "__main__":
    test_find_similar_recipes()
    print("Test completato con successo!")
