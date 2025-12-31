import os
import sys
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config


def demo1():
    items = ["apple", "banana", "orange"]
    template = "Items:\n{items}"
    result = template.format(items="\n".join(f"- {item}" for item in items))

    print(result)


# noinspection DuplicatedCode
# def demo2():
#     load_dotenv(find_dotenv())
#     ruleset_path = hashlib.md5(config.ruleset_uri_prefix.encode()).hexdigest()[0:8]
#     tpl_content = config.ruleset_tpl_path.read_text()
#     gh_proxy = config.gh_proxy
#     ruleset_uri_prefix =  gh_proxy + "/" + config.ruleset_uri_prefix if gh_proxy else config.ruleset_uri_prefix
#     rule_providers_list = []
#     ruleset_rule_list=[]
#
#     # noinspection DuplicatedCode
#     for i in config.ruleset_items:
#         behavior = i["behavior"]
#         url = ruleset_uri_prefix + i["uri_suffix"]
#         path="./ruleset/" + ruleset_path + "/" + i["uri_suffix"]
#         internal = i.get("interval", 86400)
#         provider_name=i["name"]
#         provider = "  %s: {type: http, behavior: %s, url: '%s', path: %s, interval: %d}" %(provider_name, behavior, url, path, internal )
#         rule_providers_list.append(provider)
#
#         ruleset_rule ="- RULE-SET,%s,%s" %(i["name"], i["proxy_group"])
#         ruleset_rule_list.append(ruleset_rule)
#
#     x = tpl_content.format(items="\n".join(rule_providers_list))
#     rulesets = "\n".join(ruleset_rule_list)
#     print(x)
#     print(rulesets)
#
#
#
# if __name__ == '__main__':
#     demo2()