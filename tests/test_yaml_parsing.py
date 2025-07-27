from typing import Dict, List, Union
from pathlib import Path

import yaml


def safe_load_yaml(file_path: Path) -> Union[Dict[str, str], List]:
    """Utility function to load yaml files safely"""
    with open(file_path, "r") as f:
        file = yaml.safe_load(f)
        print(file)
        return file

def test_cheatsheet_formatting(sample_yaml_cheatsheet, capsys):
    """This should be correclty loaded python dict object"""
    cs = safe_load_yaml(sample_yaml_cheatsheet)
    try:
        assert isinstance(cs, list)  # pyyaml loads as list of dicts
    except TypeError:
        raise TypeError(f"Cheatsheet is {type(cs)}")

# we want the cheatshets to be yaml files for easier data validation (dicts) 
    # we can change these into md if we need later
def test_yaml_parsing(sample_yaml_cheatsheet):
    """
    All generated cheatsheets should be rendered as yaml files
    and when loaded in correct format with required keys:"""  # TODO paramaterize this

    # assert all(isinstance(sammple_yaml_cheatsheet, glob("*.yml")))
    cs = safe_load_yaml(sample_yaml_cheatsheet)
    assert isinstance(cs, list)
    # TODO assert in real api call yaml config is validated to have correct keys (maybe with Prompt args always never being None?, important to check URL also valid in each topic file as link to real docs)

