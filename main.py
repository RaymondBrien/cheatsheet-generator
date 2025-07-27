import sys
from pathlib import Path
from dotenv import load_dotenv
import anthropic

sys.path.append(str(Path(__file__).resolve().parent.parent))
from prompt_templates.main_prompt import Prompt

# load env variable necessary?
#load_dotenv()

#dotenv_path = Path(__file__).resolve().parent / '.env'
#if dotenv_path.exists():
#    load_dotenv(dotenv_path=dotenv_path)
#    print(".env loaded")

# default prompt text object
def get_default_prompt():
    return Prompt()


if __name__== "__main__":

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=1000,
        temperature=1,
        system=get_default_prompt().main_text
        messages=[  # TODO make abstract
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Why is the ocean salty?"
                    }
                ]
            }
        ]
    )
    print(message.content)

    response = client.responses.create(model="gpt-4.1", input=get_default_prompt())

    print(response.output_text)


