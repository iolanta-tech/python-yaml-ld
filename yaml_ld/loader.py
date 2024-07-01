import datetime

import yaml


def xsd(term: str) -> str:
    return f'http://www.w3.org/2001/XMLSchema#{term}'


def i18n(term: str) -> str:
    return f'https://www.w3.org/ns/i18n#{term}'


def tag(term: str) -> str:
    return f'tag:yaml.org,2002:{term}'


class YAMLLDLoader(yaml.SafeLoader):
    pass

CONSTRUCTORS = {
    tag('timestamp'): YAMLLDLoader.construct_scalar,
    xsd('integer'): YAMLLDLoader.construct_yaml_int,
    xsd('decimal'): YAMLLDLoader.construct_yaml_float,
    xsd('double'): YAMLLDLoader.construct_scalar,
    xsd('boolean'): YAMLLDLoader.construct_yaml_bool,
    xsd('date'): YAMLLDLoader.construct_scalar,
    xsd('time'): YAMLLDLoader.construct_scalar,
    xsd('dateTime'): YAMLLDLoader.construct_scalar,
    i18n('en-US'): YAMLLDLoader.construct_yaml_str,
    i18n('en-US_ltr'): YAMLLDLoader.construct_yaml_str,
    i18n('_rtl'): YAMLLDLoader.construct_yaml_str,
}


for yaml_tag, constructor in CONSTRUCTORS.items():
    YAMLLDLoader.add_constructor(yaml_tag, constructor)   # type: ignore
