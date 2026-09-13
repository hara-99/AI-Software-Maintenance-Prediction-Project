def estimate_uncertainty(
    prediction,
    percentage=0.15
):

    margin = abs(prediction) * percentage

    return {
        "prediction": prediction,
        "lower": max(0, prediction - margin),
        "upper": prediction + margin
    }