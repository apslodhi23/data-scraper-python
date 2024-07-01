import json
import os
import requests
from typing import List

def save_to_json(data: List[dict], filename: str) -> None:
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_from_json(filename: str) -> List[dict]:
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def download_image(url: str, folder: str) -> str:
    image_name = url.split("/")[-1]
    image_path = os.path.join(folder, image_name)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(image_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    return image_path
