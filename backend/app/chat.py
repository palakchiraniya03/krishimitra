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

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.crop_data import CROP_KNOWLEDGE

def build_crop_documents():
    documents = []
    crop_ids = []

    for crop_id, data in CROP_KNOWLEDGE.items():
        text = (
            data["moistureRange"] + " " +
            data["commonProblems"] + " " +
            data["wateringTips"]
        )

        documents.append(text)
        crop_ids.append(crop_id)

    return crop_ids, documents

crop_ids, documents = build_crop_documents()

vectorizer = TfidfVectorizer()
document_vectors = vectorizer.fit_transform(documents)

def retrieve_crop_information(question: str):
    question_vector = vectorizer.transform([question])

    similarities = cosine_similarity(question_vector, document_vectors)

    best_index = similarities.argmax(axis=1)[0]

    return {
    "crop": crop_ids[best_index],
    "moistureRange": CROP_KNOWLEDGE[crop_ids[best_index]]["moistureRange"],
    "commonProblems": CROP_KNOWLEDGE[crop_ids[best_index]]["commonProblems"],
    "wateringTips": CROP_KNOWLEDGE[crop_ids[best_index]]["wateringTips"],
    "score": float(similarities[0][best_index])
}

if __name__ == "__main__":
  result = retrieve_crop_information(
       "My onion bulbs are rotting."
  )
  print(result)