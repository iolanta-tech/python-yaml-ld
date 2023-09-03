import yaml


class YAMLLDLoader(yaml.SafeLoader):
    # I do not understand how, but the below makes the system to parse a YAML
    # document regardless of tags it contains, as per YAML-LD spec.
    yaml_constructors = {}
