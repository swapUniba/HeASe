import pandas as pd

from .nutrition_vectorizer import NutritionVectorizer
from .transformer_embeddings import RecipeTransformer
from .preprocessing import remove_duplicate_titles, remove_recipes_without_tags
from .search import find_similar_by_title

class SustainaMeal:
    def __init__(self, recipes_df, ingredients_df, nutrients, transformer_name='davanstrien/autotrain-recipes-2451975973'):
        """
        Initializes the system by loading the data and preparing the embeddings.

        :param recipe_df: Datframe containing the recipes.
        :param ingredients_df: Datframe containing the ingredients for the sustanability computation.
        :param nutrients: List of nutrient names to use.
        :param transformer_name: Name of the transformer model to use for embeddings.

        """
        # Load the recipes and ingredients data from CSV files
        self.ingredients_df = ingredients_df

        #Preprocess recipes dataframe
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
        vectorized = NutritionVectorizer(self.nutrients)
        self.nutrient_vectors_df = vectorized.fit_transform(self.recipes_df)


    def find_similar_recipes(self, input_text, k):
        """
        Finds recipes similar to the given input text.

        :param input_text: The input text to find similar recipes for.
        :param k: Number of similar recipes to return.
        :return: A list of tuples with similar recipes and their similarity scores.
        """
        # Ensure that the title embeddings have been computed
        if self.title_embeddings is None:
            raise ValueError("Title embeddings have not been initialized.")

        # Use the find_similar function to find similar recipes
        similar_recipes = find_similar_by_title(input_text, k, self.recipes_df['title'].tolist(),
                                       self.title_embeddings, self.transformer)

        return similar_recipes
