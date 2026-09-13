import os
import re
import ast
import math


SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".cc",
    ".cxx",
    ".cs",
    ".php"
}


def safe_read_file(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            return file.read()

    except Exception:

        return ""


def count_python_metrics(content):

    functions = 0
    classes = 0
    complexity = 1
    imports = 0

    try:

        tree = ast.parse(
            content
        )

        for node in ast.walk(tree):

            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef
                )
            ):

                functions += 1

            elif isinstance(
                node,
                ast.ClassDef
            ):

                classes += 1

            elif isinstance(
                node,
                (
                    ast.If,
                    ast.For,
                    ast.While,
                    ast.Try,
                    ast.With,
                    ast.BoolOp,
                    ast.IfExp
                )
            ):

                complexity += 1

            elif isinstance(
                node,
                (
                    ast.Import,
                    ast.ImportFrom
                )
            ):

                imports += 1

    except Exception:

        functions = len(
            re.findall(
                r"\bdef\s+\w+",
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
                r"^\s*(import|from)\s+",
                content,
                re.MULTILINE
            )
        )

    return (
        functions,
        classes,
        complexity,
        imports
    )


def calculate_file_metrics(
    path
):

    content = safe_read_file(
        path
    )

    if not content:

        return {
            "file": path,
            "loc": 0,
            "functions": 0,
            "classes": 0,
            "complexity": 0,
            "imports": 0,
            "comments": 0
        }

    extension = os.path.splitext(
        path
    )[1].lower()

    lines = content.splitlines()

    loc = sum(
        1
        for line in lines
        if line.strip()
    )

    comments = sum(
        1
        for line in lines
        if (
            line.strip().startswith("#")
            or line.strip().startswith("//")
            or line.strip().startswith("/*")
            or line.strip().startswith("*")
        )
    )

    if extension == ".py":

        functions, classes, complexity, imports = (
            count_python_metrics(
                content
            )
        )

    else:

        functions = len(
            re.findall(
                r"\b(?:def|function|func)\s+\w+|"
                r"\b\w+\s+\w+\s*\([^;{}]*\)\s*\{",
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
                r"^\s*(import|from|using|require|include)\b",
                content,
                re.MULTILINE
            )
        )

        complexity = (
            1
            + len(
                re.findall(
                    r"\b(if|else|for|while|catch|case|switch)\b",
                    content
                )
            )
        )

    return {
        "file": path,
        "loc": loc,
        "functions": functions,
        "classes": classes,
        "complexity": complexity,
        "imports": imports,
        "comments": comments
    }


def normalize(
    value,
    minimum,
    maximum
):

    if maximum <= minimum:

        return 0.0

    result = (
        (value - minimum)
        / (maximum - minimum)
    )

    return max(
        0.0,
        min(
            1.0,
            result
        )
    )


def create_dataset_features(
    total_loc,
    total_files,
    total_functions,
    total_classes,
    total_complexity,
    total_imports,
    total_comments,
    languages_count
):

    # Automatic project-to-dataset feature mapping.
    #
    # These are automatically derived proxies because
    # the uploaded source project does not directly contain
    # the original dataset's measurement fields.

    n_effort = max(
        0.01,
        math.log1p(total_loc)
        / 10.0
    )

    enquiry = (
        total_functions
        + total_classes
        + total_imports
    ) / max(
        total_files,
        1
    )

    interface = (
        total_classes
        + languages_count
    ) / max(
        total_files,
        1
    )

    file_feature = float(
        total_files
    )

    input_feature = (
        total_imports
        + total_functions
    ) / max(
        total_loc,
        1
    )

    afp = (
        total_loc
        + total_functions * 5
        + total_classes * 10
    ) / 100.0

    added = (
        total_loc
        * (
            1
            + normalize(
                total_complexity,
                1,
                max(total_loc, 2)
            )
        )
    ) / 100.0

    duration = max(
        0.01,
        (
            total_loc / 500.0
            + total_complexity / 100.0
        )
    )

    pdr_afp = (
        total_complexity
        + total_functions
    ) / max(
        afp,
        0.01
    )

    output = (
        total_comments
        + total_functions
        + total_classes
    ) / max(
        total_files,
        1
    )

    return {
        "N_effort": float(n_effort),
        "Enquiry": float(enquiry),
        "Interface": float(interface),
        "File": float(file_feature),
        "Input": float(input_feature),
        "AFP": float(afp),
        "Added": float(added),
        "Duration": float(duration),
        "PDR_AFP": float(pdr_afp),
        "Output": float(output)
    }


def extract_project_features(
    files
):

    file_metrics = []

    for file_path in files:

        extension = os.path.splitext(
            file_path
        )[1].lower()

        if extension not in SUPPORTED_EXTENSIONS:
            continue

        metrics = calculate_file_metrics(
            file_path
        )

        file_metrics.append(
            metrics
        )

    total_files = len(
        file_metrics
    )

    total_loc = sum(
        item["loc"]
        for item in file_metrics
    )

    total_functions = sum(
        item["functions"]
        for item in file_metrics
    )

    total_classes = sum(
        item["classes"]
        for item in file_metrics
    )

    total_complexity = sum(
        item["complexity"]
        for item in file_metrics
    )

    total_imports = sum(
        item["imports"]
        for item in file_metrics
    )

    total_comments = sum(
        item["comments"]
        for item in file_metrics
    )

    extensions = set()

    for path in files:

        extension = os.path.splitext(
            path
        )[1].lower()

        if extension in SUPPORTED_EXTENSIONS:

            extensions.add(
                extension
            )

    dataset_features = create_dataset_features(
        total_loc=total_loc,
        total_files=total_files,
        total_functions=total_functions,
        total_classes=total_classes,
        total_complexity=total_complexity,
        total_imports=total_imports,
        total_comments=total_comments,
        languages_count=len(extensions)
    )

    return {
        "total_files": total_files,
        "total_loc": total_loc,
        "total_functions": total_functions,
        "total_classes": total_classes,
        "total_complexity": total_complexity,
        "total_imports": total_imports,
        "total_comments": total_comments,
        "languages_count": len(extensions),
        "dataset_features": dataset_features,
        "file_metrics": file_metrics
    }