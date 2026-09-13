import os


LANGUAGE_EXTENSIONS = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".c": "C",
    ".h": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++",
    ".cs": "C#",
    ".php": "PHP"
}


def detect_languages(files):

    languages = {}

    for file_path in files:

        extension = os.path.splitext(
            file_path
        )[1].lower()

        if extension in LANGUAGE_EXTENSIONS:

            language = LANGUAGE_EXTENSIONS[extension]

            languages[language] = (
                languages.get(language, 0) + 1
            )

    return languages