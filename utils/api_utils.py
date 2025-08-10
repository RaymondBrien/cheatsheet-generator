"""
save json response into a yaml file
move that into outputs/cheatsheets
git commit that with a unique id: response-cheatsheet-topicid-date-time
explore how to make async - create folder ready, generate file name ready, commit message ready - httpio?
"""

import yaml
import logging
import subprocess
from typing import Optional, Union, Dict, Any
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path('outputs/cheatsheets')


def save_response_to_yaml(
    response: Union[str, Dict, Any], 
    topic: str, 
    output_dir: Optional[Path] = None
) -> tuple[bool, Optional[Path]]:
    """
    Save the API response to a YAML file in the specified output directory.
    
    :param response: The API response to save (string, dict, or any YAML-serializable object)
    :param topic: The topic for which the response was generated
    :param output_dir: The directory where the YAML file will be saved (defaults to OUTPUT_DIR)
    :return: Tuple of (success: bool, file_path: Optional[Path])
    """
    try:
        # Validate inputs
        if not response:
            logger.error("Response cannot be empty")
            return False, None
            
        if not topic or not isinstance(topic, str):
            logger.error(f"Invalid topic: {topic}")
            return False, None
            
        # Use default output_dir if not provided
        output_dir = output_dir or OUTPUT_DIR
        
        # Construct file path
        file_path = construct_output_file_path(topic, output_dir)
        
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the file
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(response, file, default_flow_style=False, allow_unicode=True)
            
        logger.info(f"Successfully saved response to: {file_path}")
        return True, file_path
        
    except (OSError, IOError) as e:
        logger.error(f"File system error saving response: {e}")
        return False, None
    except yaml.YAMLError as e:
        logger.error(f"YAML serialization error: {e}")
        return False, None
    except Exception as e:
        logger.error(f"Unexpected error saving response: {e}")
        return False, None


def construct_output_file_path(topic: str, output_dir: Path = OUTPUT_DIR) -> Path:
    """
    Construct the output file path for the YAML file based on the topic.
    
    :param topic: The topic for which the response was generated
    :param output_dir: The directory where the YAML file will be saved
    :return: The full path to the output YAML file
    """
    try:
        topic_dir = get_topic_dir(topic, output_dir)
        unique_id = unique_id_generator()
        return topic_dir / f"{unique_id}.yaml"
    except Exception as e:
        logger.error(f"Error constructing file path: {e}")
        raise


def unique_id_generator() -> str:
    """
    Generate a unique identifier based on the current timestamp.
    
    :return: A unique identifier string with millisecond precision
    """
    return datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]


def generate_commit_message(topic: str, unique_id: str) -> str:
    """
    Generate a commit message for the saved file.
    
    :param topic: The topic name
    :param unique_id: The unique identifier
    :return: Formatted commit message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_topic = sanitise_topic(topic)
    return f"response-cheatsheet-{safe_topic}-{unique_id}-{timestamp}"


def commit_changes(file_path: Path, topic: str, unique_id: str) -> bool:
    """
    Commit the saved file to git repository.
    
    :param file_path: Path to the file to commit
    :param topic: The topic name
    :param unique_id: The unique identifier
    :return: True if commit successful, False otherwise
    """
    try:
        # Validate file exists
        if not file_path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False
            
        commit_message = generate_commit_message(topic, unique_id)
        
        # Stage the changes
        subprocess.run(["git", "add", str(file_path)], check=True, capture_output=True, text=True)
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True, text=True)
        
        logger.info(f"✅ Changes committed with message: {commit_message}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Git operation failed: {e}")
        return False
    except FileNotFoundError:
        logger.error("Git command not found. Is git installed?")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during git commit: {e}")
        return False


def get_topic_dir(topic: str, output_dir: Path = OUTPUT_DIR) -> Path:
    """
    Get or create the topic directory.
    
    :param topic: The topic name
    :param output_dir: The base output directory
    :return: Path to the topic directory
    """
    try:
        safe_topic = sanitise_topic(topic)
        full_output_dir = output_dir / safe_topic if safe_topic else output_dir
        
        # Create directory if it doesn't exist
        full_output_dir.mkdir(parents=True, exist_ok=True)
        
        return full_output_dir
        
    except Exception as e:
        logger.error(f"Error creating topic directory: {e}")
        raise


def sanitise_topic(topic: str) -> str:
    """
    Sanitize topic name for filesystem safety.
    
    :param topic: The original topic name
    :return: Sanitized topic name
    """
    try:
        if not isinstance(topic, str):
            raise TypeError(f"Topic must be a string, got {type(topic)}")
            
        if not topic.strip():
            raise ValueError("Topic cannot be empty or whitespace-only")
            
        # Remove or replace problematic characters
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_')
        
        # Ensure it's not empty after sanitization
        if not safe_topic:
            safe_topic = "unknown_topic"
            
        return safe_topic.lower()
        
    except Exception as e:
        logger.error(f"Error sanitizing topic '{topic}': {e}")
        return "unknown_topic"


# Convenience function for complete workflow
def save_and_commit_response(
    response: Union[str, Dict, Any], 
    topic: str, 
    output_dir: Optional[Path] = None
) -> tuple[bool, Optional[Path]]:
    """
    Complete workflow: save response to YAML and commit to git.
    
    :param response: The API response to save
    :param topic: The topic name
    :param output_dir: Optional output directory
    :return: Tuple of (success: bool, file_path: Optional[Path])
    """
    try:
        # Save the response
        success, file_path = save_response_to_yaml(response, topic, output_dir)
        
        if not success or not file_path:
            return False, None
            
        # Extract unique_id from filename for commit
        unique_id = file_path.stem
        
        # Commit the changes
        commit_success = commit_changes(file_path, topic, unique_id)
        
        if not commit_success:
            logger.warning("File saved but git commit failed")
            
        return True, file_path
        
    except Exception as e:
        logger.error(f"Error in save_and_commit workflow: {e}")
        return False, None
