from pathlib import Path
import os

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
templates_dir=Path(__file__).parent.parent / "templates"
rule_dir=templates_dir / "rules"
clash_yaml_path=templates_dir / "clash.yaml"
tail_rule_path= templates_dir / "tail_rule.yaml"
rule_providers_tpl_path= templates_dir / "rule_providers.yaml.tpl"
proxy_groups_tpl_path = templates_dir / "proxy_groups.yaml.tpl"

proxy_filter="vless-rality,美,日本,东京,新加坡,香港,Hong,Japan,United,Traffic,Expire,剩余,重置,到期,bothyi"
auto_proxy_filter = "230-reality"

rule_group_map = [
    {"path": "direct", "rule": "DIRECT"},
    {"path": "ai", "rule": "⚛️ AI"},
    {"path": "apple", "rule": "🍎 Apple"},
    {"path": "microsoft", "rule": "Ⓜ️ 微软服务"},
    {"path": "game", "rule": "🎯 游戏平台"},
    {"path": "movie", "rule": "🎬 Movies and TV"},
    {"path": "reject", "rule": "🛑 广告拦截"},
    {"path": "proxy", "rule": "🌎 全球代理"},
]

group_custom = "🇯🇵 天伟,天伟,trojan-35094,vless-rality,tuic-tls"
static_proxies = [] # 明文配置规则，计划废弃

_s3_custom_rule_path = "dingt0x-clash-migrate/custom-rules"
s3_path = os.environ.get("S3_CUSTOM_RULE_PATH", _s3_custom_rule_path)



# Parse config with ENV
gh_proxy = ""
_gh_proxy = os.environ.get("GH_PROXY", "")
gh_proxy = _gh_proxy if _gh_proxy else gh_proxy

ruleset_uri_prefix="https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/Providers/"
ruleset_tpl_path=Path(__file__).parent / "rule_providers.yaml.tpl"

# url is "[gh_proxy/] + ruleset_uri_prefix + uri_suffix"
# 元素中使用full_uri可以覆盖这个值
custom_uri_prefix="https://raw.githubusercontent.com/dingt0x/acl4ssr2custom/refs/heads/main/custom_rules/"
custom_uri_prefix = gh_proxy + "/" + custom_uri_prefix if gh_proxy else custom_uri_prefix
ruleset_items_custom =  [
    # {
    #     "name": "CustomDirect",
    #     "behavior": "classical",
    #     "proxy_group": "DIRECT",
    #     "uri_suffix": "custom/direct.yaml",
    #     "full_uri": custom_uri_prefix + "direct.yaml"
    # },
    # {
    #     "name": "CustomAI",
    #     "behavior": "classical",
    #     "proxy_group": "⚛️ AI",
    #     "uri_suffix": "custom/ai.yaml",
    #     "full_uri": custom_uri_prefix + "ai.yaml"
    # },
    # {
    #     "name": "CustomApple",
    #     "behavior": "classical",
    #     "proxy_group": "🍎 Apple",
    #     "uri_suffix": "custom/apple.yaml",
    #     "full_uri": custom_uri_prefix + "apple.yaml"
    # },
    # {
    #     "name": "CustomReject",
    #     "behavior": "classical",
    #     "proxy_group": "REJECT",
    #     "uri_suffix": "custom/reject.yaml",
    #     "full_uri": custom_uri_prefix + "reject.yaml"
    # },
    #
    # {
    #     "name": "CustomMovie",
    #     "behavior": "classical",
    #     "proxy_group": "🎬 Movies and TV",
    #     "uri_suffix": "custom/movie.yaml",
    #     "full_uri": custom_uri_prefix + "movie.yaml"
    # },
    # {
    #     "name": "CustomGame",
    #     "behavior": "classical",
    #     "proxy_group": "🎯 游戏平台",
    #     "uri_suffix": "custom/game.yaml",
    #     "full_uri": custom_uri_prefix + "game.yaml"
    # },
    # {
    #     "name": "CustomMicrosoft",
    #     "behavior": "classical",
    #     "proxy_group": "Ⓜ️ 微软服务",
    #     "uri_suffix": "custom/microsoft.yaml",
    #     "full_uri": custom_uri_prefix + "microsoft.yaml"
    #
    # },
    # {
    #     "name": "CustomProxy",
    #     "behavior": "classical",
    #     "proxy_group": "🌎 全球代理",
    #     "uri_suffix": "custom/proxy.yaml",
    #     "full_uri": custom_uri_prefix + "proxy.yaml"
    # }
]
_ruleset_items = [
    {
        "name": "LocalAreaNetwork",
        "behavior": "classical",
        "uri_suffix": "LocalAreaNetwork.yaml",
        "proxy_group": "DIRECT"
    },
    {
        "name": "UnBan",
        "behavior": "classical",
        "uri_suffix": "UnBan.yaml",
        "proxy_group": "DIRECT"
    },
    {
        "name": "BilibiliHMT",
        "behavior": "classical",
        "uri_suffix": "Ruleset/BilibiliHMT.yaml",
        "proxy_group": "DIRECT"
    },
    {
        "name": "Bilibili",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Bilibili.yaml",
        "proxy_group": "DIRECT"
    },
    {
        "name": "ChinaMedia",
        "behavior": "classical",
        "uri_suffix": "ChinaMedia.yaml",
        "proxy_group": "DIRECT"
    },
    {
        "name": "SteamCN",
        "behavior": "classical",
        "uri_suffix": "Ruleset/SteamCN.yaml",
        "proxy_group": "DIRECT"
    },
    {
        "name": "GoogleCN",
        "behavior": "classical",
        "uri_suffix": "Ruleset/GoogleCN.yaml",
        "proxy_group": "DIRECT"
    },
    {
        "name": "NetEaseMusic",
        "behavior": "classical",
        "uri_suffix": "Ruleset/NetEaseMusic.yaml",
        "proxy_group": "DIRECT"
    },
    {
        "name": "ChinaDomain",
        "behavior": "classical",
        "uri_suffix": "ChinaDomain.yaml",
        "proxy_group": "DIRECT"
    },
    {
        "name": "ChinaCompanyIp",
        "behavior": "ipcidr",
        "uri_suffix": "ChinaCompanyIp.yaml",
        "proxy_group": "DIRECT"
    },
    {
        "name": "AI",
        "behavior": "classical",
        "uri_suffix": "Ruleset/AI.yaml",
        "proxy_group": "⚛️ AI"
    },
    {
        "name": "OpenAi",
        "behavior": "classical",
        "uri_suffix": "Ruleset/OpenAi.yaml",
        "proxy_group": "⚛️ AI"
    },
    {
        "name": "Apple",
        "behavior": "classical",
        "uri_suffix": "Apple.yaml",
        "proxy_group": "🍎 Apple"
    },
    {
        "name": "Bing",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Bing.yaml",
        "proxy_group": "Ⓜ️ 微软服务"
    },
    {
        "name": "OneDrive",
        "behavior": "classical",
        "uri_suffix": "Ruleset/OneDrive.yaml",
        "proxy_group": "Ⓜ️ 微软服务"
    },
    {
        "name": "Microsoft",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Microsoft.yaml",
        "proxy_group": "Ⓜ️ 微软服务"
    },
    {
        "name": "Epic",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Epic.yaml",
        "proxy_group": "🎯 游戏平台"
    },
    {
        "name": "Origin",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Origin.yaml",
        "proxy_group": "🎯 游戏平台"
    },
    {
        "name": "Sony",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Sony.yaml",
        "proxy_group": "🎯 游戏平台"
    },
    {
        "name": "Steam",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Steam.yaml",
        "proxy_group": "🎯 游戏平台"
    },
    {
        "name": "Nintendo",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Nintendo.yaml",
        "proxy_group": "🎯 游戏平台"
    },
    {
        "name": "YouTube",
        "behavior": "classical",
        "uri_suffix": "Ruleset/YouTube.yaml",
        "proxy_group": "🎬 Movies and TV"
    },
    {
        "name": "Netflix",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Netflix.yaml",
        "proxy_group": "🎬 Movies and TV"
    },
    {
        "name": "Bahamut",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Bahamut.yaml",
        "proxy_group": "🎬 Movies and TV"
    },
    {
        "name": "ProxyMedia",
        "behavior": "classical",
        "uri_suffix": "ProxyMedia.yaml",
        "proxy_group": "🎬 Movies and TV"
    },
    {
        "name": "GoogleFCM",
        "behavior": "classical",
        "uri_suffix": "Ruleset/GoogleFCM.yaml",
        "proxy_group": "🌎 全球代理"
    },
    {
        "name": "Telegram",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Telegram.yaml",
        "proxy_group": "🌎 全球代理"
    },
    {
        "name": "Amazon",
        "behavior": "classical",
        "uri_suffix": "Ruleset/Amazon.yaml",
        "proxy_group": "🌎 全球代理"
    },
    {
        "name": "ProxyGFWlist",
        "behavior": "classical",
        "uri_suffix": "ProxyGFWlist.yaml",
        "proxy_group": "🌎 全球代理"
    }


]







ruleset_items = ruleset_items_custom + _ruleset_items