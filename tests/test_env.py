#!/usr/bin/env python3
"""
Test script for environment loader
"""
# Add the project root to the path

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from utils.env_loader import (create_env_template, find_env_file,
                              get_anthropic_api_key,
                              setup_anthropic_environment, validate_api_key)


def test_environment_loader():
    """Test the environment loader functionality."""
    print("🔧 Testing Environment Loader...")
    print("=" * 50)
    
    try:
        
        print("✅ Environment loader imported successfully")
        
        # Test finding .env file
        env_file = find_env_file()
        if env_file:
            print(f"📁 Found .env file: {env_file}")
        else:
            print("⚠️  No .env file found")
            print("💡 Creating template...")
            create_env_template()
        
        # Test environment setup
        print("\n🔑 Testing environment setup...")
        if setup_anthropic_environment():
            print("✅ Environment setup successful!")
            
            # Check API key
            api_key = get_anthropic_api_key()
            if api_key:
                print(f"🔑 API Key loaded: {api_key[:10]}...{api_key[-4:]}")
                print(f"✅ API Key valid: {validate_api_key(api_key)}")
            else:
                print("❌ No API key found")
        else:
            print("❌ Environment setup failed")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    test_environment_loader() 