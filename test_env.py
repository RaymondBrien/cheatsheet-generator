#!/usr/bin/env python3
"""
Test script for environment loader
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).resolve().parent))

def test_environment_loader():
    """Test the environment loader functionality."""
    print("🔧 Testing Environment Loader...")
    print("=" * 50)
    
    try:
        from utils.env_loader import (
            load_environment_variables,
            get_anthropic_api_key,
            validate_api_key,
            setup_anthropic_environment,
            create_env_template
        )
        
        print("✅ Environment loader imported successfully")
        
        # Test finding .env file
        from utils.env_loader import find_env_file
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