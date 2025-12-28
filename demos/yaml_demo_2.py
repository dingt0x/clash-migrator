import yaml


class SmartProxiesDumper(yaml.SafeDumper):
    """智能处理：只让 proxies 列表中的项用流式风格"""

    def represent_dict(self, data):
        # 如果是 proxies 列表中的字典项，用流式
        if (len(self.represented_objects) > 1 and
                isinstance(self.represented_objects[-2], list) and
                len(self.represented_objects) > 2 and
                isinstance(self.represented_objects[-3], dict) and
                'proxies' in self.represented_objects[-3]):
            return self.represent_mapping(
                'tag:yaml.org,2002:map',
                data,
                flow_style=True
            )
        return super().represent_dict(data)
# 使用示例
data = {
    "dns": {
        "enable": True,
        "ipv6": False,
        "default-nameserver": ['tcp://223.5.5.5', 'tls://223.5.5.5'],
        "enhanced-mode": "fake-ip",
        "fake-ip-range": "198.18.0.1/16",
        "nameserver": ['https://dns.alidns.com/dns-query'],
    },
    "proxies": [
        {
            "name": "cus-vless-rality",
            "type": "vless",
            "server": "by.tindings.fun",
            "port": 443,
            "uuid": "a2dfcf1c-2d6b-49a0-81d5-cba41bc15452",
            "tls": True,
            "flow": "xtls-rprx-vision"
        },
        {
            "name": "cus-xjp.bothyi.cn:443",
            "type": "trojan",
            "server": "xjp.bothyi.cn",
            "port": 443,
            "password": "dingtianwei..."
        }
    ]
}

yaml_str = yaml.dump(
    data,
    Dumper=SmartProxiesDumper,
    default_flow_style=None,
    indent=2,
    width=float('inf'),  # 禁用换行
    allow_unicode=True
)

print(yaml_str)