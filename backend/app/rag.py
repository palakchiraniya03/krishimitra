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
    print(retrieved)

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

CURRENT SENSOR DATA (use these values EXACTLY, do NOT invent):
{sensor_block}

SYSTEM RECOMMENDATION (already computed by the backend):
{system_block}

RETRIEVED CROP KNOWLEDGE (use this ONLY as supporting context):
{context}

USER QUESTION:
{question}

RESPONSE FORMAT and RULES:
- The CURRENT SENSOR DATA belongs to the crop specified in the sensor data.
- If the user's question mentions a different crop than the sensor crop, explain that the live sensor readings apply only to the sensor crop, and provide only general guidance for the requested crop from the retrieved knowledge.
- Never claim that the sensor crop is something different from the value provided.
- MUST use BOTH the CURRENT SENSOR DATA and the RETRIEVED CROP KNOWLEDGE.
- NEVER invent or guess sensor values; if a sensor value is missing, say so.
- Begin the Reason section by explaining the backend recommendation reason before expanding with retrieved crop knowledge.
- Do not introduce agricultural facts that are not supported by the retrieved crop knowledge or the provided sensor data.
- If the retrieved knowledge does not contain enough information, say so instead of adding new facts.
The backend has already determined the irrigation recommendation using deterministic rules.

Do NOT override or contradict this recommendation.

Your responsibility is to explain the recommendation clearly using the sensor data and retrieved crop knowledge.

Your job is to:

- Explain the system recommendation in simple language.
- Use the retrieved crop knowledge to support the explanation.
- Mention weather and sensor values only if they support the recommendation.
- Never contradict the System Recommendation.

Always explain why the recommendation was made using the provided recommendation reason and sensor data.
Never invent weather or sensor values.
- Mention Temperature, Humidity, and Pump Status only if they are relevant to the recommendation.
- Keep the answer short and practical.
Provide exactly three short labeled sections:

Recommendation:
- The Recommendation MUST be EXACTLY the same as the System Recommendation.
- Do not change, rewrite, or contradict it.

Reason:
- Explain the Recommendation Reason using the retrieved crop knowledge and relevant sensor values.

Warning:
- Mention any risks or precautions from the retrieved crop knowledge.
- If no warning is applicable, write "None".
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