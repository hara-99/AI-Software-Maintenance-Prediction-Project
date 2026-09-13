def estimate_technical_debt(
    complexity,
    loc,
    hotspots
):

    debt = (
        complexity * 0.5 +
        loc * 0.01 +
        hotspots * 5
    )

    return round(debt, 2)