# IDEA: methods for saving file names in the format of: topic-date-time
# putting asset in correct folder (eg cheatsheets  - and checking correct format)
# creating subdirs for each new call (dated): eg assets/cheatsheets/TOPIC/file-with-datename.yml

import re
from pathlib import Path
from typing import Any, TypeVar

import yaml

from config.lib_config import CHEATSHEET_DIR
from utils.general_utils import make_version


def get_expected_filename(topic: str, artefact: Any) -> str:
    """
    Generate expected filename for cheatsheet or voiceover script based on topic and current version.
    Args:
        artefact (str): The type of artefact: "cheatsheet" or "voiceover_script".
    Returns:
        str: The expected filename for the cheatsheet or voiceover script.

    """
    if not topic:
        raise ValueError("Topic must be provided to generate filename.")

    topic = validate_topic_name(topic)
    version = make_version()

    if artefact.name == ("cheatsheet" or "cs"):
        suffix = 'yml'
    elif artefact.name == ("voiceover_script" or "v"):
        suffix = 'txt'
    return f"{topic}_{artefact.name}_{version}.{suffix}"



def save_cheatsheet(response: str, topic: str):
    """Save the generated cheatsheet to a YAML file."""
    # Ensure directory exists
    CHEATSHEET_DIR.mkdir(parents=True, exist_ok=True)
    version =  make_version()
    # Create filename with .yml extension
    filename = f"{topic}_cheatsheet_{version}.yml"
    filepath = CHEATSHEET_DIR / filename

    try:
        # Extract YAML content if response contains it
        yaml_match = re.search(r'```yaml\s*(.*?)\s*```', response, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            # Validate YAML
            parsed_yaml = yaml.safe_load(yaml_content)
            # Save formatted YAML
            with open(filepath, 'w') as f:
                yaml.dump(parsed_yaml, f, default_flow_style=False, sort_keys=False)
        else:
            # If no YAML found, save the raw response
            with open(filepath, 'w') as f:
                f.write(response)

        # check file made successfully
        if not filepath.exists():
            raise RuntimeError(f"Failed to create cheatsheet file: {filepath}")
        print(f"✅ Cheatsheet saved successfully: {filepath}")

        return filepath
    except Exception as e:
        raise RuntimeError(f"Failed to save cheatsheet: {e}")


def save_voiceover_script(voiceover_content: str, topic: str):
    """Save the generated voiceover script to a text file."""
    # Ensure directory exists
    VOICEOVER_DIR = Path.cwd() / "outputs" / "voiceover_scripts"
    VOICEOVER_DIR.mkdir(parents=True, exist_ok=True)

    version = make_version()
    filename = f"{topic}_voiceover_{version}.txt"
    filepath = VOICEOVER_DIR / filename

    try:
        with open(filepath, 'w') as f:
            f.write(voiceover_content)

        if not filepath.exists():
            raise RuntimeError(f"Failed to create voiceover file: {filepath}")
        print(f"✅ Voiceover script saved successfully: {filepath}")

        return filepath
    except Exception as e:
        raise RuntimeError(f"Failed to save voiceover script: {e}")


def save_response_data(response_data, topic: str):
    """
    Save both cheatsheet and voiceover script if available.
    Generate a voiceover wav file from the voiceover script if available.
    """
    if isinstance(response_data, dict):
        cheatsheet_content = response_data.get("cheatsheet", "")
        voiceover_content = response_data.get("voiceover", "")

        # Save cheatsheet
        cheatsheet_file = save_cheatsheet(cheatsheet_content, topic)

        # Save voiceover script if available
        if voiceover_content:
            voiceover_file = save_voiceover_script(voiceover_content, topic)
            generate_voiceover(voiceover_file, topic)  # Generate voiceover wav file
            return cheatsheet_file, voiceover_file
        else:
            return cheatsheet_file, None
    else:
        # Handle string response (backward compatibility)
        cheatsheet_file = save_cheatsheet(response_data, topic)
        return cheatsheet_file, None


def sanitise_topic_name(topic: str) -> str:
    """
    Sanitise string name, find a matching topic file,
    and validate the topic key's value matches the topic
    string specified.
    If no topic file exists, return self.topic name as none.
    """
    if not topic or topic.strip() == "":
        raise ValueError("Topic cannot be empty or None.")
    if isinstance(topic, str) and len(topic) < 1:
        raise ValueError("Topic must be at least 1 character long.")

    # check if topic is empty after sanitisation
    if not topic.strip():
        raise ValueError("Topic cannot be empty after sanitisation.")

    topic = str(topic).replace(" ", "_").lower().strip()  # strip after to avoid leading/trailing spaces and catch any empty strings
    return topic