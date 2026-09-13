import os
import re


def analyze_file(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            content = file.read()

    except Exception:

        return None

    lines = content.splitlines()

    code_lines = [
        line for line in lines
        if line.strip()
    ]

    comment_lines = [
        line for line in lines
        if line.strip().startswith(
            ("#", "//", "/*", "*")
        )
    ]

    functions = len(
        re.findall(
            r"\b(def|function|func)\s+\w+",
            content
        )
    )

    classes = len(
        re.findall(
            r"\bclass\s+\w+",
            content
        )
    )

    imports = len(
        re.findall(
            r"^\s*(import|from|using|include|require)",
            content,
            re.MULTILINE
        )
    )

    return {
        "file": file_path,
        "loc": len(lines),
        "code_lines": len(code_lines),
        "comment_lines": len(comment_lines),
        "functions": functions,
        "classes": classes,
        "imports": imports
    }