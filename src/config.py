from pathlib import Path
templates_dir=Path(__file__).parent.parent / "templates"
rule_dir=templates_dir / "rules"
clash_yaml_path=templates_dir / "clash.yaml"
tail_rule_path= templates_dir / "tail_rule.yaml"
rule_providers_tpl_path= templates_dir / "rule_providers.yaml.tpl"
proxy_groups_tpl_path = templates_dir / "proxy_groups.yaml.tpl"

proxy_filter="trojan-35094,vless-rality,tuic-tls,美,日本,东京,香港,Hong,Japan,United,Traffic,Expire,剩余,重置,到期,bothyi"
auto_proxy_filter = "trojan-35094,vless-rality,tuic-tls,天伟"

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

static_proxies = [] # 明文配置规则，计划废弃