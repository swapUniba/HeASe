from .nutrition_vectorizer import NutritionVectorizer
from .transformer_embeddings import RecipeTransformer
from .preprocessing import remove_duplicate_titles, remove_recipes_without_tags
from .search import find_similar_by_title, find_nearest_recipes_by_tags_and_id, \
    find_nearest_recipes_by_nutrients_and_tags
from .utils import calculate_centroids_and_find_common_tags, save_data, load_data, save_dataframe, load_dataframe
from .ordering import sort_recipes_by_healthiness_score, sort_recipes_by_sustainability_score, \
    sort_recipes_by_sustainameal_score

import openai
import pandas as pd
import os
import pickle


class SustainaMeal:
    def __init__(self, recipes_df, nutrients, load=False,
                 transformer_name='davanstrien/autotrain-recipes-2451975973'):
        """
        Initializes the system by loading the data and preparing the embeddings.

        :param recipe_df: Datframe containing the recipes.
        :param nutrients: List of nutrient names to use.
        :param transformer_name: Name of the transformer model to use for embeddings.

        """

        # Preprocess recipes dataframe

        self.open_ai_key = None
        self.nearest_recipes = None

        # Create an instance of RecipeTransformer
        self.transformer = RecipeTransformer(transformer_name)

        # List of nutrients to be used for vector space representation
        self.nutrients = nutrients

        # Initialize embeddings and nutrient vectors as None before calling setup
        self.title_embeddings = None
        self.nutrient_vectors_df = None
        self.original_scores = None

        if load:
            self._load_saved_data()
        else:
            self._process_and_save_data(recipes_df)

        # Call the internal method to perform setup tasks
        self._initialize_system()

    def _load_saved_data(self):
        if os.path.exists('stored_data/processed_recipes_df.pkl'):
            self.recipes_df = pd.read_pickle('stored_data/processed_recipes_df.pkl')
        else:
            raise FileNotFoundError("Processed recipes DataFrame not found.")

        if os.path.exists('stored_data/title_embeddings.pkl'):
            with open('stored_data/title_embeddings.pkl', 'rb') as f:
                self.title_embeddings = pickle.load(f)
        else:
            raise FileNotFoundError("Title embeddings not found.")

        with open('stored_data/vectorized.pkl', 'rb') as f:
            self.vectorized = pickle.load(f)
            self.nutrient_vectors_df = self.vectorized.fit_transform(self.recipes_df)

    def _process_and_save_data(self, recipes_df):
        recipes_df = remove_duplicate_titles(recipes_df)
        recipes_df = remove_recipes_without_tags(recipes_df)
        self.recipes_df = recipes_df
        save_dataframe(self.recipes_df, 'stored_data/processed_recipes_df.pkl')


    def _initialize_system(self):
        """
        Private method to initialize the embeddings and the vector space for the recipes.
        """

        # Processa i titoli tramite il transformer per ottenere le embedding solo se non sono già stati caricati
        if self.title_embeddings is None:
            titles = self.recipes_df['title'].tolist()
            self.title_embeddings = self.transformer.process_batch(titles)
            save_data(self.title_embeddings, 'stored_data/title_embeddings.pkl')

        # Inizializza e adatta il NutritionVectorizer e trasforma i dati sui nutrienti solo se non sono già stati caricati
        if self.nutrient_vectors_df is None:
            self.vectorized = NutritionVectorizer(self.nutrients)
            with open('stored_data/vectorized.pkl', 'wb') as f:
                pickle.dump(self.vectorized, f)
            self.nutrient_vectors_df = self.vectorized.fit_transform(self.recipes_df)

    def find_similar_recipes(self, input_text, k, acceptable_tags, match_all_tags, check_sustainability=False, j=5):
        """
        Finds recipes similar to the given input text.

        :param input_text: The input text to find similar recipes for.
        :param k: Number of similar recipes to return.
        :param acceptable_tags: List of tags considered acceptable for filtering recipes.
        :param match_all_tags: Matching strategy
        :param check_sustainability: check if the desired recipe is sustainable
        :param j: number of recipes to consider in the centroid computation
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

            if check_sustainability:
                self.nearest_recipes = self.recipes_df[
                    (self.recipes_df['title'] == recipe_title) &
                    (self.recipes_df['sustainability_label'] == 0)
                    ]

                if not self.nearest_recipes.empty:
                    return self.nearest_recipes

            # Extract the tags of the corresponding recipe
            tags_of_most_similar_recipe = \
                self.recipes_df.loc[self.recipes_df['recipe_id'] == recipe_id_to_use, 'tags'].iloc[0]
            # Ensure the 'tags' column in the DataFrame is formatted as a list; otherwise, convert it
            if isinstance(tags_of_most_similar_recipe, str):
                tags_of_most_similar_recipe = eval(tags_of_most_similar_recipe)

            # Filter tags to include only those that are acceptable
            tags_to_match = [tag for tag in tags_of_most_similar_recipe if tag in acceptable_tags]

            print(f"Tags to match: {tags_to_match}")
            # tags_to_match.append('healthy')
            if len(tags_to_match) == 0:
                raise ValueError("No tag found to match.")
            # Save health score & sus score
            self.original_scores = self.recipes_df.loc[
                self.recipes_df['recipe_id'] == recipe_id_to_use, ['who_score', 'sustainability_score']].to_dict(
                orient='records')

            # Calculate the nearest recipes
            self.nearest_recipes = find_nearest_recipes_by_tags_and_id(recipe_id_to_use, self.recipes_df,
                                                                       self.nutrient_vectors_df, tags_to_match,
                                                                       match_all_tags, n=k, distance_metric='cosine')
        else:
            recipe_ids = [recipe[0] for recipe in similar_recipes_by_title[:j]]

            # Calculate the nutritional centroid and find the most common tags
            centroid, common_tags, mean_who_score, mean_sustainability_score = calculate_centroids_and_find_common_tags(
                recipe_ids, self.recipes_df,
                self.nutrients, self.vectorized)

            mean_scores_dict = {'who_score': mean_who_score, 'sustainability_score': mean_sustainability_score}

            self.original_scores = [mean_scores_dict]

            # Filter tags to include only those that are acceptable
            tags_to_match = [tag for tag in common_tags if tag in acceptable_tags]
            print(f"Tags to match: {tags_to_match}")
            # tags_to_match.append('healthy')
            if len(tags_to_match) == 0:
                raise ValueError("No tag found to match.")

            self.nearest_recipes = find_nearest_recipes_by_nutrients_and_tags(centroid, self.recipes_df,
                                                                              self.nutrient_vectors_df, tags_to_match,
                                                                              match_all_tags, n=k,
                                                                              distance_metric='cosine')
        return self.nearest_recipes

    def get_similar_by_title(self, input_text, k):
        entities_list = list(zip(self.recipes_df['recipe_id'].tolist(), self.recipes_df['title'].tolist()))
        return find_similar_by_title(input_text, k, entities_list, self.title_embeddings,
                                     self.transformer)

    def order_recipe_by_healthiness(self, nearest_recipes=None, score='who_score'):

        """
        Order the recipes obtained previously.

        :param (optional) nearest_recipes: Dataframe to order, if none the dataframe computed by find_similar_recipes will be used.
        :param score: The column name used as the primary sorting criterion.
        :return: A DataFrame of recipes ordered by the specified score.

        """
        if nearest_recipes is not None:
            return sort_recipes_by_healthiness_score(nearest_recipes, self.recipes_df, score,
                                                     self.original_scores[0]['who_score'])
        else:
            return sort_recipes_by_healthiness_score(self.nearest_recipes, self.recipes_df, score,
                                                     self.original_scores[0]['who_score'])

    def order_recipe_by_sustainability(self, nearest_recipes=None, score='sustainability_score',
                                       secondary_sort_field='who_score'):

        """
        Order the recipes obtained previously.

        :param (optional) nearest_recipes: Dataframe to order , if none the dataframe computed by find_similar_recipes will be used.
        :param score: The column name used as the primary sorting criterion.
        :param secondary_sort_field: The column name used as the secondary sorting criterion.
        :return: A Dataframe with recipes ordered by the given metric.
        """

        if nearest_recipes is not None:
            return sort_recipes_by_sustainability_score(nearest_recipes, self.recipes_df, score,
                                                        secondary_sort_field,
                                                        self.original_scores[0]['sustainability_score'])
        else:
            return sort_recipes_by_sustainability_score(self.nearest_recipes, self.recipes_df, score,
                                                        secondary_sort_field,
                                                        self.original_scores[0]['sustainability_score'])

    def order_recipe_by_sustainameal(self, nearest_recipes=None, alpha=0.7, beta=0.3):

        """
        Order the recipes obtained previously.


        :param (optional) nearest_recipes: Dataframe to order , if none the dataframe computed by find_similar_recipes will be used.
        :return: A Dataframe with recipes ordered by the given metric.
        :param alpha: weight for sustainability score
        :param beta: weight for healthiness score
        """

        if nearest_recipes is not None:
            return sort_recipes_by_sustainameal_score(nearest_recipes, self.recipes_df,
                                                      self.original_scores[0]['sustainability_score'],
                                                      self.original_scores[0]['who_score'],
                                                      alpha, beta)
        else:
            return sort_recipes_by_sustainameal_score(self.nearest_recipes, self.recipes_df,
                                                      self.original_scores[0]['sustainability_score'],
                                                      self.original_scores[0]['who_score'], alpha, beta)

    def setup_openai_key(self, open_ai_key):
        self.open_ai_key = open_ai_key

    def choose_best_recipe_with_gpt(self, nearest_recipes=None, alpha=0.7, beta=0.3):
        """
        Use an LLM to choose the best recipe from a list ordered by sustainability and healthiness.

        :param nearest_recipes: Optional DataFrame of recipes to order. If None, use the DataFrame from find_similar_recipes.
        :param alpha: Weight for sustainability score.
        :param beta: Weight for healthiness score.
        :return: The name of the best recipe chosen by GPT-3.5.
        """

        ordered_recipes = self.order_recipe_by_sustainameal(nearest_recipes, alpha, beta)

        # Verifica se il DataFrame 'ordered_recipes' è vuoto prima di procedere
        if ordered_recipes.empty:
            print("No recipes to order. Please provide a non-empty DataFrame.")
            return None

        prompt = "Using your knowledge please rank the following recipes from most to least recommended based on a balance of sustainability and healthiness:\n\n"
        prompt += "\n".join([
            f"{idx + 1}. Recipe: {row['title']}"
            for idx, row in ordered_recipes.iterrows()])
        prompt += "\n\nWhich one should I choose? Return just the name"

        # Assicurati di avere la tua chiave API configurata correttamente
        openai.api_key = self.open_ai_key

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
        except Exception as e:
            print("Errore nell'invio della richiesta all'API di OpenAI:", e)
            return None

        # Estrai la scelta migliore dalla risposta
        response_text = response.choices[0].message['content'].strip()

        # Analizza la risposta per ottenere il nome della ricetta
        # Assumiamo che il modello risponda con il nome della ricetta dopo "I should choose" o una frase simile.
        best_recipe_name = None
        print(response_text)
        for sentence in response_text.split('\n'):
            if "recipe:" in sentence.lower():
                best_recipe_name = sentence.split(":")[1].strip()  # Estrai il nome dopo 'Recipe:'
                break

        return best_recipe_name
