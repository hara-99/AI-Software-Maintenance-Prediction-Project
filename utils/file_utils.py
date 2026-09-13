import os


def ensure_directory(path):

    os.makedirs(
        path,
        exist_ok=True
    )

    return path


def get_file_extension(path):

    return os.path.splitext(
        path
    )[1].lower()