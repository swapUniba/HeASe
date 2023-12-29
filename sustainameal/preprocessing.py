# preprocessing.py
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from nltk.tag import pos_tag

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

def remove_duplicate_titles(df):
    """
    Removes recipes with duplicate titles.

    :param df: DataFrame containing the recipes.
    :return: DataFrame with duplicates removed.
    """
    return df.drop_duplicates(subset='title', keep='first')

def remove_recipes_without_tags(df):
    """
    Removes recipes that don't have any tags.

    :param df: DataFrame containing the recipes.
    :return: DataFrame with recipes without tags removed.
    """
    return df[df['tags'].notna() & (df['tags'] != '')]

stop_words = set(stopwords.words('english'))

# Funzione per rimuovere stopwords e aggettivi dalla colonna 'Food commodity ITEM'
def remove_stopwords_and_adjectives(text):
    stop_words = set(stopwords.words('english'))

    tokens = wordpunct_tokenize(text)
    tagged_words = pos_tag(tokens)
    filtered_words = [word.replace('*', '') for word, tag in tagged_words if word.lower() not in stop_words and tag not in ['JJ', 'JJR', 'JJS']]
    return ' '.join(filtered_words)

def clean_ingredients_dataframe(df):
    # Applica la rimozione delle stopwords e degli aggettivi alla colonna 'Food commodity ITEM'
    return df['Food commodity ITEM'].apply(remove_stopwords_and_adjectives)
