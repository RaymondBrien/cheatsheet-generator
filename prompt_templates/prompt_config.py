from typing import Dict, Str
import yaml

from API_CONFIG import MAX_TOKENS

class Role:
    def __init__(self):
        self.default = """knowledgeable technical assistant and expert in setting up 
        developers with the most relevant and future-proof skills"""

        self.custom: Str = ""

    def custom_role(self) -> Str:
        input("Type a custom role here: ")


def validate_token_length(text: Str, MAX_TOKENS) -> None:
    if len(text) < MAX_TOKENS:
        return text
    else: 
        raise RuntimeError()  # TODO


if
def get_topic_dict(filename: Str):
    with open(f"{filename}.yml", 'r',) as f:
        output = yaml.safe_load(f)
    print(output)
    return output

def match_topic_with_file() -> Path:
    ...


class Topic:
    def __init__(self):
        self.topic: Str = ""
        self.topic_file: Dict = get_topic_dict(self.topic)  # TODO fill out func above to find topic file by matching text with file name from topics dir
        
