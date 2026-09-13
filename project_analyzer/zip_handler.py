import os
import zipfile
import shutil
import uuid


def extract_project(zip_path, output_directory):

    # Create a unique extraction folder
    unique_folder = "project_" + str(uuid.uuid4())[:8]

    extraction_path = os.path.join(
        output_directory,
        unique_folder
    )

    os.makedirs(
        extraction_path,
        exist_ok=True
    )

    # Extract ZIP file
    with zipfile.ZipFile(
        zip_path,
        "r"
    ) as zip_ref:

        zip_ref.extractall(
            extraction_path
        )

    # Detect whether ZIP contains one main folder
    items = os.listdir(
        extraction_path
    )

    if len(items) == 1:

        first_item = os.path.join(
            extraction_path,
            items[0]
        )

        if os.path.isdir(
            first_item
        ):

            return first_item

    return extraction_path