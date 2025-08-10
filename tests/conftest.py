import os
import pytest
import yaml

from pathlib import Path

from cli import CHEATSHEET_DIR, make_version

@pytest.fixture
def sample_yaml_cheatsheet():
    example_cheatsheet = Path("prompt_templates/example_cheatsheet.yml")
    if example_cheatsheet is not None:
        return example_cheatsheet
    else:
        raise FileNotFoundError("Example cheatsheet not found")

def create_yaml_file(data: dict, file_path: Path):
    """
    Create a YAML file from a dictionary.

    :param data: Dictionary to convert to YAML.
    :param file_path: Path where the YAML file will be saved.
    """
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

@pytest.fixture
def dict_to_yaml():
    return create_yaml_file

@pytest.fixture(scope="function")
def sample_topic_file():
    """Fixture to provide a topic file path."""
    yield Path(f"topics/test_topic_file.yml")

@pytest.fixture
def local_generated_cheatsheets():
    """Use outputs dir of real cheatsheets"""
    # TODO
        # return [Path(s) for s in cheatsheet_path:=Abspath(assets.cheatsheets)]
    ...

@pytest.fixture
def sample_yaml_cheatsheet_response() -> str:
    """Fixture to provide a sample YAML cheatsheet response."""
    return """
```yaml
- topic: bash
  date: 2023-10-01
  commands:
    - "!!": repeat last command
    - "fg": bring most recent suspended command to foreground
    - "&&": exectute next command but ONLY if previous succeeds
    - "$": store command output to variable
    - ";": chain commands regardless of success of previous
```
"""

@pytest.fixture
def cheatsheet_file_factory():
    """Factory fixture that creates cheatsheet files for any topic."""
    def _create_cheatsheet_file(topic, sample_response):
        version = make_version()
        expected_filename = f"{topic}_cheatsheet_{version}.yml"
        expected_filepath = CHEATSHEET_DIR / expected_filename

        yield sample_response, expected_filepath

        # Cleanup
        if expected_filepath.exists():
            os.remove(expected_filepath)
            print(f"Cleaned up test file: {expected_filepath}")

    return _create_cheatsheet_file