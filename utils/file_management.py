# IDEA: methods for saving file names in the format of: topic-date-time
# putting asset in correct folder (eg cheatsheets  - and checking correct format)
# creating subdirs for each new call (dated): eg assets/cheatsheets/TOPIC/file-with-datename.yml

import re
import yaml

from pathlib import Path
from config.lib_config import CHEATSHEET_DIR
from utils.general_utils import make_version

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
    """Save both cheatsheet and voiceover script if available."""
    if isinstance(response_data, dict):
        cheatsheet_content = response_data.get("cheatsheet", "")
        voiceover_content = response_data.get("voiceover", "")

        # Save cheatsheet
        cheatsheet_file = save_cheatsheet(cheatsheet_content, topic)

        # Save voiceover script if available
        if voiceover_content:
            voiceover_file = save_voiceover_script(voiceover_content, topic)
            return cheatsheet_file, voiceover_file
        else:
            return cheatsheet_file, None
    else:
        # Handle string response (backward compatibility)
        cheatsheet_file = save_cheatsheet(response_data, topic)
        return cheatsheet_file, None