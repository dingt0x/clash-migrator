
import os
import pytest
from rule_provider import RuleProviderRender
from utils import is_yaml_string
from pathlib import Path
import config
import asyncio
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

@pytest.mark.provider
@pytest.mark.parametrize(["tpl_file", "fqdn", "want"],[
    [config.rule_providers_tpl_path, "baidu.com", True],
    [config.rule_providers_tpl_path, "baidu.com:443", True],
    [config.rule_providers_tpl_path, "", False],
    [Path("no_file"), "baidu.com", False],
    [config.rule_providers_tpl_path, os.environ.get("FQDN_RULE_PROVIDER"), True]
])
def test_rule_provider(tpl_file: Path, fqdn:str, want: bool):
    render = RuleProviderRender(tpl_file, fqdn)
    try:
        res = asyncio.run(render.exec())
    except FileNotFoundError as _:
         assert False == want
         return

    if res == "":
        assert True
        return

    is_yaml = is_yaml_string(res)
    if is_yaml != want:
        print(res)
        assert  is_yaml == want



























