import time

from gemini.gemini_config import client, MODEL_NAME


def generate_maintenance_recommendations(
    project_summary,
    detected_errors=None,
    hotspots=None,
    risk_level=None
):
    """
    Generate software maintenance recommendations using Gemini.

    If Gemini is temporarily unavailable, the dashboard will
    continue working and return fallback recommendations.
    """

    if detected_errors is None:
        detected_errors = []

    if hotspots is None:
        hotspots = []

    prompt = f"""
You are an expert software maintenance engineer.

Analyze the following software project information and provide
practical maintenance recommendations.

PROJECT SUMMARY:
{project_summary}

RISK LEVEL:
{risk_level}

DETECTED ERRORS:
{detected_errors}

MAINTENANCE HOTSPOTS:
{hotspots}

Return recommendations covering:

1. Critical maintenance actions
2. Bug fixing priorities
3. Code quality improvements
4. Security improvements
5. Performance improvements
6. Technical debt reduction
7. Testing recommendations
8. Long-term maintenance recommendations

Keep the recommendations practical and specific to the project.
"""


    # ---------------------------------------------------------
    # GEMINI RETRY
    # ---------------------------------------------------------

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if response is None:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            text = getattr(
                response,
                "text",
                None
            )

            if text and text.strip():

                return text.strip()

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        except Exception as error:

            error_text = str(error)

            # Temporary Google server problems
            temporary_error = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
                or "temporarily unavailable" in error_text.lower()
                or "429" in error_text
            )

            if temporary_error:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    time.sleep(
                        wait_time
                    )

                    continue

                # Gemini is unavailable after retries.
                return get_fallback_recommendations(
                    risk_level=risk_level,
                    detected_errors=detected_errors,
                    hotspots=hotspots
                )

            # Other Gemini/API errors
            return get_fallback_recommendations(
                risk_level=risk_level,
                detected_errors=detected_errors,
                hotspots=hotspots
            )


def get_fallback_recommendations(
    risk_level=None,
    detected_errors=None,
    hotspots=None
):
    """
    Local recommendations used when Gemini is unavailable.
    """

    if detected_errors is None:
        detected_errors = []

    if hotspots is None:
        hotspots = []

    recommendations = []

    # ---------------------------------------------------------
    # RISK BASED RECOMMENDATION
    # ---------------------------------------------------------

    if risk_level:

        level = str(
            risk_level
        ).upper()

    else:

        level = "MEDIUM"

    if level == "CRITICAL":

        recommendations.append(
            "Immediately address critical defects and "
            "security vulnerabilities before further deployment."
        )

    elif level == "HIGH":

        recommendations.append(
            "Prioritize high-risk modules and resolve "
            "critical defects before major changes."
        )

    elif level == "MEDIUM":

        recommendations.append(
            "Prioritize modules with high complexity and "
            "increase automated testing coverage."
        )

    else:

        recommendations.append(
            "Continue regular maintenance and monitor "
            "code quality for future degradation."
        )

    # ---------------------------------------------------------
    # ERROR BASED RECOMMENDATIONS
    # ---------------------------------------------------------

    if detected_errors:

        recommendations.append(
            "Review the detected code issues and resolve "
            "high-severity problems before lower-priority refactoring."
        )

        recommendations.append(
            "Add regression tests for corrected defects "
            "to prevent the same problems from returning."
        )

    else:

        recommendations.append(
            "Perform regular static analysis and automated "
            "testing to identify future defects."
        )

    # ---------------------------------------------------------
    # HOTSPOT BASED RECOMMENDATIONS
    # ---------------------------------------------------------

    if hotspots:

        recommendations.append(
            "Prioritize maintenance of the identified "
            "code hotspots because they have elevated "
            "maintenance complexity."
        )

    # ---------------------------------------------------------
    # GENERAL RECOMMENDATIONS
    # ---------------------------------------------------------

    recommendations.extend([
        "Improve unit and integration test coverage.",
        "Reduce unnecessary code complexity.",
        "Document important modules, functions, and dependencies.",
        "Review dependencies regularly for outdated or vulnerable packages.",
        "Use version control and code review for maintenance changes.",
        "Monitor technical debt and refactor high-risk modules gradually."
    ])

    return "\n".join(
        "• " + item
        for item in recommendations
    )