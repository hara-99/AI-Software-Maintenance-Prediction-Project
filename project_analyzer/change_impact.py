def calculate_change_impact(
    added_lines=0,
    changed_lines=0,
    deleted_lines=0
):

    total = (
        added_lines +
        changed_lines +
        deleted_lines
    )

    if total == 0:
        return {
            "added": 0,
            "changed": 0,
            "deleted": 0,
            "impact_score": 0
        }

    impact_score = (
        added_lines * 1.0 +
        changed_lines * 1.5 +
        deleted_lines * 1.2
    )

    return {
        "added": added_lines,
        "changed": changed_lines,
        "deleted": deleted_lines,
        "impact_score": impact_score
    }