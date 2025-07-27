import pytest
import yaml

from assets.templates import example_cheatsheet


@pytest.fixture
def sample_yaml_cheatsheet(example_cheatsheet):
    yield yaml.safe_load(example_cheatsheet)


def test_cheatsheet_formatting(sample_yaml_cheatsheet):
    """Check example_cheatsheet correctly formatted:"""
    cs =  yaml.dump(sample_yaml_cheatsheet)
    assert isinstance(cs, dict)


@pytest.fixture
def local_generated_cheatsheets():
        return [Path(s) for s in cheatsheet_path:=Abspath(assets.cheatsheets)]


# we want the cheatshets to be yaml files for easier data validation (dicts) 
    # we can change these into md if we need later
def test_yaml_parsing(local_generated_cheatsheets):
    """All generated cheatsheets should be rendered as yaml files


    and when loaded in correct format 
        with required keys:"""

        if local_generated_cheatsheets:  # TODO define
            assert all(isinstance(local_generated_cheatsheets, glob(*.yml))
        with yaml.safe_load(file):
            assert isinstance(file, dict)
        # TODO assert in real api call yaml config is validated to have correct keys (maybe with Prompt args always never being None?, important to check URL also valid in each topic file as link to real docs)

