import os


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "dist",
    "build"
}


def scan_files(project_path):

    files = []

    for root, directories, filenames in os.walk(project_path):

        directories[:] = [
            d for d in directories
            if d not in IGNORED_DIRECTORIES
        ]

        for filename in filenames:

            file_path = os.path.join(
                root,
                filename
            )

            files.append(file_path)

    return files