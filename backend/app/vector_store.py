from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from app.crop_data import CROP_KNOWLEDGE

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


documents = []
crop_ids = []

for crop, data in CROP_KNOWLEDGE.items():

    text = f"""
    Crop: {crop}

    Moisture:
    {data["moistureRange"]}

    Problems:
    {data["commonProblems"]}

    Watering:
    {data["wateringTips"]}
    """

    documents.append(text)
    crop_ids.append(crop)


print(f"Loaded {len(documents)} crop documents.")

embeddings = model.encode(
    documents,
    convert_to_numpy=True
)

embeddings = embeddings.astype(np.float32)

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

index.add(embeddings)

print("FAISS index created.")
print("Documents indexed:", index.ntotal)

def search(query, k=3):
    """
    Search the vector database.
    Returns the indices of the k most similar crop documents.
    """

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype(np.float32)

    distances, indices = index.search(
        query_embedding,
        k
    )

    return distances[0], indices[0]