from app.chat import retrieve_crop_information
from app.llm import generate_llm_response


def generate_rag_response(question: str):
    """
    Retrieve relevant crop information and use it
    as context for the language model.
    """

    retrieved = retrieve_crop_information(question)
    print(retrieved)

    if retrieved is None:
        return {
            "response": "I couldn't find relevant information in the knowledge base."
        }

    context = ""

    for doc in retrieved["documents"]:
        context += f"""
    Crop:
    {doc["crop"]}

    Ideal Moisture Range:
    {doc["moistureRange"]}

    Common Problems:
    {doc["commonProblems"]}

    Watering Tips:
    {doc["wateringTips"]}

    --------------------------
    """

    prompt = f"""
You are KrishiMitra, an AI assistant for farmers.

Use ONLY the following crop information to answer the user's question.

Retrieved Knowledge:
{context}

User Question:
{question}

Instructions:
- Answer in simple language.
- Use only the provided information.
- Do not invent facts.
- If the information is insufficient, clearly say so.
"""

    answer = generate_llm_response(prompt)

    return {
        "response": answer,
        "best_crop": retrieved["best_crop"],
        "best_score": retrieved["best_score"],
        "documents": retrieved["documents"]
    }


if __name__ == "__main__":
    result = generate_rag_response("How often should I water onion crops?")
    print(result)