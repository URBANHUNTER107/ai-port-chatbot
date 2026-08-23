import json
from pathlib import Path


def load_personal_data():

    data_path = (
        Path(__file__).parent.parent
        / "data"
        / "personal_data.json"
    )

    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)