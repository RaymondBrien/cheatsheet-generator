import pytest
import yaml

from pathlib import Path

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