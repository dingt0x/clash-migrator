import yaml
from yaml.parser import ParserError
from yaml.scanner import ScannerError

import os
from typing import List,Tuple


async def get_url_from_env_list() -> List[str]:
    url_from_env_list = []
    for i in range(1, 9):
        url_from_env = os.environ.get(f"URL{i}", "").strip()
        if url_from_env:
            url_from_env_list.append(url_from_env)

    return url_from_env_list

async def get_url_and_prefix_list() -> Tuple[List[str], list[str]]:
    url_list = []
    prefix_list = []
    url_from_env_list=await  get_url_from_env_list()
    for url_env in url_from_env_list:
        url_env_split = url_env.split(',')
        if len(url_env_split) == 1:
            url_env_split = ["", url_env]
        prefix = url_env_split[0]
        url = url_env_split[1]
        url_list.append(url)
        prefix_list.append(prefix)

    return url_list, prefix_list



def is_yaml_string(text: str) -> bool:
    if not text or not isinstance(text, str):
        return False
    text = text.strip()
    if not text:
        return False
    try:
        result = yaml.safe_load(text)
        if result is None:
            lines = text.strip().split('\n')
            has_content = any(
                line.strip() and not line.strip().startswith('#')
                for line in lines
            )
            return has_content
        return True
    except (ParserError, ScannerError):
        return False
    except Exception:
        return False