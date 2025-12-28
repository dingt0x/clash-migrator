import yaml
from typing import Dict
def preprocess_proxies(data):
    if 'proxies' in data and isinstance(data['proxies'], list):
        # 为每个代理配置添加一个标记
        for i, proxy in enumerate(data['proxies']):
            if isinstance(proxy, dict):
                # 复制一份，避免修改原数据
                data['proxies'][i] = {'__flow__': True, **proxy}
    if 'proxy-groups' in data and isinstance(data['proxy-groups'], list):
        for i, proxy in enumerate(data['proxy-groups']):
            if isinstance(proxy, dict):
                # 复制一份，避免修改原数据
                data['proxy-groups'][i] = {'__flow__': True, **proxy}
    if 'rule-providers' in data and isinstance(data['rule-providers'], dict):
        for k,v in data['rule-providers'].items():
            if isinstance(v, dict):
                data['rule-providers'][k] = {'__flow__': True, **v}

    return data

class MarkedFlowDumper(yaml.SafeDumper):
    def represent_mapping(self, tag, mapping, flow_style=None):
        # 检查是否有流式标记
        if '__flow__' in mapping:
            # 移除标记并设置流式
            data = {k: v for k, v in mapping.items() if k != '__flow__'}
            return super().represent_mapping(tag, data, flow_style=True)
        return super().represent_mapping(tag, mapping, flow_style)


def dump_yaml(data :Dict) -> str:
    processed_data = preprocess_proxies(data)
    yaml_str = yaml.dump(processed_data, Dumper=MarkedFlowDumper, default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=2,width=500)
    return yaml_str