from pathlib import Path
import pytest

@pytest.fixture
def sample_yaml_cheatsheet():
    example_cheatsheet = Path("prompt_templates/example_cheatsheet.yml")
    if example_cheatsheet is not None:
        return example_cheatsheet
    else:
        raise FileNotFoundError("Example cheatsheet not found")


@pytest.fixture
def local_generated_cheatsheets():
    """Use outputs dir of real cheatsheets"""
    # TODO
        # return [Path(s) for s in cheatsheet_path:=Abspath(assets.cheatsheets)]
    ...