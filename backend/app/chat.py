"""
Chat service for KrishiMitra.

Responsibilities:
- Answer crop-related questions.
- Use crop knowledge.
- Integrate ML predictions.
- Future: RAG support.
"""

# TODO:
# Step 1: Create a function to process user questions.
# Step 2: Connect it to FastAPI.
# Step 3: Integrate with frontend chatbot.

import numpy as np
from sentence_transformers import SentenceTransformer

from app.crop_data import CROP_KNOWLEDGE

SEMANTIC_SIMILARITY_THRESHOLD = 0.25
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading semantic embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL_NAME)
print("Semantic embedding model loaded.")

def build_crop_documents():
    documents = []
    crop_ids = []

    for crop_id, data in CROP_KNOWLEDGE.items():
        text = (
            crop_id + " " +
            data["moistureRange"] + " " +
            data["commonProblems"] + " " +
            data["wateringTips"]
        )

        documents.append(text)
        crop_ids.append(crop_id)

    return crop_ids, documents

crop_ids, documents = build_crop_documents()

# The crop knowledge base is small and static, so we precompute embeddings once at import time.
document_vectors = model.encode(
    documents,
    convert_to_numpy=True,
).astype(np.float32)

document_norms = np.linalg.norm(document_vectors, axis=1, keepdims=True)
document_norms[document_norms == 0] = 1.0
document_vectors = document_vectors / document_norms

def retrieve_crop_information(question: str):
    question_vector = model.encode(
        [question],
        convert_to_numpy=True,
    ).astype(np.float32)

    question_norm = np.linalg.norm(question_vector, axis=1, keepdims=True)
    question_norm[question_norm == 0] = 1.0
    question_vector = question_vector / question_norm

    scores = np.dot(question_vector, document_vectors.T)[0]

    top_indices = scores.argsort()[::-1][:3]

    best_index = top_indices[0]
    best_score = float(scores[best_index])

    print("\n===== Top Retrieved Documents =====")

    for idx in top_indices:
        print(
            crop_ids[idx],
            "->",
            round(float(scores[idx]), 4)
        )

    print("===============================\n")

    if best_score < SEMANTIC_SIMILARITY_THRESHOLD:
        return None

    retrieved_docs = []

    for idx in top_indices:
        crop = crop_ids[idx]

        retrieved_docs.append({
            "crop": crop,
            "moistureRange": CROP_KNOWLEDGE[crop]["moistureRange"],
            "commonProblems": CROP_KNOWLEDGE[crop]["commonProblems"],
            "wateringTips": CROP_KNOWLEDGE[crop]["wateringTips"],
            "score": float(scores[idx])
        })

    return {
        "documents": retrieved_docs,
        "best_crop": crop_ids[best_index],
        "best_score": best_score,
        "crop_ids": crop_ids,
        "crop": crop_ids[best_index],
        "score": best_score,
}

def generate_response(question: str):
    result = retrieve_crop_information(question)

    response = (
        f"Based on your question, the most relevant crop is {result['crop']}.\n\n"
        f"Recommended Moisture Range: {result['moistureRange']}\n\n"
        f"Common Problems: {result['commonProblems']}\n\n"
        f"Watering Tips: {result['wateringTips']}"
    )

    return {
        "response": response,
        "crop": result["crop"],
        "score": result["score"]
    }

if __name__ == "__main__":
    result = generate_response(
        "My onion bulbs are rotting."
    )
    print(result)