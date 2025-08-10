import os
import pytest
import yaml
from unittest.mock import Mock, patch

from pathlib import Path

# Fix import path - use relative import from project root
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.lib_config import CHEATSHEET_DIR

# =========== MOCK ENV ==============
# Mock the Anthropic client for tests
@pytest.fixture(autouse=True)
def mock_anthropic_client():
    """Mock the Anthropic client to avoid API calls during tests."""
    with patch('anthropic.Anthropic') as mock_client:
        mock_client.return_value = Mock()
        yield mock_client

@pytest.fixture(autouse=True)
def mock_env_setup():
    """Mock environment setup to avoid requiring real API keys during tests."""
    # Patch at the module level where it's imported
    with patch('prompt_templates.BasePrompt.setup_anthropic_environment') as mock_setup:
        mock_setup.return_value = True
        yield mock_setup

@pytest.fixture(autouse=True)
def mock_os_env():
    """Mock environment variables for tests."""
    with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
        yield

# =========== MOCK CHEATSHEETS ==============
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
    yield Path("topics/test_topic_file.yml")

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

@pytest.fixture
def test_default_prompt_class():
    """Provide a test-friendly DefaultPrompt class that doesn't initialize API client."""
    from prompt_templates.default_prompt import DefaultPrompt
    from prompt_templates.prompt_config import Role
    
    class TestDefaultPrompt(DefaultPrompt):
        def __init__(self, topic='test'):
            # Skip parent __init__ to avoid API client initialization
            self.role = Role().default
            self.topic = self.validate_topic(topic)
            self.topic_file = self.match_topic_file(self.topic)
            self._initialize_prompt_content()
    
    return TestDefaultPrompt
