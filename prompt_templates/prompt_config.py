from typing import Dict
from pathlib import Path
from enum import Enum

import yaml

from API_CONFIG import MAX_TOKENS


class Role:
    def __init__(self):
        self.default = """knowledgeable technical assistant and expert in setting up
        developers with the most relevant and future-proof skills"""

        self.role: str = self.default

    def custom_role(self) -> str:
        self.custom = input("Type a custom role here: ")
        return self.role


class Topic:
    def __init__(self):
        self.topic: str ""
        self.topic_file: Dict = self.get_topic_dict(self.topic)  # TODO fill out func above to find topic file by matching text with file name from topics dir
        

    def get_topic_dict(self, filename: str):
        with open(f"{filename}.yml", 'r',) as f:
            output = yaml.safe_load(f)
        print(output)
        return output


class PromptType(Enum):
    """TODO add more, according to anthropic docs"""
    TEXT = "text"
    DOCUMENT = "document"


class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"


class RequestReturnType(Enum):
    MARKDOWN = "markdown"
    TEXT = "text"
    YAML = "yaml"
    CODE = "code"
    FILE = "file"

class TargettedOs(Enum):
    LINUX = "linux"
    WINDOWS = "windows"
    MACOS = "macos"


def validate_token_length(text: str, MAX_TOKENS) -> str:
    if len(text) < MAX_TOKENS:
        return text
    else:
        raise RuntimeError()  # TODO

def match_topic_with_file() -> Path:
    return
