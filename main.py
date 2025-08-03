import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from prompt_templates.main_prompt import Prompt

def get_prompt(*args) -> Prompt:
    """Return a Prompt object initialized with the default or custom arguments."""
    return Prompt(*args) if args else Prompt()

def main(dry_run: bool = False):
    dry_run = False  # CLI argument to skip API call to validate input for testing

    prompt = get_prompt()  # auto-inits client
    role = prompt.role
    prompt_type = prompt.prompt_type
    content_text = prompt.main_text  # TODO should return a content object which also has a type

    if not dry_run:
        client = prompt.client
        message = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=1000,
            temperature=1,
            system=prompt,
            messages=[  # TODO make abstract
                {
                    "role": role,
                    "content": [
                        {
                            "type": prompt_type,
                            "text": content_text,
                        }
                    ]
                }
            ]
        )
        # Claude's repsonse
        print(message.content)
    else:
        print(f"Dry run mode: {content_text}")
        print(f"Role: {role}")
        print(f"Prompt type: {prompt_type}")



if __name__== "__main__":
    main()