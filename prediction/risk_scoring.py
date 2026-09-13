def calculate_risk(effort):

    if effort >= 10000:
        return "CRITICAL"

    if effort >= 6000:
        return "HIGH"

    if effort >= 3000:
        return "MEDIUM"

    return "LOW"