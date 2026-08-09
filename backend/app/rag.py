from app.chat import retrieve_crop_information
from app.llm import generate_llm_response
from app.recommendation import get_irrigation_recommendation


def generate_rag_response(
    question: str,
    crop: str,
    moisture: float,
    temperature: float,
    humidity: float,
    pump_status: str,
    threshold: float,
    is_raining: bool,
    forecast_rain_probability: float,
):
    """
    Retrieve relevant crop information and use it
    as context for the language model.
    """
    retrieved = retrieve_crop_information(
        f"{crop} {question}"
    )

    if retrieved is None:
        return {
            "response": "I couldn't find relevant information in the knowledge base."
        }
    # Build a concise context block from retrieved documents. The LLM must ONLY use
    # this text as its knowledge source. Also build a sensor data block that the
    # model must use and must not invent values for.
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

    recommendation, recommendation_reason = get_irrigation_recommendation(
        moisture=moisture,
        threshold=threshold,
        is_raining=is_raining,
        forecast_rain_probability=forecast_rain_probability,
    )
    sensor_block = (
        f"Crop: {crop}\n"
        f"Current Moisture: {moisture}%\n"
        f"Recommended Threshold: {threshold}%\n"
        f"Temperature: {temperature}°C\n"
        f"Humidity: {humidity}%\n"
        f"Pump Status: {pump_status}\n"
        f"Currently Raining: {'Yes' if is_raining else 'No'}\n"
        f"Forecast Rain Probability: {forecast_rain_probability:.0%}\n"
    )

    system_block = (
        f"Recommendation: {recommendation}\n"
        f"Reason: {recommendation_reason}\n"
    )

    prompt = f"""
You are KrishiMitra, an agricultural expert assistant for farmers.

Follow this priority order:
1. The backend SYSTEM RECOMMENDATION is authoritative and must never be overridden or contradicted.
2. CURRENT SENSOR DATA is factual live data and must be used exactly as provided.
3. RETRIEVED CROP KNOWLEDGE is supporting context only and must not be treated as a source for facts that are not present in it.

CURRENT SENSOR DATA (use these values EXACTLY, do NOT invent):
{sensor_block}

SYSTEM RECOMMENDATION (already computed by the backend):
{system_block}

RETRIEVED CROP KNOWLEDGE (use this ONLY as supporting context):
{context}

USER QUESTION:
{question}

Rules:
- Never invent sensor, weather, or agricultural facts.
- Never change, soften, or contradict the backend recommendation.
- Use the system recommendation as final and explain it with the provided reason, relevant sensor/weather values, and retrieved crop knowledge.
- If the user's question mentions a different crop than the sensor crop, say the live sensor readings apply to the sensor crop and give only general guidance for the requested crop.
- If the retrieved crop knowledge is insufficient, say the available knowledge base does not contain enough information rather than guessing.
- Treat Forecast Rain Probability as a normalized value from 0.0 to 1.0, where 0.10 means 10%.
- Keep the answer concise and practical.

Output exactly three sections:

Recommendation:
- Reproduce the backend recommendation exactly.

Reason:
- Explain why the backend made that recommendation using the supplied recommendation reason, relevant sensor/weather values, and retrieved crop knowledge.

Warning:
- Mention relevant risks or precautions supported by the retrieved crop knowledge.
- If none applies, output exactly "None".

Answer now.
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
    # Example invocation for local testing with sample sensor values
    result = generate_rag_response(
        question="Should I irrigate now?",
        crop="wheat",
        moisture=28.0,
        temperature=32.0,
        humidity=45.0,
        pump_status="OFF",
        threshold=40.0,
        is_raining=False,
        forecast_rain_probability=0.20,
    )
    print(result)