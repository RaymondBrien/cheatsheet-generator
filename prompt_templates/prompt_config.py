from typing import Dict
from pathlib import Path

import yaml

from API_CONFIG import MAX_TOKENS


def validate_token_length(text: str, MAX_TOKENS) -> str:
    if len(text) < MAX_TOKENS:
        return text
    else: 
        raise RuntimeError()  # TODO

def get_topic_dict(filename: str):
    with open(f"{filename}.yml", 'r',) as f:
        output = yaml.safe_load(f)
    print(output)
    return output

def match_topic_with_file() -> Path:
    ...



class Role:
    def __init__(self):
        self.default = """knowledgeable technical assistant and expert in setting up
        developers with the most relevant and future-proof skills"""

        self.custom: str = ""

    def custom_role(self) -> str:
        self.role = input("Type a custom role here: ")
        return self.role


class Topic:
    def __init__(self):
        self.topic: Str = ""
        self.topic_file: Dict = get_topic_dict(self.topic)  # TODO fill out func above to find topic file by matching text with file name from topics dir
        
