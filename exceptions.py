

class ProjectBaseException(Exception):
    pass

# class PromptTooLong(ProjectBaseException):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args)
#         self.prompt_text: str = kwargs.get("")  # TODO
#         self.prompt_length = kwargs.get("")  # TODO

#     try:
#         raise ProjectBaseException(
#             f"Prompt exceeds defined max tokens ({MAX_TOKENS})")

#     except ProjectBaseException as exc:
#             print(f"x")  # TODO


