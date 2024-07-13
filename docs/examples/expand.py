import yaml
import yaml_ld

print(yaml.dump(yaml_ld.expand('pythagorean-theorem.yamlld')))
