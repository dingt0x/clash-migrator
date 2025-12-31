
import os
import pytest
from rule_provider import RuleProviderRender
from utils import is_yaml_string
from pathlib import Path
import config
import asyncio
from dotenv import load_dotenv,find_dotenv

import logging
import asyncio
import aiohttp
import yaml

from typing import List, Dict, Optional
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv(find_dotenv())

@pytest.mark.provider
@pytest.mark.parametrize(["tpl_file", "fqdn", "want"],[
    [config.rule_providers_tpl_path, "baidu.com", True],
    [config.rule_providers_tpl_path, "baidu.com:443", True],
    [config.rule_providers_tpl_path, "", False],
    [Path("no_file"), "baidu.com", False],
    [config.rule_providers_tpl_path, os.environ.get("FQDN_RULE_PROVIDER"), True]
])
def test_rule_provider(tpl_file: Path, fqdn:str, want: bool):
    render = RuleProviderRender(tpl_file, fqdn)
    try:
        res = asyncio.run(render.exec())
    except FileNotFoundError as _:
         assert False == want
         return

    if res == "":
        assert True
        return

    is_yaml = is_yaml_string(res)
    if is_yaml != want:
        print(res)
        assert  is_yaml == want


class RulesetDownloader:
    def __init__(self, base_url: str, ruleset_items:List[Dict]):
        """
        初始化下载器

        Args:
            base_url: 基础URL路径
        """
        self.ruleset_items =  ruleset_items
        self.base_url = base_url.rstrip('/')


        self.failed_downloads = []
        self.invalid_rulesets = []

    async def download_ruleset(self, session: aiohttp.ClientSession, item: Dict) -> Optional[Dict]:
        """
        下载单个ruleset文件

        Args:
            session: aiohttp会话
            item: ruleset配置项

        Returns:
            解析后的规则内容，失败返回None
        """
        url = f"{self.base_url}/{item['uri_suffix']}"
        name = item['name']

        try:
            logger.info(f"正在下载: {name} -> {url}")

            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status != 200:
                    error_msg = f"下载失败: {name}, 状态码: {response.status}"
                    logger.error(error_msg)
                    self.failed_downloads.append({
                        'name': name,
                        'url': url,
                        'error': error_msg
                    })
                    return None

                content = await response.text()
                logger.info(f"下载成功: {name}")

                # 根据behavior判断内容
                if item['behavior'] == 'classical':
                    if not self._validate_classical_ruleset(content, name):
                        return None

                # 返回解析后的内容
                return {
                    'name': name,
                    'behavior': item['behavior'],
                    'proxy_group': item['proxy_group'],
                    'content': content,
                    'parsed': self._parse_ruleset(content)
                }

        except asyncio.TimeoutError:
            error_msg = f"下载超时: {name}"
            logger.error(error_msg)
            self.failed_downloads.append({
                'name': name,
                'url': url,
                'error': error_msg
            })
        except Exception as e:
            error_msg = f"下载异常: {name}, 错误: {str(e)}"
            logger.error(error_msg)
            self.failed_downloads.append({
                'name': name,
                'url': url,
                'error': error_msg
            })

        return None

    def _validate_classical_ruleset(self, content: str, name: str) -> bool:
        """
        验证classical类型的ruleset内容

        Args:
            content: 规则内容
            name: ruleset名称

        Returns:
            是否验证通过
        """
        # 检查是否包含DOMAIN或IP-CIDR关键词
        has_domain = "DOMAIN" in content
        has_ip_cidr = "IP-CIDR" in content or "IP-CIDR6" in content

        if not (has_domain or has_ip_cidr):
            error_msg = f"无效的classical规则集: {name}, 未包含DOMAIN或IP-CIDR"
            logger.error(error_msg)
            self.invalid_rulesets.append({
                'name': name,
                'type': 'classical',
                'error': error_msg,
                'has_domain': has_domain,
                'has_ip_cidr': has_ip_cidr
            })
            return False

        logger.info(f"验证通过: {name} [DOMAIN: {has_domain}, IP-CIDR: {has_ip_cidr}]")
        return True

    def _parse_ruleset(self, content: str) -> Optional[Dict]:
        """
        解析ruleset内容

        Args:
            content: 规则内容

        Returns:
            解析后的规则字典
        """
        try:
            # 尝试解析为YAML格式
            data = yaml.safe_load(content)
            return data
        except yaml.YAMLError:
            # 如果不是YAML格式，按文本格式处理
            lines = content.strip().split('\n')
            rules = []

            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    rules.append(line)

            return {
                'raw_rules': rules,
                'rule_count': len(rules)
            }

    async def download_all_rulesets(self, max_concurrent: int = 5) -> Dict[str, Dict]:
        """
        并发下载所有rulesets

        Args:
            max_concurrent: 最大并发数

        Returns:
            下载成功的rulesets字典，key为名称，value为规则内容
        """
        connector = aiohttp.TCPConnector(limit=max_concurrent, ssl=False)

        async with aiohttp.ClientSession(connector=connector) as session:
            # 创建下载任务
            tasks = []
            for item in self.ruleset_items:
                task = asyncio.create_task(self.download_ruleset(session, item))
                tasks.append((item['name'], task))

            # 等待所有任务完成
            results = {}
            for name, task in tasks:
                try:
                    result = await task
                    if result:
                        results[name] = result
                except Exception as e:
                    logger.error(f"任务执行异常: {name}, 错误: {str(e)}")

            return results

    def print_summary(self, results: Dict[str, Dict]):
        """
        打印下载摘要

        Args:
            results: 下载结果
        """
        print("\n" + "=" * 60)
        print("下载摘要")
        print("=" * 60)
        print(f"成功下载: {len(results)}/{len(self.ruleset_items)}")

        if results:
            print("\n成功下载的rulesets:")
            for name, data in results.items():
                parsed = data.get('parsed', {})
                rule_count = parsed.get('rule_count', '未知')
                print(f"  - {name}: {data['behavior']} -> {data['proxy_group']} (规则数: {rule_count})")

        if self.failed_downloads:
            print(f"\n下载失败 ({len(self.failed_downloads)}):")
            for fail in self.failed_downloads:
                print(f"  - {fail['name']}: {fail['error']}")

        if self.invalid_rulesets:
            print(f"\n无效的rulesets ({len(self.invalid_rulesets)}):")
            for invalid in self.invalid_rulesets:
                print(f"  - {invalid['name']}: {invalid['error']}")

        print("=" * 60)



async def main():
    """主函数示例"""
    # 您的ruleset_items列表
    ruleset_items = config.ruleset_items
    base_url = config.ruleset_uri_prefix
    gh_proxy = config.gh_proxy

    base_url = gh_proxy + "/" + base_url if gh_proxy else  base_url


    # 创建下载器
    downloader = RulesetDownloader(base_url=base_url,ruleset_items=ruleset_items)

    # 下载所有rulesets
    results = await downloader.download_all_rulesets(max_concurrent=10)

    # 打印摘要
    downloader.print_summary(results)

    # 返回结果
    return {
        'successful': results,
        'failed': downloader.failed_downloads,
        'invalid': downloader.invalid_rulesets
    }


if __name__ == "__main__":
    # 运行示例
    asyncio.run(main())






















