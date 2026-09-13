def detect_hotspots(metrics):

    hotspots = []

    for item in metrics:

        score = (
            item.get("loc", 0) * 0.2 +
            item.get("functions", 0) * 2 +
            item.get("classes", 0) * 3
        )

        hotspots.append({
            "file": item["file"],
            "hotspot_score": score
        })

    hotspots.sort(
        key=lambda x: x["hotspot_score"],
        reverse=True
    )

    return hotspots