def calculate_quality_score(
    loc,
    comments,
    functions,
    complexity
):

    if loc <= 0:
        return 0

    comment_ratio = comments / loc

    score = 100

    if complexity > 100:
        score -= 25
    elif complexity > 50:
        score -= 15
    elif complexity > 20:
        score -= 8

    if comment_ratio < 0.05:
        score -= 15
    elif comment_ratio < 0.10:
        score -= 8

    if functions > 500:
        score -= 10

    return max(0, min(100, score))