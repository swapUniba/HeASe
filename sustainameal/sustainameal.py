import pandas as pd

from .nutrition_vectorizer import NutritionVectorizer
from .transformer_embeddings import RecipeTransformer
from .preprocessing import remove_duplicate_titles, remove_recipes_without_tags, clean_ingredients_dataframe
from .search import find_similar_by_title, find_nearest_recipes_by_tags_and_id, \
    find_nearest_recipes_by_nutrients_and_tags
from .utils import calculate_centroid_and_find_common_tags
from .ordering import sort_recipes_by_healthiness_score, sort_recipes_by_sustainability_score


class SustainaMeal:
    def __init__(self, recipes_df, nutrients,
                 transformer_name='davanstrien/autotrain-recipes-2451975973'):
        """
        Initializes the system by loading the data and preparing the embeddings.

        :param recipe_df: Datframe containing the recipes.
        :param nutrients: List of nutrient names to use.
        :param transformer_name: Name of the transformer model to use for embeddings.

        """

        # Preprocess recipes dataframe
        recipes_df = remove_duplicate_titles(recipes_df)
        recipes_df = remove_recipes_without_tags(recipes_df)

        self.recipes_df = recipes_df

        # Create an instance of RecipeTransformer
        self.transformer = RecipeTransformer(transformer_name)

        # List of nutrients to be used for vector space representation
        self.nutrients = nutrients

        # Initialize embeddings and nutrient vectors as None before calling setup
        self.title_embeddings = None
        self.nutrient_vectors_df = None

        # Call the internal method to perform setup tasks
        self._initialize_system()

    def _initialize_system(self):
        """
        Private method to initialize the embeddings and the vector space for the recipes.
        """
        # Process the titles through the transformer to get embeddings
        titles = self.recipes_df['title'].tolist()
        self.title_embeddings = self.transformer.process_batch(titles)

        # Initialize and fit the NutritionVectorizer and transform the nutrient data
        self.vectorized = NutritionVectorizer(self.nutrients)
        self.nutrient_vectors_df = self.vectorized.fit_transform(self.recipes_df)

    def find_similar_recipes(self, input_text, k, acceptable_tags, match_all_tags):
        """
        Finds recipes similar to the given input text.

        :param input_text: The input text to find similar recipes for.
        :param k: Number of similar recipes to return.
        :param acceptable_tags: List of tags considered acceptable for filtering recipes.
        :return: A list of tuples with similar recipes and their similarity scores.
        """
        # Ensure that the title embeddings have been computed
        if self.title_embeddings is None:
            raise ValueError("Title embeddings have not been initialized.")

        entities_list = list(zip(self.recipes_df['recipe_id'].tolist(), self.recipes_df['title'].tolist()))

        # Use the find_similar_by_title function to find similar recipes
        similar_recipes_by_title = find_similar_by_title(input_text, k, entities_list, self.title_embeddings,
                                                         self.transformer)

        (recipe_id_to_use, recipe_title), similarity_score = similar_recipes_by_title[0]

        # Proceed only if the similarity score is greater than 0.99 (step 1)
        if similarity_score > 0.99:
            # Extract the tags of the corresponding recipe
            tags_of_most_similar_recipe = \
                self.recipes_df.loc[self.recipes_df['recipe_id'] == recipe_id_to_use, 'tags'].iloc[0]
            # Ensure the 'tags' column in the DataFrame is formatted as a list; otherwise, convert it
            if isinstance(tags_of_most_similar_recipe, str):
                tags_of_most_similar_recipe = eval(tags_of_most_similar_recipe)

            # Filter tags to include only those that are acceptable
            tags_to_match = [tag for tag in tags_of_most_similar_recipe if tag in acceptable_tags]

            tags_to_match.append('healthy')  # We add the 'healthy' tag for recovery
            # print("tags_to_match:", tags_to_match)

            # Calculate the nearest recipes
            self.nearest_recipes = find_nearest_recipes_by_tags_and_id(recipe_id_to_use, self.recipes_df,
                                                                       self.nutrient_vectors_df, tags_to_match,
                                                                       match_all_tags, n=k, distance_metric='cosine')
        else:
            recipe_ids = [recipe[0] for recipe in similar_recipes_by_title]

            # Calcola il centroide nutrizionale e trova i tag più comuni
            centroid, common_tags = calculate_centroid_and_find_common_tags(recipe_ids, self.recipes_df,
                                                                            self.nutrients, self.vectorized)

            # print("Centroide nutrizionale:", centroid)
            # print("6 tag più comuni:", common_tags)

            # Filtra i tag per includere solo quelli accettabili
            tags_to_match = [tag for tag in common_tags if tag in acceptable_tags]
            tags_to_match.append('healthy')  # aggiungiamo healthy per cercare ricette più salutari

            # print("tags_to_match:", tags_to_match)

            self.nearest_recipes = find_nearest_recipes_by_nutrients_and_tags(centroid, self.recipes_df,
                                                                              self.nutrient_vectors_df, tags_to_match,
                                                                              match_all_tags=True, n=k,
                                                                              distance_metric='cosine')
        return self.nearest_recipes

    def get_similar_by_title(self, input_text, k):
        entities_list = list(zip(self.recipes_df['recipe_id'].tolist(), self.recipes_df['title'].tolist()))
        return find_similar_by_title(input_text, k, entities_list, self.title_embeddings,
                                     self.transformer)

    def order_recipe_by_healthiness(self, score='who_score'):
        return sort_recipes_by_healthiness_score(self.nearest_recipes, self.recipes_df, score)

    def order_recipe_by_sustainability(self, score='sustainability_score'):
        return sort_recipes_by_sustainability_score(self.nearest_recipes, self.recipes_df, score)
