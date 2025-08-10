from typing import Union, List
from pathlib import Path
from prompt_templates.BasePrompt import Prompt
from prompt_templates.prompt_config import Role, PromptType, RequestReturnType, TargettedOs
from utils.parse_yaml import read_yaml_key, render_yaml_file


from API_CONFIG import MAX_TOKENS


class DefaultPrompt(Prompt):

    def __init__(self, topic: str):

        super().__init__()
        role = Role()

        # API configuration
        self.max_tokens: int = MAX_TOKENS
        self.temperature: float = 0.7

        # Text content
        self.request_return_type: str = RequestReturnType.TEXT.value
        self.targetted_os: str = TargettedOs.MACOS.value
        self.prompt_type: str = PromptType.TEXT.value
        self.role: str = role.default

        try:
            self.topic: str = self.validate_topic(topic)
            self.topic_file: Union[Path, None] = self.match_topic_file(topic)
            self.subtopics: Union[str, None] = ", ".join(read_yaml_key(self.topic_file, "Subtopics", as_list=True)) if self.topic_file else None
            self.topic_docs: Union[str, List[str]] = read_yaml_key(self.topic_file, "Docs") if self.topic_file else None # TODO, add catch for docs, so that if used 'as_list=True', there MUST be more than one value in order, otherwise -> ['a' 'b', 'c'] etc
        except ValueError as e:
            raise ValueError(f"Error setting up default prompt object: {e}")

        # Text Components
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

        self.voiceover_prompt: str = f"""
        Additionally, provide a voiceover script that:
        - Targets professional/aspiring software engineers
        - Is succinct and clear (2-3 minutes max)
        - Explains use cases and tips/tricks for each command
        - Uses conversational, engaging language
        - Includes practical examples for {self.topic}
        
        Format the complete response as:
        ```yaml
        [cheatsheet content]
        ```
        
        ```voiceover
        [voiceover script content]
        ```
        """

        self.main_text: str = f"""
        You are a {self.role}, brilliant at generating a concise,
        accurate *{self.topic}* cheat sheet of useful commands for professional developers,
        particularly focussing on the following subtopics: {self.subtopics}.

        You must only use commands that are commonly used and are **officially documented** in
        reputable developer references such as:
        - {self.topic} official documentation
        - from {self.topic_docs}.

        If documentation is unavailable, do **not** include that command.
        """

        self.main_text = self.default()

    def default(self):
        # ex = yaml.safe_load(self.example_cheatsheet)

        # self.topic = ex.keys()
        # self.subtopic = ex.values()
        t = [
            "main_text",
            "format_instructions",
            "additional_reqs",
            "output_goal",
            "voiceover_prompt",
        ]
        l = [getattr(self, i) for i in t]
        return "\n".join(l)
