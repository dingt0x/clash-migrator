
from pathlib import Path
from lambda_function import lambda_handler
from dotenv import load_dotenv, find_dotenv
import pytest
from utils import is_yaml_string

def test_lambda_handler():
    load_dotenv(find_dotenv())
    cache_dir = Path(__file__).parent.parent / ".cache"
    target_file1 = cache_dir / "clash_rule_test.yaml"
    x = lambda_handler({}, {})

    if not cache_dir.exists():
        cache_dir.mkdir()




    if x.get('statusCode',0) == 200:
        content = x.get("body")
        with target_file1.open('w', encoding='utf-8') as f1:
            f1.write(content)
        if not is_yaml_string(content):
            pytest.fail(f"错误：返回的不是yaml,请检查文件.cache/clash_rule_test.yaml")
    else:
        pytest.fail(f"API 响应状态码错误; {x}，期望 200")
