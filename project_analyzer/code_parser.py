import ast


def parse_python_code(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            source = file.read()

        tree = ast.parse(source)

        return tree, source, None

    except Exception as error:

        return None, "", str(error)