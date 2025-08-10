import sys
import re
from pathlib import Path
from typing import Union, Optional

sys.path.append(str(Path(__file__).resolve().parent.parent))

from API_CONFIG import MAX_TOKENS
from prompt_templates.default_prompt import DefaultPrompt


def get_default_prompt(topic: str) -> DefaultPrompt:
    """Return a DefaultPrompt object initialized with the specified topic."""
    return DefaultPrompt(topic=topic)

def validate_prompt_content(prompt, required_fields: Optional[list[str]]) -> bool:
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


def print_dry_run(role: str, prompt_type: str, prompt_text: str) -> tuple[str, ...]:
    response = (
        "\n📋 DRY RUN MODE - No API call will be made",
        "=" * 50,
        f"Role: {role}",
        f"Prompt Type: {prompt_type}",
        f"Content Length: {len(prompt_text)} characters",
        "\n📝 Prompt Content Preview:",
        "-" * 30,
        prompt_text[:900] + "..." if len(prompt_text) > 900 else prompt_text,
        "-" * 30,
        "\n✅ Dry run completed successfully!",
    )
    return response


def main(topic: str, dry_run: bool = True) -> Union[str, dict[str, str]]:
    print("🚀 Starting cheatsheet generator...")
    print(f"📚 Topic: {topic}")
    
    # Initialize response variable at the top
    response: Union[str, dict[str, str]] = ""
    
    try:
        # Ensure environment is loaded before creating prompt
        if not dry_run:
            try:
                from utils.env_loader import setup_anthropic_environment
                if not setup_anthropic_environment():
                    raise RuntimeError("Failed to setup Anthropic environment variables")
            except ImportError:
                print("⚠️  Environment loader not available, using system environment")
        
        prompt: DefaultPrompt = get_default_prompt(topic=topic)  # Pass topic to prompt
        role: str = prompt.role
        prompt_type: str = prompt.prompt_type
        prompt_text: str = prompt.main_text
        
        # Validate prompt content
        if not validate_prompt_content(prompt):
            raise ValueError("Invalid prompt content")
            
        if dry_run:
            # Convert tuple response to string for consistency
            response_tuple = print_dry_run(role=role, prompt_type=prompt_type, prompt_text=prompt_text)
            response = "\n".join(response_tuple)
        else:
            print("\n🌐 Making API call to Claude...")
            client = prompt.client
            message = client.messages.create(
                model="claude-3-7-sonnet-20250219",  # Updated to valid model
                max_tokens=MAX_TOKENS,
                temperature=1,
                system=str(prompt.main_text),  # Fixed: use main_text as system prompt
                messages=[
                    {
                        "role": prompt.message_role.value,  # Use message role from prompt
                        "content": [
                            {
                                "type": "text",  # TODO can't this be prompt_type?
                                "text": prompt_text
                            }
                        ]
                    }
                ]
            )
            print("✅ API call successful!")
            print("\n📄 Response:")
            print("=" * 50)
            
            # Handle different content block types
            # https://docs.anthropic.com/en/api/messages
            response_content = ""
            voiceover_script = ""
            
            for block in message.content:
                if hasattr(block, 'text'):
                    full_response = block.text
                    
                    # Extract cheatsheet and voiceover
                    cheatsheet_match = re.search(r'```yaml\s*(.*?)\s*```', full_response, re.DOTALL)
                    voiceover_match = re.search(r'```voiceover\s*(.*?)\s*```', full_response, re.DOTALL)
                    
                    if cheatsheet_match:
                        response_content = cheatsheet_match.group(1)
                        print(f"📄 Cheatsheet content found:\n {response_content[:100]}...")
                    if voiceover_match:
                        voiceover_script = voiceover_match.group(1)
                        print(f"🎤 Voiceover script found:\n {voiceover_script[:100]}...")
                    
                    break
            
            # If no cheatsheet content found, set a default response
            if not response_content:
                response_content = "No cheatsheet content found in API response"
            
            # Return both cheatsheet and voiceover
            response = {
                "cheatsheet": response_content,
                "voiceover": voiceover_script
            }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        response = f"Error occurred: {str(e)}"

    return response