import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
from typing import Union, Dict, List

import anthropic

import prompt_templates.prompt_config as prompt_config
from .prompt_config import PromptType, RequestReturnType, TargettedOs
from utils.env_loader import setup_anthropic_environment


class Prompt:
    def __init__(self):
        # Initialize the Anthropic client and prompt configuration
        role = prompt_config.Role()
        self.client: anthropic.Anthropic = self.client_init()

        # POST request parameters
        # self.model: str = "claude-2"  # TODO make this dynamic
        self.prompt_type = PromptType.TEXT
        self.message_role = prompt_config.MessageRole.USER

        # Prompt instance text content
        self.role: str = ""
        self.targetted_os: TargettedOs = None
        self.request_return_type: RequestReturnType = None
        self.example_cheatsheet: Path = Path()
        self.topic_file: Path = Path()
        self.topic: str = ""
        self.subtopic: List[str] = ""
        self.topic_docs: Union[str, List[str]] = ""
        self.request_return_type: str = ""
        self.max_tokens: int = 0
        self.temperature: float = 0.0

        # Prompt instance configuration of main text bodies
        self.output_goal: str = ""
        self.additional_reqs: str = ""
        self.format_instructions: str = ""
        self.main_text: str = ""

    def client_init(self, *args):
        """
        Initialize the Anthropic client with robust environment loading.
        """
        # Ensure environment variables are loaded
        try:
            if not setup_anthropic_environment():
                raise RuntimeError("Failed to setup Anthropic environment variables")
        except ImportError:
            # Fallback if env_loader is not available
            if not os.getenv("ANTHROPIC_API_KEY"):
                raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
        
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
