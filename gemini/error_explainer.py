from gemini.gemini_config import (
    client,
    MODEL_NAME
)


def explain_error(error_text):

    prompt = f"""
Explain this software problem in simple language.

Problem:
{error_text}

Explain:
1. What is wrong?
2. Why does it happen?
3. What can happen if it is not fixed?
4. How should a developer fix it?
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text