import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
from typing import Union, List, Optional

import anthropic

import prompt_templates.prompt_config as prompt_config
from .prompt_config import PromptType, RequestReturnType, TargettedOs
from utils.env_loader import setup_anthropic_environment
from utils.parse_yaml import read_yaml_key, render_yaml_file

TOPIC_DIR: Path = Path("topics")  # Directory where topic files are stored


class Prompt:
    def __init__(self):
        # Initialize the Anthropic client and prompt configuration
        role: prompt_config.Role = prompt_config.Role()
        self.client: anthropic.Anthropic = self.client_init()

        # POST request parameters
        # self.model: str = "claude-2"  # TODO make this dynamic
        self.prompt_type = PromptType.TEXT
        self.message_role = prompt_config.MessageRole.USER

        # Prompt instance text content
        self.role: str = ""
        self.targetted_os: TargettedOs = None
        self.request_return_type: RequestReturnType = None
        self.example_cheatsheet: Path = None
        self.topic: str = ""
        self.subtopic: List[str] = ""
        self.topic_file: Union[Path, None] = None
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

    def validate_topic(self, topic: str) -> str:
        """Sanitise string name, find a matching topic file, and validate the topic key's value matches the topic string specified. If no topic file exists, return self.topic name as none."""
        if not topic or topic.strip() == "":
            raise ValueError("Topic cannot be empty or None.")
        if isinstance(topic, str) and len(topic) < 1:
            raise ValueError("Topic must be at least 1 character long.")

        topic = self.sanitise_topic_name(topic)
        if not self.match_topic_file(topic):
            self.topic_file = None
        return topic

    def sanitise_topic_name(self, topic: str) -> str:
        """Sanitise topic name by replacing spaces with underscores and converting to lowercase."""
        topic = str(topic).replace(" ", "_").lower().strip()  # strip after to avoid leading/trailing spaces and catch any empty strings
        # check topic contains chars

        # check if topic is empty after sanitisation
        if not topic:
            raise ValueError("Topic cannot be empty after sanitisation.")
        print(f"Sanitised topic name: {topic}")
        return topic


    def validate_topic_file(self, topic: str, topic_file: Path) -> Path:
        """Validate that the topic file exists and matches the topic."""

        if topic == str(read_yaml_key(topic_file, "Topic")):
            print(f"✅ Topic file '{topic_file}' matches topic '{topic}'")
            return topic_file
        else:
            raise ValueError(f"topic does not match file: {render_yaml_file(topic_file)}")

    def match_topic_file(self, topic: str) -> Optional[Path]:
        topic_path = Path(TOPIC_DIR / f"{topic}.yml")
        if not topic_path.exists():
            self.topic_file = None
        else:
            return self.validate_topic_file(topic, topic_path)


    def update_role(self, new_role: str):
        """Update the role of the prompt."""
        if not new_role:
            raise ValueError("Role cannot be empty or None.")
        self.role = new_role


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
