from pathlib import Path
import aiofiles
import hashlib
import yaml
from dotenv import load_dotenv, find_dotenv
from typing import Tuple,List
import config

load_dotenv(find_dotenv())

class RuleProviderRender:
    def __init__(self, tpl_file: Path, fqdn:str):
        self.tpl_file = tpl_file
        self.fqdn = fqdn


    async def exec(self) -> str:
        if not self.fqdn:
            return ""
        if not self.tpl_file.is_file():
            return ""

        async with aiofiles.open(str(self.tpl_file), mode='r', encoding='utf-8') as f:
            ruleset_path=hashlib.md5(self.fqdn.encode()).hexdigest()[0:8]
            content = await f.read()
            res_content = content.format(FQDN_RULE_PROVIDER=self.fqdn,ruleset_path=ruleset_path)
            providers = yaml.safe_load(res_content)
            if not providers["rule-providers"]:
                return ""
            else:
                return res_content


async def rulesets_rander() -> Tuple[str, str]:
    if not  config.ruleset_uri_prefix:
        return "", ""

    if not config.ruleset_items:
        return "", ""

    ruleset_path: str = hashlib.md5(config.ruleset_uri_prefix.encode()).hexdigest()[0:8]
    tpl_content: str = "rule-providers:\n"
    gh_proxy :str = config.gh_proxy
    ruleset_uri_prefix :str =  gh_proxy + "/" + config.ruleset_uri_prefix if gh_proxy else config.ruleset_uri_prefix
    rule_providers_list :List[str] = []
    ruleset_rule_list : List[str]=[]


    for i in config.ruleset_items:
        behavior = i.get("behavior", "")
        uri_suffix = i.get("uri_suffix","")
        provider_name=i.get("name","")
        internal = i.get("interval", 86400)
        proxy_group= i.get("proxy_group","")
        full_uri = i.get("full_uri", "")



        path="./ruleset/" + ruleset_path + "/" + uri_suffix
        if not all([provider_name , behavior , any([uri_suffix,full_uri]), proxy_group]):
            continue
        url = full_uri if full_uri else ruleset_uri_prefix + uri_suffix

        provider = "  %s: {type: http, behavior: %s, url: '%s', path: %s, interval: %d}" %(provider_name, behavior, url, path, internal )
        rule_providers_list.append(provider)

        ruleset_rule ="- RULE-SET,%s,%s" %(provider_name, proxy_group)
        ruleset_rule_list.append(ruleset_rule)

    providers_content = tpl_content + "\n".join(rule_providers_list)
    rulesets = "\n".join(ruleset_rule_list)
    providers = yaml.safe_load(providers_content)
    if not providers["rule-providers"]:
        return "", ""
    else:
        return providers_content, rulesets
