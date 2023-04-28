import json
import os
from fastapi import HTTPException, status


def write_json_file(file_name, file_path, content):
    # Create the full path to the file
    full_path = os.path.join(file_path, file_name)

    # Check if the file already exists and has the same content
    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            current_content = json.load(f)
            if current_content == content:
                print(f"Content of file {file_name} is already up-to-date.")
                return

    # Write the new content to the file
    with open(full_path, 'w') as f:
        json.dump(content, f)

    return full_path

def read_json_file(file_name, file_path):
    try:
        # Load the content of the file
        with open(os.path.join(file_path, file_name), 'r') as f:
            content = json.load(f)
        return content
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File {file_name} not found.")
        return None
