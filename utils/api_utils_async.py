"""
Async version of api_utils for improved concurrency
"""

import asyncio
import aiofiles
import yaml
import logging
import subprocess
from typing import Optional, Union, Dict, Any
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path('outputs/cheatsheets')


async def save_response_to_yaml_async(
    response: Union[str, Dict, Any], 
    topic: str, 
    output_dir: Optional[Path] = None
) -> tuple[bool, Optional[Path]]:
    """
    Async version of save_response_to_yaml
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
        file_path = await construct_output_file_path_async(topic, output_dir)
        
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the file asynchronously
        yaml_content = yaml.dump(response, default_flow_style=False, allow_unicode=True)
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
            await file.write(yaml_content)
            
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


async def construct_output_file_path_async(topic: str, output_dir: Path = OUTPUT_DIR) -> Path:
    """
    Async version of construct_output_file_path
    """
    try:
        topic_dir = await get_topic_dir_async(topic, output_dir)
        unique_id = unique_id_generator()
        return topic_dir / f"{unique_id}.yaml"
    except Exception as e:
        logger.error(f"Error constructing file path: {e}")
        raise


async def get_topic_dir_async(topic: str, output_dir: Path = OUTPUT_DIR) -> Path:
    """
    Async version of get_topic_dir
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


def unique_id_generator() -> str:
    """
    Generate a unique identifier based on the current timestamp.
    """
    return datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]


def generate_commit_message(topic: str, unique_id: str) -> str:
    """
    Generate a commit message for the saved file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_topic = sanitise_topic(topic)
    return f"response-cheatsheet-{safe_topic}-{unique_id}-{timestamp}"


async def commit_changes_async(file_path: Path, topic: str, unique_id: str) -> bool:
    """
    Async version of commit_changes using ThreadPoolExecutor for git operations
    """
    try:
        # Validate file exists
        if not file_path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False
            
        commit_message = generate_commit_message(topic, unique_id)
        
        # Run git operations in thread pool (git operations are blocking)
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            # Stage the changes
            await loop.run_in_executor(
                executor, 
                lambda: subprocess.run(
                    ["git", "add", str(file_path)], 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
            )
            
            # Commit the changes
            await loop.run_in_executor(
                executor,
                lambda: subprocess.run(
                    ["git", "commit", "-m", commit_message], 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
            )
        
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


def sanitise_topic(topic: str) -> str:
    """
    Sanitize topic name for filesystem safety.
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


async def save_and_commit_response_async(
    response: Union[str, Dict, Any], 
    topic: str, 
    output_dir: Optional[Path] = None
) -> tuple[bool, Optional[Path]]:
    """
    Async complete workflow: save response to YAML and commit to git.
    """
    try:
        # Save the response
        success, file_path = await save_response_to_yaml_async(response, topic, output_dir)
        
        if not success or not file_path:
            return False, None
            
        # Extract unique_id from filename for commit
        unique_id = file_path.stem
        
        # Commit the changes
        commit_success = await commit_changes_async(file_path, topic, unique_id)
        
        if not commit_success:
            logger.warning("File saved but git commit failed")
            
        return True, file_path
        
    except Exception as e:
        logger.error(f"Error in save_and_commit workflow: {e}")
        return False, None


# Batch processing for multiple responses
async def process_multiple_responses(
    responses: list[tuple[Union[str, Dict, Any], str]], 
    output_dir: Optional[Path] = None,
    max_concurrent: int = 5
) -> list[tuple[bool, Optional[Path]]]:
    """
    Process multiple responses concurrently with rate limiting.
    
    :param responses: List of (response, topic) tuples
    :param output_dir: Optional output directory
    :param max_concurrent: Maximum concurrent operations
    :return: List of (success, file_path) tuples
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_single(response_data):
        async with semaphore:
            response, topic = response_data
            return await save_and_commit_response_async(response, topic, output_dir)
    
    tasks = [process_single(response_data) for response_data in responses]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle exceptions in results
    processed_results: list[tuple[bool, Optional[Path]]] = []
    for result in results:
        if isinstance(result, Exception):
            logger.error(f"Task failed with exception: {result}")
            processed_results.append((False, None))
        else:
            processed_results.append(result)  # type: ignore
    
    return processed_results 