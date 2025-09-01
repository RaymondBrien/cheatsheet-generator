"""
Environment variable loader with robust fallback mechanisms
"""

import logging
import os
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def load_environment_variables() -> bool:
    """
    Load environment variables from .env file with robust fallback mechanisms.
    
    Returns:
        bool: True if API key is successfully loaded, False otherwise
    """
    try:
        # Try to load from python-dotenv first
        try:
            from dotenv import load_dotenv

            # Look for .env file in current directory and parent directories
            env_file = find_env_file()
            if env_file:
                load_dotenv(env_file)
                logger.info(f"✅ Loaded environment from: {env_file}")
            else:
                logger.warning("⚠️  No .env file found, trying system environment")
        except ImportError:
            logger.warning("⚠️  python-dotenv not available, using system environment")
        
        # Check if API key is available
        api_key = get_anthropic_api_key()
        if api_key:
            logger.info("✅ Anthropic API key loaded successfully")
            return True
        else:
            logger.error("❌ No Anthropic API key found")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error loading environment variables: {e}")
        return False


def find_env_file() -> Optional[Path]:
    """
    Find .env file starting from the project root (where this file is located).
    
    Returns:
        Optional[Path]: Path to .env file if found, None otherwise
    """
    # Start from the directory where this env_loader.py file is located
    current_file = Path(__file__)
    project_root = current_file.parent.parent  # Go up from utils/ to project root
    
    # Check project root first, then go up if needed
    for i in range(4):
        check_dir = project_root.parents[i] if i > 0 else project_root
        env_file = check_dir / ".env"
        
        if env_file.exists():
            return env_file
    
    return None


def get_anthropic_api_key() -> Optional[str]:
    """
    Get Anthropic API key from various sources with fallbacks.
    
    Returns:
        Optional[str]: API key if found, None otherwise
    """
    # Try multiple environment variable names
    api_key_names = [
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_API_KEY_DEV",
        "CLAUDE_API_KEY",
        "CLAUDE_API_KEY_DEV"
    ]
    
    for key_name in api_key_names:
        api_key = os.getenv(key_name)
        if api_key and api_key.strip():
            return api_key.strip()
    
    return None


def validate_api_key(api_key: str) -> bool:
    """
    Basic validation of API key format.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        bool: True if key appears valid, False otherwise
    """
    if not api_key:
        return False
    
    # Anthropic API keys typically start with 'sk-ant-' and are 48+ characters
    if not api_key.startswith('sk-ant-'):
        return False
    
    if len(api_key) < 48:
        return False
    
    return True


def setup_anthropic_environment() -> bool:
    """
    Complete setup for Anthropic environment variables.
    
    Returns:
        bool: True if setup successful, False otherwise
    """
    # Load environment variables
    if not load_environment_variables():
        return False
    
    # Get and validate API key
    api_key = get_anthropic_api_key()
    if not api_key:
        logger.error("❌ No API key found after loading environment")
        return False
    
    if not validate_api_key(api_key):
        logger.error("❌ API key format appears invalid")
        return False
    
    # Set environment variable explicitly for Anthropic SDK
    os.environ["ANTHROPIC_API_KEY"] = api_key
    
    # Also set the working directory to the project root for consistency
    try:
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        logger.info(f"✅ Set working directory to project root: {project_root}")
    except Exception as e:
        logger.warning(f"⚠️  Could not change working directory: {e}")
    
    logger.info("✅ Anthropic environment setup complete")
    return True


def create_env_template() -> None:
    """
    Create a template .env file if it doesn't exist.
    """
    env_file = Path(".env")
    
    if env_file.exists():
        logger.info("✅ .env file already exists")
        return
    
    template_content = """# Anthropic API Configuration
# Get your API key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional: Development API key
# ANTHROPIC_API_KEY_DEV=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Other configuration
MAX_TOKENS=10000
TEMPERATURE=0.7
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(template_content)
        logger.info(f"✅ Created .env template: {env_file}")
        logger.info("⚠️  Please edit .env file with your actual API key")
    except Exception as e:
        logger.error(f"❌ Failed to create .env template: {e}")


if __name__ == "__main__":
    # Test the environment loader
    logging.basicConfig(level=logging.INFO)
    
    print("🔧 Testing environment loader...")
    
    if setup_anthropic_environment():
        print("✅ Environment setup successful!")
        api_key = get_anthropic_api_key()
        if api_key:
            print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")
    else:
        print("❌ Environment setup failed!")
        print("💡 Creating .env template...")
        create_env_template() 