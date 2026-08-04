def get_irrigation_recommendation(
    moisture: float,
    threshold: float,
    is_raining: bool,
    forecast_rain_probability: float,
) -> tuple[str, str]:
    
    """
    Determine the irrigation recommendation using deterministic rules.

    Returns:
        tuple[str, str]:
            recommendation (str): Action to perform.
            reason (str): Explanation for the recommendation.

    This module intentionally avoids using the LLM for decision-making.
    The language model only explains the recommendation.
    """

    # Rule 1:
    # Never irrigate while it is raining.
    if is_raining:
        return (
            "Delay irrigation",
            "It is currently raining."
        )

    # Rule 2:
    # Delay irrigation if rain is highly likely.
    if forecast_rain_probability >= 0.7:
        return (
            "Delay irrigation",
            "Rain is expected soon."
        )

    # Rule 3:
    # Irrigate when moisture is below the threshold.
    if moisture < threshold:
        return (
            "Irrigate now",
            "Current moisture is below the recommended threshold."
        )

    # Rule 4:
    # Moisture is already sufficient.
    return (
        "Do not irrigate",
        "Current moisture is already sufficient."
    )

    

