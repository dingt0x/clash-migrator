
from pathlib import Path
from src.utils import is_yaml_string

file = Path(__file__).parent.parent / "templates/rule_providers.yaml.tpl"



content = file.read_text()


x = content.format(FQDN_RULE_PROVIDER="xxx",ruleset_path="sddf" )

print(x)

