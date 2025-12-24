
import pytest
import config

@pytest.mark.parametrize("name,tail_string,file_type", [
    ("rule_dir","rules", "dir"),
    ("clash_yaml_path","clash.yaml", "file"),
    ("tail_rule_path", "tail_rule.yaml", "file"),
    ("proxy_groups_tpl_path", "proxy_groups.yaml.tpl", "file"),
    ("rule_providers_tpl_path", "rule_providers.yaml.tpl", "file")

])
def test_config_path(name :str, tail_string: str, file_type: str):
    templates_dir="/clash-migrator/templates"

    path_for_test = getattr(config, name, "")
    if path_for_test == "":
        assert False
    assert str(path_for_test).endswith(templates_dir + "/" + tail_string)

    if file_type == "file":
        assert path_for_test.is_file()
    else:
        assert path_for_test.is_dir()



