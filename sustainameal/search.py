from sklearn.metrics.pairwise import cosine_similarity
import torch

def find_similar_by_title(input_text, k, entities_list, embeddings, transformer):
    """
    Finds the most similar entities to the given input.

    Args:
    input_text (str): The input text for which to calculate the embedding.
    k (int): Number of similar entities to find.
    entities_list (list): List of entities against which to calculate similarity.
    embeddings (np.array or torch.Tensor): Matrix of embeddings for the entities.
    transformer (RecipeTransformer): Instance of RecipeTransformer for computing embeddings.

    Returns:
    list: List of the 'k' most similar entities and their similarities.
    """

    # Use RecipeTransformer to compute the embedding of the input text
    input_embedding = transformer.process_batch([input_text])[0]

    # Ensure that the input embedding and the provided embeddings have the same dimension
    assert input_embedding.shape[0] == embeddings.shape[1], "Embedding dimensions do not match."

    # Convert the embeddings to numpy format if necessary
    if isinstance(input_embedding, torch.Tensor):
        input_embedding = input_embedding.cpu().numpy()

    # Convert the embeddings to NumPy array if they are tensors
    if isinstance(embeddings, torch.Tensor):
        embeddings = embeddings.cpu().numpy()

    # Calculate cosine similarity between the input embedding and the provided embeddings
    similarities = cosine_similarity([input_embedding], embeddings)[0]

    # Pair each entity with its similarity and sort by similarity
    similar_entities_with_scores = [(entities_list[i], similarities[i]) for i in range(len(entities_list))]
    similar_entities_with_scores.sort(key=lambda x: x[1], reverse=True)

    # Return the top 'k' most similar entities
    return similar_entities_with_scores[:k]
