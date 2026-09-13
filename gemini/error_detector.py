def extract_error_findings(response):

    if not response:
        return []

    sections = response.split(
        "\n"
    )

    findings = []

    for line in sections:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        if any(
            word in lower
            for word in [
                "error",
                "bug",
                "issue",
                "warning",
                "vulnerability"
            ]
        ):

            findings.append(line)

    return findings