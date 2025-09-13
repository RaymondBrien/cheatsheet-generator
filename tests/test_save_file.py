import os
import re
from pathlib import Path

import pytest
import yaml

from cli import (CHEATSHEET_DIR, make_version, save_cheatsheet,
                 save_response_data, save_voiceover_script)
from utils.voiceover import generate_voiceover


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
def sample_voiceover_response() -> str:
    """Fixture to provide a sample voiceover script response."""
    return """Welcome to the Bash cheatsheet! Today we'll cover five essential commands that every developer should know.

First up, the double exclamation mark - !! - repeats your last command. Perfect when you need to run something again with sudo.

Next, 'fg' brings the most recent suspended command to the foreground. Great for managing multiple terminal sessions.

The '&&' operator executes the next command only if the previous one succeeds. Use this for safe command chaining.

The dollar sign '$' stores command output to a variable. Essential for scripting and automation.

Finally, the semicolon ';' chains commands regardless of success. Use this when you want all commands to run.

These commands will make your terminal workflow much more efficient!"""

@pytest.fixture
def sample_response_dict(sample_yaml_cheatsheet_response, sample_voiceover_response) -> dict:
    """Fixture to provide a sample response dictionary with both cheatsheet and voiceover."""
    return {
        "cheatsheet": sample_yaml_cheatsheet_response,
        "voiceover": sample_voiceover_response
    }

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


def test_response_saved_to_file_with_correct_name(cheatsheet_file_factory, sample_yaml_cheatsheet_response):
    """Test that the filename reflects the topic name and includes a timestamp."""
    for sample_response, expected_filepath in cheatsheet_file_factory('bash', sample_yaml_cheatsheet_response):
        # Save the cheatsheet
        save_cheatsheet(sample_response, 'bash')
        
        # Check if the file is saved and in correct location
        assert expected_filepath.exists(), f"File {expected_filepath.name} was not created or saved in wrong location."


def test_saved_file_contains_correct_content(cheatsheet_file_factory, sample_yaml_cheatsheet_response):
    """Test that the saved file contains the correct YAML content."""
    for sample_response, expected_filepath in cheatsheet_file_factory('bash', sample_yaml_cheatsheet_response):
        # Save the cheatsheet
        filepath = save_cheatsheet(sample_response, 'bash')
        
        try:
            # Read and parse the saved file
            with open(filepath, 'r') as file:
                saved_content = yaml.safe_load(file)
            
            # Extract YAML content from the response (remove markdown formatting)
            yaml_match = re.search(r'```yaml\s*(.*?)\s*```', sample_response, re.DOTALL)
            expected_yaml_content = yaml_match.group(1) if yaml_match else sample_response
            expected_content = yaml.safe_load(expected_yaml_content)
            
            # Compare parsed YAML structures
            assert saved_content == expected_content, "YAML content mismatch"
            
        except Exception as e:
            pytest.fail(f"Error reading file {filepath}: {e}")


# New tests for voiceover functionality
def test_save_voiceover_script_creates_file(sample_voiceover_response):
    """Test that voiceover script is saved to a text file."""
    topic = 'bash'
    filepath = save_voiceover_script(sample_voiceover_response, topic)
    
    try:
        # Check if file was created
        assert filepath.exists(), f"Voiceover file {filepath.name} was not created"
        
        # Check file content
        with open(filepath, 'r') as f:
            content = f.read()
            assert sample_voiceover_response in content, "Voiceover content mismatch"
            
    finally:
        # Cleanup
        if filepath.exists():
            os.remove(filepath)
            print(f"Cleaned up voiceover test file: {filepath}")


def test_save_response_data_with_dict_response(sample_response_dict):
    """Test that save_response_data handles dictionary responses correctly."""
    topic = 'bash'
    cheatsheet_file, voiceover_file = save_response_data(sample_response_dict, topic)
    
    try:
        # Check both files were created
        assert cheatsheet_file.exists(), "Cheatsheet file was not created"
        assert voiceover_file.exists(), "Voiceover file was not created"
        
        # Check file types
        assert cheatsheet_file.suffix == '.yml', "Cheatsheet should have .yml extension"
        assert voiceover_file.suffix == '.txt', "Voiceover should have .txt extension"
        
    finally:
        # Cleanup
        if cheatsheet_file.exists():
            os.remove(cheatsheet_file)
        if voiceover_file and voiceover_file.exists():
            os.remove(voiceover_file)
        print("Cleaned up response data test files")


def test_save_response_data_with_string_response(sample_yaml_cheatsheet_response):
    """Test that save_response_data handles string responses (backward compatibility)."""
    topic = 'bash'
    cheatsheet_file, voiceover_file = save_response_data(sample_yaml_cheatsheet_response, topic)
    
    try:
        # Check cheatsheet file was created
        assert cheatsheet_file.exists(), "Cheatsheet file was not created"
        # Check voiceover file was not created
        assert voiceover_file is None, "Voiceover file should not be created for string response"
        
    finally:
        # Cleanup
        if cheatsheet_file.exists():
            os.remove(cheatsheet_file)
        print("Cleaned up string response test file")


def test_voiceover_directory_creation():
    """Test that voiceover directory is created if it doesn't exist."""
    topic = 'test_topic'
    test_content = "Test voiceover content"
    
    # Remove directory if it exists
    voiceover_dir = Path.cwd() / "outputs" / "voiceover_scripts"
    if voiceover_dir.exists():
        import shutil
        shutil.rmtree(voiceover_dir)
    
    # Save voiceover script (should create directory)
    filepath = save_voiceover_script(test_content, topic)
    
    try:
        # Check directory was created
        assert voiceover_dir.exists(), "Voiceover directory was not created"
        assert filepath.exists(), "Voiceover file was not created"
        
    finally:
        # Cleanup
        if filepath.exists():
            os.remove(filepath)
        if voiceover_dir.exists():
            import shutil
            shutil.rmtree(voiceover_dir)
        print("Cleaned up voiceover directory test")