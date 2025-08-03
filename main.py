import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from prompt_templates.default_prompt import DefaultPrompt


def get_default_prompt(topic: str = "bash") -> DefaultPrompt:
    """Return a DefaultPrompt object initialized with the specified topic."""
    return DefaultPrompt(topic=topic)

def validate_prompt_content(prompt) -> bool:
    """Validate that the prompt has all required content for API call."""
    required_fields = ['role', 'main_text', 'prompt_type']
    
    for field in required_fields:
        if not hasattr(prompt, field) or not getattr(prompt, field):
            print(f"❌ Missing required field: {field}")
            return False
    
    if len(prompt.main_text) < 10:
        print(f"❌ Prompt text too short: {len(prompt.main_text)} characters")
        return False
    
    print("✅ Prompt validation passed")
    print(f"   Role: {prompt.role}")
    print(f"   Type: {prompt.prompt_type}")
    print(f"   Text length: {len(prompt.main_text)} characters")
    return True


def main(topic: str, dry_run: bool = True):  # Accept topic parameter
    print("🚀 Starting cheatsheet generator...")
    print(f"📚 Topic: {topic}")
    
    try:
        prompt = get_default_prompt(topic=topic)  # Pass topic to prompt
        
        # Validate prompt content
        if not validate_prompt_content(prompt):
            print("❌ Prompt validation failed. Exiting.")
            return

        role = prompt.role
        prompt_type = prompt.prompt_type
        content_text = prompt.main_text

        if dry_run:
            print("\n📋 DRY RUN MODE - No API call will be made")
            print("=" * 50)
            print(f"Role: {role}")
            print(f"Prompt Type: {prompt_type}")
            print(f"Content Length: {len(content_text)} characters")
            print("\n📝 Prompt Content Preview:")
            print("-" * 30)
            print(content_text[:900] + "..." if len(content_text) > 900 else content_text)
            print("-" * 30)
            print("\n✅ Dry run completed successfully!")

        else:
            print("\n🌐 Making API call to Claude...")
            client = prompt.client
            message = client.messages.create(
                model="claude-3-7-sonnet-20250219",  # Updated to valid model
                max_tokens=1000,
                temperature=1,
                system=str(prompt.main_text),  # Fixed: use main_text as system prompt
                messages=[
                    {
                        "role": prompt.message_role.value,  # Use message role from prompt
                        "content": [
                            {
                                "type": prompt_type.value,  # Use prompt type
                                "text": content_text  # Use main_text as content
                            }
                        ]
                    }
                ]
            )
            print("✅ API call successful!")
            print("\n📄 Response:")
            print("=" * 50)
            # Handle different content block types
            for block in message.content:
                if hasattr(block, 'text'):
                    print(block.text)
                else:
                    print(f"Content block type: {type(block).__name__}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
