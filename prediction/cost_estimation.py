def estimate_cost(effort, hourly_rate=600):

    return round(
        effort * hourly_rate,
        2
    )