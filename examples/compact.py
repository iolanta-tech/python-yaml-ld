import yaml

import yaml_ld

print(
    yaml.dump(
        yaml_ld.compact(
            'pythagorean-theorem.yamlld',
            ctx='ctx.jsonld',
        ),
    ),
)
