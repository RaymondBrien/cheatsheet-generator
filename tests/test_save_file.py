import pytest
import os
import re
import yaml


from cli import save_cheatsheet


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
            assert saved_content == expected_content, f"YAML content mismatch"
            
        except Exception as e:
            pytest.fail(f"Error reading file {filepath}: {e}")