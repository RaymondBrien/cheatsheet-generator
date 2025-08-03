from prompt_templates.main_prompt import Prompt
from prompt_templates.prompt_config import Role

from typing import Union, Dict, List

class DefaultPrompt(Prompt):
    def __init__(self):
        super().__init__()
        role = Role()

        self.role: str = role.default
        self.prompt_type = "text"
        self.targetted_os: Union[str, List[str]] = ""

        # self.example_cheatsheet = Path()
        self.topic: Union[str, Dict[str, str]] = ""
        self.subtopic: Union[str, List[str]] = ""
        self.docs_links: Union[str, List[str]] = ""
        self.main_text = self.default()

        self.output_goal: str = """
        A YAML-formatted list of 5 distinct, relevant,
        and verifiable commands with correct usage explanations.
        """

        self.additional_reqs: str = f"""
        * The commands must be valid and executable on standard Unix-based systems ({self.targetted_os})
        * Only include commands relevant to the subtopic.
        * Be concise but informative.
        * Do NOT wrap the YAML in triple backticks (` ``` `).
        * Avoid repetition across subtopics.
        * If a subtopic cannot yield 5 unique, documented commands,
          return an error message instead of guessing.\n
        """

        self.format_instructions: str = """
        Return a valid YAML file structured like this:

        ```yaml
        <command_1>: "<short, correct explanation of what it does and how/when it is used>"
        <command_2>: "<...>"
        <command_3>: "<...>"
        <command_4>: "<...>"
        <command_5>: "<...>"
        ```

        Each key should be a command (like `ls`, `cat`, `grep`, `awk`, etc.).
        Each value should be a **brief, professional-level explanation** (1–2 sentences).
        The YAML must contain **exactly 5** unique commands with no duplicates or near-duplicates.\n
        """

        self.main_text: str = f"""
        You are a {self.role}, brilliant at generating a concise,
        accurate {self.topic} cheat sheet of useful commands for professional developers,
        particularly focussing on {self.subtopic}.

        You must only use commands that are commonly used and are **officially documented** in
        reputable developer references such as:
        - {self.topic} official documentation
        - from {self.docs_links}. \n

        If documentation is unavailable, do **not** include that command.
        """

        self.docs_links = ["https://www.gnu.org/software/bash/manual/bash.html"]

    def default(self):
        # ex = yaml.safe_load(self.example_cheatsheet)

        # self.topic = ex.keys()
        # self.subtopic = ex.values()
        t = [
            "main_text",
            "format_instructions",
            "additional_reqs",
            "output_goal",
        ]
        l = [getattr(self, i) for i in t]
        return "\n".join(l)