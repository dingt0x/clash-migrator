
from typing import Dict, List
import os
import config
class ProxyGroup:
    def __init__(self, proxy_group_list: List[Dict],proxy_name_list: str):
        self.proxy_group_list = proxy_group_list
        self.proxy_name_list = proxy_name_list


    def __call__(self):
        group_custom = os.environ.get("GROUP_CUSTOM", config.group_custom)
        group_custom_list = []
        for i in group_custom.split(';'):
            name1 = i.split(',')[0]
            name2 = name1 + '♻️ 自动选择'
            proxy_filter = i.split(',')[1:]
            group_custom_list.append({"group": {'name': name1, 'type': 'select', 'proxies': []},
                                      "name": name1, "filter": proxy_filter})

            group_custom_list.append({"group": {'name': name2, 'type': 'url-test', 'proxies': [], 'tolerance': 50,
                                                'lazy': True, 'url': 'http://cp.cloudflare.com/generate_204',
                                                'interval': 150},
                                      "name": name2, "filter": proxy_filter})

        group_custom_dict = {i["name"]: i for i in group_custom_list}
        group_custom_names = [i["name"] for i in group_custom_list]


        for i in group_custom_list[::-1]:
            self.proxy_group_list.insert(1, i["group"])

        auto_proxy_filter = os.environ.get("AUTO_PROXY_FILTER", config.auto_proxy_filter)

        japan_proxy_filter_list = ["日本", "东京", "Japan"]
        us_proxy_filter_list = ["美国"]

        custom_proxies = []

        for index, proxy_group in enumerate(self.proxy_group_list):
            proxy_group_name = proxy_group.get("name", "")
            if proxy_group_name == "":
                raise ValueError("proxy_group_name 没有名称")

            if "♻️ 自动选择" == proxy_group_name:
                if auto_proxy_filter == "":
                    continue
                if auto_proxy_filter == "-wo-dou-yao-a":
                    proxy_group.setdefault('proxies', []).extend(self.proxy_name_list)
                else:
                    auto_proxy_filter_list = auto_proxy_filter.split(",")
                    auto_proxy_name_list = list(
                        filter(lambda x: any(f in x for f in auto_proxy_filter_list), self.proxy_name_list))
                    proxy_group.setdefault('proxies', []).extend(auto_proxy_name_list)
            elif "🇯🇵 日本" == proxy_group_name:
                japan_proxy_name_list_by_filter = list(
                    filter(lambda x: any(f in x for f in japan_proxy_filter_list), self.proxy_name_list))
                japan_proxy_name_list = list(
                    filter(lambda x: x not in custom_proxies, japan_proxy_name_list_by_filter)
                )
                proxy_group.setdefault('proxies', []).extend(japan_proxy_name_list)
            elif "🇺🇸 美国"  == proxy_group_name:
                us_proxy_name_list_by_filter = list(
                    filter(lambda x: any(f in x for f in us_proxy_filter_list), self.proxy_name_list))
                us_proxy_name_list = list(
                    filter(lambda x: x not in custom_proxies, us_proxy_name_list_by_filter)
                )
                proxy_group.setdefault('proxies', []).extend(us_proxy_name_list)

            elif proxy_group_name in group_custom_names:
                x_proxy_filter_list = group_custom_dict[proxy_group_name].get("filter")
                x_proxy_name_list = list(
                    filter(lambda x: any(f in x for f in x_proxy_filter_list), self.proxy_name_list))
                custom_proxies.extend(x_proxy_name_list)
                proxy_group.setdefault('proxies', []).extend(x_proxy_name_list)

            elif proxy_group_name == "🔰 手动选择":
                proxy_group_proxies = proxy_group.setdefault('proxies', [])

                manual_proxy_name_list = list(
                    filter(lambda x: x not in custom_proxies, self.proxy_name_list)
                )
                proxy_group_proxies.extend(group_custom_names)
                proxy_group_proxies.extend(manual_proxy_name_list)
        self.del_empty()


    def del_empty(self):
        to_del_set = set()
        to_del_index = []
        for i, proxy_group in  enumerate(self.proxy_group_list):
            if not proxy_group.get('proxies', []):
                to_del_set.add(proxy_group.get('name'))
                to_del_index.append(i)

        for i in to_del_index:
            del self.proxy_group_list[i]


        for proxy_group in self.proxy_group_list:
            proxies_names = proxy_group.get('proxies',[])

            proxies_set = set(proxies_names)
            to_delete_in_proxy_group = proxies_set & to_del_set

            for i in to_delete_in_proxy_group:
                proxies_names.remove(i)












