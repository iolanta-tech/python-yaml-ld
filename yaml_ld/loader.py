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


YAMLLDLoader.add_constructor(tag('timestamp'), YAMLLDLoader.construct_yaml_str)

YAMLLDLoader.add_constructor(xsd('integer'), YAMLLDLoader.construct_yaml_int)
YAMLLDLoader.add_constructor(xsd('decimal'), YAMLLDLoader.construct_yaml_float)

YAMLLDLoader.add_constructor(xsd('double'), YAMLLDLoader.construct_scalar)

YAMLLDLoader.add_constructor(xsd('boolean'), YAMLLDLoader.construct_yaml_bool)
YAMLLDLoader.add_constructor(xsd('date'), YAMLLDLoader.construct_scalar)
YAMLLDLoader.add_constructor(xsd('time'), YAMLLDLoader.construct_scalar)
YAMLLDLoader.add_constructor(xsd('dateTime'), YAMLLDLoader.construct_scalar)

YAMLLDLoader.add_constructor(i18n('en-US'), YAMLLDLoader.construct_yaml_str)
YAMLLDLoader.add_constructor(i18n('en-US_ltr'), YAMLLDLoader.construct_yaml_str)
YAMLLDLoader.add_constructor(i18n('_rtl'), YAMLLDLoader.construct_yaml_str)
