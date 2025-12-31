from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv

ruleset_items = [{
    "name": "AI",
    "behavior": "domain",
    "uri_suffix": "Ruleset/AI.yaml",
    "proxy_group": "⚛️ AI"
}]

ruleset_uri_prefix="https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/Providers/"
ruleset_tpl_path=Path(__file__).parent / "rule_providers.yaml.tpl"
gh_proxy = ""


# Parse config with ENV
load_dotenv(find_dotenv())
_gh_proxy = os.environ.get("GH_PROXY", "")
gh_proxy = _gh_proxy if _gh_proxy else gh_proxy

