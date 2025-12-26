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
from rule_provider import RuleProviderRender
from utils import get_url_and_prefix_list


async def generate_singbox_config_str() -> str:
    return "{}"


async def generate_clash_config_str(url_list: List[str], prefix_list: List[str]) -> str:
    rule_dir = str(config.rule_dir)
    tail_rule_file = str(config.tail_rule_path)
    rule_group_map = config.rule_group_map

    clash_tmpl_file = config.clash_yaml_path
    proxy_filter = os.environ.get("PROXY_FILTER", config.proxy_filter)
    static_proxies = config.static_proxies

    rule_generator = rule.RuleGenerator(rule_dir, tail_rule_file, rule_group_map)
    proxy_getter = proxy.ProxyGetter(url_list, prefix_list, proxy_filter, static_proxies=static_proxies)
    tmpl_loader = clash.TmplLoader(clash_tmpl_file)
    fqdn_of_rule_provider = os.environ.get("FQDN_RULE_PROVIDER", "")
    rule_provider_render = RuleProviderRender(config.rule_providers_tpl_path, fqdn_of_rule_provider)

    start_time = time.time()
    rules_str, (proxy_list, proxy_name_list), final_config, rule_providers = await asyncio.gather(
        rule_generator.generate(),
        proxy_getter.get_proxies(),
        tmpl_loader.load_file(),
        rule_provider_render.exec()
    )
    print(f"异步加载共耗时 {time.time() - start_time} 秒")

    final_config.setdefault('proxies', []).extend(proxy_list)

    proxy_group_list = final_config.get("proxy-groups", [])

    if not proxy_group_list:
        raise ValueError(f"{clash_tmpl_file} Error, 没找到 proxy-groups")

    group_custom = os.environ.get("GROUP_CUSTOM", config.group_custom)
    group_custom_list = [{"group": {'name': i.split(',')[0], 'type': 'url-test', 'proxies': [], 'tolerance': 50,
                                    'lazy': True, 'url': 'http://www.gstatic.com/generate_204', 'interval': 150},
                          "name": i.split(',')[0], "filter": i.split(',')[1:]} for i in group_custom.split(';')]

    group_custom_dict = {i["name"]: i for i in group_custom_list }
    group_custom_names = {i["name"]: i for i in group_custom_list}

    for i in group_custom_list[::-1]:
        proxy_group_list.insert(1, i["group"])


    delete_auto_group = False
    delete_index = 65535
    auto_proxy_filter = os.environ.get("AUTO_PROXY_FILTER", config.auto_proxy_filter)
    if auto_proxy_filter == "":
        delete_auto_group = True
    for index, proxy_group in enumerate(proxy_group_list):
        proxy_group_name = proxy_group.get("name", "")
        if proxy_group_name == "":
            raise ValueError("proxy_group_name 没有名称")

        if "自动选择" in proxy_group_name:
            if delete_auto_group:
                delete_index = index
                continue
            if auto_proxy_filter == "-wo-dou-yao-a":
                proxy_group.setdefault('proxies', []).extend(proxy_name_list)
            else:
                auto_proxy_filter_list = auto_proxy_filter.split(",")
                auto_proxy_name_list = list(
                    filter(lambda x: any(f in x for f in auto_proxy_filter_list), proxy_name_list))
                proxy_group.setdefault('proxies', []).extend(auto_proxy_name_list)
        elif proxy_group_name in group_custom_names:
            x_proxy_filter_list = group_custom_dict[proxy_group_name].get("filter")
            x_proxy_name_list = list(
                filter(lambda x: any(f in x for f in x_proxy_filter_list), proxy_name_list))
            proxy_group.setdefault('proxies', []).extend(x_proxy_name_list)



        else:
            proxy_group_proxies = proxy_group.setdefault('proxies', [])
            if delete_auto_group:
                del_auto_in_proxy_index = 65535
                for i, v in enumerate(proxy_group_proxies):
                    if "自动选择" in v:
                        del_auto_in_proxy_index = i
                if del_auto_in_proxy_index != 65535:
                    del proxy_group_proxies[del_auto_in_proxy_index]
            proxy_group_proxies.extend(group_custom_names)
            proxy_group_proxies.extend(proxy_name_list)

    # 如果不自动选择，则将该项删除
    if delete_auto_group and delete_index != 65535:
        del proxy_group_list[delete_index]

    if "rules" in final_config:
        final_config.pop("rules")

    if "rule-providers" in final_config:
        final_config.pop("rule-providers")

    try:
        yaml_output = yaml.dump(
            final_config,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=2
        )
    except yaml.YAMLError as e:
        print(f"生成YAML时出错: {e}")
        raise e

    return yaml_output + "\n" + rule_providers + "\n" + rules_str


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
