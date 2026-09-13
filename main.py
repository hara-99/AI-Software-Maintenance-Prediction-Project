import subprocess
import sys


def main():

    print(
        "Starting AI Software Maintenance Dashboard..."
    )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "dashboard/app.py"
        ]
    )


if __name__ == "__main__":
    main()