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

    # Build a concise context block from retrieved documents. The LLM must ONLY use
    # this text as its knowledge source.
    context_parts = []
    for doc in retrieved["documents"]:
        part = (
            f"Crop: {doc.get('crop','')}\n"
            f"Ideal Moisture Range: {doc.get('moistureRange','')}\n"
            f"Common Problems: {doc.get('commonProblems','')}\n"
            f"Watering Tips: {doc.get('wateringTips','')}\n"
        )
        context_parts.append(part)

    context = "\n----\n".join(context_parts)

    # Improved, safety-focused prompt. It instructs the LLM to behave as an
    # agricultural expert, to rely ONLY on the retrieved context, to avoid
    # hallucinations, and to reply in three short labeled sections.
    prompt = f"""
You are KrishiMitra, an agricultural expert assistant for farmers.

CONTEXT (use ONLY this information):
{context}

USER QUESTION:
{question}

RESPONSE FORMAT and RULES:
- Use ONLY the CONTEXT above. If the context does not contain enough information to answer, say so clearly and do NOT guess.
- Never hallucinate or introduce facts not present in the CONTEXT.
- Keep the answer short and practical.
- Provide exactly three short labeled sections: Recommendation, Reason, Warning.
  * Recommendation: concise, actionable advice.
  * Reason: one-sentence explanation citing the CONTEXT.
  * Warning: short note about risks or uncertainty (can be "None" if not applicable).
- Do not include extra commentary, filler, or internal chain-of-thought.

Answer now following the rules above.
"""

    answer = generate_llm_response(prompt)

    # Safety: if LLM returned nothing or an empty response, provide a fallback.
    if not answer or (isinstance(answer, str) and not answer.strip()):
        answer = "I couldn't generate a reliable answer."

    return {
        "response": answer,
        "best_crop": retrieved.get("best_crop"),
        "best_score": retrieved.get("best_score"),
        "documents": retrieved.get("documents")
    }


if __name__ == "__main__":
    result = generate_rag_response("How often should I water onion crops?")
    print(result)