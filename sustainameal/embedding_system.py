import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.preprocessing import StandardScaler

class SustainaMeal:
    def __init__(self, recipe_csv, ingredients_csv, transformer_name, nutrients):
        """
        Initializes the system by loading the data and preparing the embeddings.

        :param recipe_csv: Path to the CSV file containing the recipes.
        :param ingredients_csv: Path to the CSV file containing the ingredients.
        :param transformer_name: Name of the transformer model to use for embeddings.
        :param nutrients: List of nutrient names to use.
        """
        # Load the recipes and ingredients data from CSV files
        self.recipes_df = pd.read_csv(recipe_csv)
        self.ingredients_df = pd.read_csv(ingredients_csv)

        # Load the transformer model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(transformer_name)
        self.model = AutoModel.from_pretrained(transformer_name)

        # List of nutrients to be used for vector space representation
        self.nutrients = nutrients

        # Initialize embeddings and nutrient vectors as None before calling setup
        self.title_embeddings = None
        self.nutrient_vectors_df = None

        # Initialize a StandardScaler for nutrient normalization
        self.scaler = StandardScaler()

        # Call the internal method to perform setup tasks
        self._initialize_system()

    def _initialize_system(self):
        """
        Private method to initialize the embeddings and the vector space for the recipes.
        """
        # Calculate the title embeddings of the recipes
        titles = self.recipes_df['title'].tolist()
        encodings = self.tokenizer(titles, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            self.title_embeddings = self.model(**encodings).pooler_output

        # Normalize the nutrient values using the scaler
        nutrient_data = self.recipes_df[self.nutrients]
        self.nutrient_vectors_df = pd.DataFrame(
            self.scaler.fit_transform(nutrient_data),
            columns=self.nutrients
        )
        # Add the recipe IDs to the nutrient vectors DataFrame
        self.nutrient_vectors_df['recipe_id'] = self.recipes_df['recipe_id']
