import ast


def python_complexity(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            source = file.read()

        tree = ast.parse(source)

        complexity = 1

        for node in ast.walk(tree):

            if isinstance(
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

        return complexity

    except Exception:

        return 0