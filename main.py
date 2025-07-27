import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

sys.path.append(str(Path(__file__).resolve().parent.parent))
from prompt_templates.main_prompt import Prompt


load_dotenv()

dotenv_path = Path(__file__).resolve().parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)

client = OpenAI()


def get_default_prompt():
    p = Prompt()
    return p.default()


response = client.responses.create(model="gpt-4.1", input=get_default_prompt())

print(response.output_text)
