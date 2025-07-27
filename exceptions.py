from API_CONFIG import MAX_TOKENS


class ProjectBaseException(Exception):
    pass

class PromptTooLong(ProjectBaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.prompt_text: Str = kwargs.get("")  # TODO 
        self.prompt_length = kwargs.get("")  # TODO

    try: 
        raise ProjectBaseException(
            f"Prompt exceeds defined max prompt from API_CONFIG.yml: {MAX_TOKENS)",
            prompt_length="x"
        )  # TODO

    except ProjectBaseException as exc:
            print(f"x")  # TODO


