# SustainaMeal

## Introduction
`SustainaMeal` is a Python library designed to suggest alternative recipes for healthier or more sustainable options. Leveraging machine learning and natural language processing, it compares nutritional profiles and semantic similarities to provide recipe recommendations.

## Architecture
The library consists of several modules:

- **Data Preprocessing**: Remove unnecessary recipe data.
- **Transformer Embeddings**: Generates text embeddings for recipe titles using a transformer model.
- **Nutritional Vector Space**: Maps recipes into a vector space based on nutritional content.
- **Similarity Search**: Executes cosine similarity searches for finding matching recipes.

![SustainaMeal Architecture](docs/architecture.png)

## Installation
Install `SustainaMeal` using pip:

```bash
pip install git+https://github.com/GiovTemp/SustainaMeal.git
```

## Usage

```bash
from sustainameal import SustainaMeal

sm = SustainaMeal(
    recipes_df="recipes_df",
    ingredients_df="ingredients_df",
    nutrients=['calories', 'fat', 'protein', ...],
    transformer_name='your_transformer_model'
)
```

## Find similar recipes 
Initializes the system by loading the data and preparing the embeddings.

        :param recipe_df: Datframe containing the recipes.
        :param ingredients_df: Datframe containing the ingredients for the sustanability computation.
        :param nutrients: List of nutrient names to use.
        :param transformer_name: Name of the transformer model to use for embeddings. 

Default transformer davanstrien/autotrain-recipes-2451975973

```bash
similar_recipes = sm.find_similar_recipes("Quinoa Salad", k=5)
```

## Display the recommendations
```bash
for recipe in similar_recipes:
    print(recipe)
```
