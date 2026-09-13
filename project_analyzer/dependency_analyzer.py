import os
import re


def analyze_dependencies(project_path):

    dependencies = []

    dependency_files = {
        "requirements.txt",
        "package.json",
        "pom.xml",
        "build.gradle"
    }

    for root, _, files in os.walk(project_path):

        for filename in files:

            if filename in dependency_files:

                dependencies.append(
                    os.path.join(root, filename)
                )

    return dependencies