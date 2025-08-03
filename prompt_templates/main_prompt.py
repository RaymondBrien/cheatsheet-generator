import sys
from enum import Enum
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
from typing import Union, Dict, List

import anthropic

import prompt_templates.prompt_config as prompt_config
from prompt_config import PromptType, RequestReturnType


class Prompt:
    def __init__(self):
        # Initialize the Anthropic client and prompt configuration
        role = prompt_config.Role()
        self.client: anthropic.Anthropic = self.client_init()

        # POST request parameters
        # self.model: str = "claude-2"  # TODO make this dynamic
        self.prompt_type: Enum = PromptType.TEXT

        # Prompt instance text content
        self.role: str = ""
        self.targetted_os: Union[str, List[str]] = ""
        self.example_cheatsheet: Path = Path()
        self.topic: Union[str, Dict[str, str]] = ""
        self.subtopic: Union[str, List[str]] = ""
        self.docs_links: Union[str, List[str]] = ""
        self.request_return_type: Enum = RequestReturnType.TEXT

        # Prompt instance configuration of main text bodies
        self.output_goal: str = ""
        self.additional_reqs: str = ""
        self.format_instructions: str = ""
        self.main_text: str = ""

    def client_init(self, *args):
        """
        Initialize the Anthropic client.
        """
        return anthropic.Anthropic(*args) if args else anthropic.Anthropic()

    def upload_file_to_anthropic(
        self,
        type: PromptType = PromptType.DOCUMENT,  # default
        path: str = ""):
        """
        Upload a file to the Anthropic client.
        """
        # Initialize the Anthropic client
        self.client.beta.files.upload(
            file=(str(type), open(path, "rb")),
        )

    def main_text_only(self):
        return self.main_text

    def request_markdown(self):
        """Request Claude to return markdown formatted text."""
        self.prompt_type = PromptType.TEXT


def quick_prompt_check():
    warning = input(
        "This is a test prompt. Do you want to continue? (y/n): "
    )
    if warning.lower() != 'y':
        print("Test prompt aborted.")
        return
    print("Running test prompt...")

    # for quick testing
    p = Prompt()
    p = p.default()
    print(p.ljust(10, "|"))
    print(type(p))
    print(len(p))
    print("main text only is:", p.main_text)
