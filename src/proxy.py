import asyncio
import time
from typing import Dict, Any,List
from urllib.parse import urlparse

import aiohttp
import yaml
from utils import *

# Get URLS from ENV URL1 to URL8 and return proxies

class ProxyGetter:
    def __init__(self, url_list: List[str], prefix_list: List[str], proxy_filter:str, user_agent: str = "clashx", static_proxies: list[Dict[str, Any]] = None, ):

        self.url_list = url_list
        self.prefix_list = prefix_list
        self.timeout = aiohttp.ClientTimeout(total=10)
        self.user_agent = user_agent
        self.static_proxies = static_proxies
        self.proxy_filter=proxy_filter

    async def parse_content(self, content: str, separator: Dict[str, Any] = None, prefix: str = "") -> List[
        Dict[str, Any]]:
        if not content:
            print(f"待处理内容为空{separator}")
            return []
        lines = content.splitlines()
        start_flag = False
        yaml_content = ""
        res = []
        if separator:
            res.append(separator)

        for line in lines:
            if line.startswith("#"): continue
            if not line: continue
            if line.startswith("proxies:"):
                yaml_content += f"{line}\n"
                start_flag = True
                continue

            if start_flag:

                if line.startswith("- ") or line.startswith("  "):
                    yaml_content += f"{line}\n"
                else:
                    break
        try:
            proxies_dict = yaml.safe_load(yaml_content)

            proxy_list = proxies_dict.get("proxies", [])

            if proxy_list:
                res.extend(filter_proxy_list(proxy_list,self.proxy_filter,prefix))
                return res
            else:
                return []

        except Exception as e:
            print(f"解析proxies yaml错误: {e}")
            return []

    async def downloader(self, session: aiohttp.ClientSession, url: str) -> str:
        try:
            async with session.get(
                    url,
                    headers={'User-Agent': self.user_agent},
                    timeout=self.timeout
            ) as response:
                if response.status == 200:
                    content = await response.text()
                    return content
                else:
                    print(f"下载失败 {url}: HTTP {response.status}")
                    return ""
        except asyncio.TimeoutError:
            print(f"下载超时 {url}")
            return ""
        except Exception as e:
            print(f"下载错误 {url}: {e}")
            return ""

    async def get_proxies(self) -> Tuple[List[Dict[str, Any]], List[str]]:
        all_proxies = []
        res_list = []
        res_name_list = []
        if self.static_proxies:
            all_proxies.extend(self.static_proxies)

        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            download_tasks = [
                self.downloader(session, url) for url in self.url_list
            ]

            contents = await asyncio.gather(*download_tasks, return_exceptions=True)
        download_time = time.time()
        print(f"Download urls 共计耗时 {download_time - start_time}秒")

        parse_tasks = []
        for i, content in enumerate(contents):
            if isinstance(content, Exception):
                print(f"URL {self.url_list[i]} 处理异常: {content}")
                continue
            elif isinstance(content, str):
                if not content:
                    print(f"内容为空，url:{urlparse(self.url_list[i]).netloc}")
                # separator = get_separator(urlparse(self.url_list[i]).netloc)
                separator = {}
                parse_tasks.append(self.parse_content(content, separator, self.prefix_list[i]))

        if parse_tasks:
            proxy_lists = await asyncio.gather(*parse_tasks)
            for proxy_list in proxy_lists:
                if proxy_list:
                    all_proxies.extend(proxy_list)

        else:
            print("没有可以处理的内容")

        for proxy in all_proxies:
            proxy_name = proxy.get('name')
            if proxy.get('name') in res_name_list: continue
            res_name_list.append(proxy_name)
            res_list.append(proxy)
        print(f"提取proxies共耗时{time.time() - download_time}")
        return res_list, res_name_list


def get_separator(separator_name: str) -> Dict[str, Any]:
    return {
        "name": f"---- {separator_name} ----",
        "type": "trojan",
        "server": "127.0.0.1",
        "port": 1,
        "password": "disabled",
        "udp": False,
        "sni": ""
    }


def get_proxy_name_list(proxy_list: List[Dict[str, Any]]) -> List[str]:
    res = []
    for proxy in proxy_list:
        proxy_name = proxy.get('name', "")
        if proxy_name:
            res.append(proxy_name)

    return res



def filter_proxy_list(proxy_list: List[Dict[str,Any]],proxy_filter: str, prefix: str) -> List[Dict[str,Any]]:
    res = []
    for proxy in proxy_list:
        proxy_name=proxy['name']
        for f in proxy_filter.split(","):
            if f in proxy_name:
                proxy["name"] = proxy_name if prefix == "" else f"{prefix}-{proxy_name}"
                res.append(proxy)
                break
    return res