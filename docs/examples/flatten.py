import io

from ruamel.yaml import YAML

import yaml_ld

yaml = YAML(typ='safe')
stream = io.StringIO()
yaml.dump(yaml_ld.flatten('pythagorean-theorem.yamlld'), stream)
print(stream.getvalue())  # noqa: WPS421
