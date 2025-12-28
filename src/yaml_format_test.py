from textwrap import indent

import pytest
from yaml_format import preprocess_proxies,MarkedFlowDumper,dump_yaml
import yaml
from typing import Dict
from pathlib import Path
import json

def load_yaml(p :Path) -> Dict:
    with p.open('r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(p :Path, s :str):
    p.write_text(s)

@pytest.mark.offline
def test_preprocess_proxies():
    file_path = Path(__file__).parent.parent /".cache/clash_rule_test.yaml"
    res_file_path = Path(__file__).parent.parent /".cache/format_clash_rule_test.yaml"
    data = load_yaml(file_path)
    yaml_str = dump_yaml(data)
    save_yaml(res_file_path, yaml_str)

    file_path_2 = Path(__file__).parent.parent/"templates/rule_providers.yaml.tpl"
    res_file_path_2 = Path(__file__).parent.parent /".cache/format_rule_providers.yaml.tpl"
    data_2 = load_yaml(file_path_2)
    yaml_str_2 = dump_yaml(data_2)
    save_yaml(res_file_path_2, yaml_str_2)

