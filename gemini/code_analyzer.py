import json
import re

from gemini.gemini_config import client, MODEL_NAME


def clean_json_response(text):

    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def analyze_project_with_gemini(
    source_files,
    project_features,
    languages
):

    source_text = []

    for file_path, content in source_files:

        source_text.append(
            f"\n===== FILE: {file_path} =====\n"
        )

        lines = content.splitlines()

        for number, line in enumerate(
            lines,
            start=1
        ):

            source_text.append(
                f"{number}: {line}\n"
            )

    combined_source = "".join(
        source_text
    )

    # Protect the API request from extremely large projects.
    max_chars = 300000

    if len(combined_source) > max_chars:

        combined_source = (
            combined_source[:max_chars]
            + "\n\n[PROJECT SOURCE TRUNCATED]"
        )

    prompt = f"""
You are an expert software maintenance engineer,
software architect, security reviewer and debugging expert.

Analyze the uploaded software project.

IMPORTANT:
- Do NOT invent files or line numbers.
- Only report issues supported by the supplied source code.
- Give exact file paths.
- Give exact line numbers whenever possible.
- If an issue cannot be confirmed, mark it as "Potential".
- Focus on actionable maintenance problems.
- Analyze multiple programming languages if present.

PROJECT LANGUAGES:
{json.dumps(languages, indent=2)}

AUTOMATIC PROJECT METRICS:
{json.dumps(project_features, indent=2, default=str)}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": {{
        "overall_assessment": "",
        "maintenance_level": "",
        "quality_score": 0,
        "technical_debt_score": 0
    }},

    "errors": [
        {{
            "severity": "Critical|High|Medium|Low",
            "type": "",
            "file": "",
            "line": 0,
            "code": "",
            "problem": "",
            "explanation": "",
            "solution": "",
            "maintenance_action": ""
        }}
    ],

    "security_issues": [
        {{
            "severity": "",
            "file": "",
            "line": 0,
            "problem": "",
            "explanation": "",
            "solution": ""
        }}
    ],

    "code_quality_issues": [
        {{
            "severity": "",
            "file": "",
            "line": 0,
            "problem": "",
            "explanation": "",
            "solution": ""
        }}
    ],

    "maintenance_recommendations": [
        {{
            "priority": "Critical|High|Medium|Low",
            "recommendation": "",
            "reason": "",
            "expected_benefit": ""
        }}
    ],

    "hotspots": [
        {{
            "file": "",
            "reason": "",
            "priority": ""
        }}
    ],

    "change_impact": {{
        "high_impact_areas": [],
        "affected_components": [],
        "recommendation": ""
    }}
}}

SOURCE CODE:

{combined_source}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    response_text = response.text

    cleaned = clean_json_response(
        response_text
    )

    try:

        return json.loads(
            cleaned
        )

    except json.JSONDecodeError:

        return {
            "summary": {
                "overall_assessment":
                    "Gemini returned a non-JSON response.",
                "maintenance_level":
                    "Unknown",
                "quality_score": 0,
                "technical_debt_score": 0
            },

            "errors": [],

            "security_issues": [],

            "code_quality_issues": [],

            "maintenance_recommendations": [],

            "hotspots": [],

            "change_impact": {
                "high_impact_areas": [],
                "affected_components": [],
                "recommendation": ""
            },

            "raw_response": response_text
        }