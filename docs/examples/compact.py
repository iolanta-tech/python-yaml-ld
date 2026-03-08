import io

from ruamel.yaml import YAML

import yaml_ld

yaml = YAML(typ='safe')
stream = io.StringIO()
yaml.dump(
    yaml_ld.compact(
        'pythagorean-theorem.yamlld',
        ctx='ctx.jsonld',
    ),
    stream,
)
print(stream.getvalue())  # noqa: WPS421
