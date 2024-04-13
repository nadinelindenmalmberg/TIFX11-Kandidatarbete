import os
import json
from django.conf import settings

def calculate_from_json(filename):
    json_files_dir = os.path.join(os.path.dirname(__file__), '..', 'json_files')
    file_path = os.path.join(json_files_dir, filename)

    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r') as file:
        data = json.load(file)
        # Perform your calculations here
        # For instance, count the number of items in the "images" list
        result = len(data["images"])
        return result