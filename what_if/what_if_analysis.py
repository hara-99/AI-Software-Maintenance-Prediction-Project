from prediction.effort_prediction import predict_effort


def what_if_analysis(
    features,
    changes
):

    original = predict_effort(
        features
    )

    modified = features.copy()

    for key, value in changes.items():

        if key in modified:
            modified[key] = value

    new_prediction = predict_effort(
        modified
    )

    return {
        "original_effort": original,
        "new_effort": new_prediction,
        "difference": new_prediction - original
    }