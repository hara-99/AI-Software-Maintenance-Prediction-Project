import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)

REPORT_DIR = os.path.join(
    BASE_DIR,
    "generated_reports"
)