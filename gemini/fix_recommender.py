from gemini.gemini_config import (
    client,
    MODEL_NAME
)


def recommend_fix(code, problem):

    prompt = f"""
You are an expert software developer.

Problem:
{problem}

Source code:
{code}

Give a safe and practical solution.

Provide:
1. Explanation
2. Recommended change
3. Corrected code when possible
4. Why the fix works
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text