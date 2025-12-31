import os
import sys
from pathlib import Path

vendor_path = str(Path(__file__).parent.parent / "vendor")
if vendor_path not in sys.path:
    sys.path.append(vendor_path)

current_path = str(Path(__file__).parent)
if current_path not in sys.path:
    sys.path.append(current_path)

import config
import time
import json
import asyncio
import yaml
from typing import List
import rule
import proxy
import clash
from rule_provider import rulesets_rander
from utils import get_url_and_prefix_list
from proxy_group import ProxyGroup
from yaml_format import dump_yaml

async def generate_singbox_config_str() -> str:
    return "{}"


async def generate_clash_config_str(url_list: List[str], prefix_list: List[str]) -> str:
    rule_dir = str(config.rule_dir)

    rule_group_map = config.rule_group_map

    clash_tmpl_file = config.clash_yaml_path
    proxy_filter = os.environ.get("PROXY_FILTER", config.proxy_filter)
    static_proxies = config.static_proxies

    rule_generator = rule.RuleGenerator(rule_dir, rule_group_map)
    proxy_getter = proxy.ProxyGetter(url_list, prefix_list, proxy_filter, static_proxies=static_proxies)
    tmpl_loader = clash.TmplLoader(clash_tmpl_file)
    # fqdn_of_rule_provider = os.environ.get("FQDN_RULE_PROVIDER", "")
    # rule_provider_render = RuleProviderRender(config.rule_providers_tpl_path, fqdn_of_rule_provider)

    start_time = time.time()
    rules_str, (proxy_list, proxy_name_list), final_config, (rule_providers, rulesets) = await asyncio.gather(
        rule_generator.generate(),
        proxy_getter.get_proxies(),
        tmpl_loader.load_file(),
        rulesets_rander()
        # rule_provider_render.exec()
    )
    print(f"异步加载共耗时 {time.time() - start_time} 秒")

    final_config.setdefault('proxies', []).extend(proxy_list)

    proxy_group_list = final_config.get("proxy-groups", [])

    if not proxy_group_list:
        raise ValueError(f"{clash_tmpl_file} Error, 没找到 proxy-groups")

    pg = ProxyGroup(proxy_group_list, proxy_name_list)
    final_config["proxy-groups"] = pg()

    if "rules" in final_config:
        final_config.pop("rules")

    if "rule-providers" in final_config:
        final_config.pop("rule-providers")

    tail_rule_file = config.tail_rule_path

    tail_rules = tail_rule_file.read_text()

    try:
        yaml_output = dump_yaml(final_config)
        # yaml_output = yaml.dump(
        #     final_config,
        #     default_flow_style=None,
        #     allow_unicode=True,
        #     sort_keys=False,
        #     indent=2,
        #     width=300
        # )
    except yaml.YAMLError as e:
        print(f"生成YAML时出错: {e}")
        raise e

    return yaml_output + "\n" + rule_providers + "\n" + rules_str + "\n" + rulesets + "\n" + tail_rules


def lambda_handler(event, context):
    url_list, prefix_list = asyncio.run(get_url_and_prefix_list())

    try:
        format_type = event.get("queryStringParameters", {}).get("format", "clash")

        if format_type == "json":
            content = asyncio.run(
                generate_singbox_config_str()
            )
        else:
            content = asyncio.run(
                generate_clash_config_str(url_list, prefix_list))

        if not content:
            print("未获取到任何数据：检查数据源连接")
            raise ValueError("未获取到任何数据：检查数据源连接")

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html; charset=UTF-8',
                'Access-Control-Allow-Origin': '*',
                'Content-Disposition': "attachment;filename*=UTF-8''dingt"

            },
            'body': content
        }
    except Exception as e:
        print(f"Lambda执行错误: {str(e)}")  # CloudWatch日志
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'message': '内部服务器错误',
                'error': str(e)
            }, ensure_ascii=False)
        }
