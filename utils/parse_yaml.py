import yaml
from pathlib import Path
from typing import Optional, Union, List, Dict


def validate_str(file):
    print(yaml.dump(file))
    with yaml.safe_load(file):
        ...

def yaml_to_md(file: Path):
    pass  # TODO

def render_yaml_file(file: Path) -> Dict[str, str]:
    """
    Convert a YAML file to a dictionary.

    :param file: Path to the YAML file.
    :return: Dict[str, str] - The content of the YAML file as a dictionary.
    """
    with open(file, 'r') as f:
        return yaml.safe_load(f)

def read_yaml_key(filepath: Path, key: str, as_list: Optional[bool] = False) -> Union[List[str], str]:
    """
    Convert a YAML file to a dictionary.

    :param file: Path to the YAML file.
    :return: Union[List[str], str] - The value associated with the key, as a list if as_list is True, otherwise as a string.
    """
    with open(filepath, 'r') as f:
        file = yaml.safe_load(f)
        value =  file.get(key, "")
        return list(value) if as_list else value
