from yaml import safe_load, dump


def validate_str(file):
    print(yaml.dump(file))
    with yaml.safe_load(file):
        ...


def yaml_to_md(file):
    with yaml.dump(file):
        ...
