import asyncio
import time
from pathlib import Path
from typing import List, Dict

import aiofiles

# load files and return YAML of the rules

async def parse_file_to_list(file_path: Path) -> List[str]:
    res = []
    async with aiofiles.open(str(file_path), mode='r', encoding='utf-8') as f:
        for line in await f.readlines():
            line = line.strip()

            if not line: continue
            if line.startswith('#'): continue
            if line.startswith("USER-AGENT"): continue
            if line.startswith("URL-REGEX"): continue
            res.append(line)
        return res

class RuleGenerator:
    def __init__(self, rule_dir: str, tail_rule_file: str, rule_group_map: List[Dict[str, str]]):
        self.rule_dir = rule_dir
        self.tail_rule_file = tail_rule_file
        self.rule_group_map = rule_group_map
        self.all_rule_set = set()

    async def parse_list_to_rule(self, rule_list: List[str], rule_name: str) -> str:
        rule_content = ""
        for line in rule_list:
            if line in self.all_rule_set: continue

            if line.endswith(",no-resolve"):
                rule_content += f"- {line.replace(",no-resolve", f",{rule_name},no-resolve")}\n"
            else:
                rule_content += f"- {line},{rule_name}\n"

            self.all_rule_set.add(line)
        return rule_content


    async def parse_dir(self) -> List[Dict[str, str]]:
        res = []
        res_from_dir = []

        rule_dir_path = Path(self.rule_dir)
        custom_rule_dir = rule_dir_path / "custom"

        for c in self.rule_group_map:
            f = c.get("path", "")
            group_name = c.get("rule", "")
            if not f or not group_name:
                print(f"警告: path or group name not exist in rule_config_map {c}")
                continue

            custom_file_path = custom_rule_dir / f"{f}.list"
            group_dir = rule_dir_path / f

            if custom_file_path.exists():
                res.append({"file_path": str(custom_file_path),
                            "rule_group": group_name})

            if not group_dir.exists():
                print(f"警告: 目录 {group_dir} 不存在")

            list_files = sorted(group_dir.glob('*.list'))
            res_from_dir.extend([{"file_path": file, "rule_group": group_name}
                                 for file in list_files])
        res.extend(res_from_dir)

        return res

    async def generate(self) -> str:
        start_time = time.time()
        res = "rules:\n"
        file_group_list = await self.parse_dir()
        tasks = []
        for file_group in file_group_list:
            file = file_group.get("file_path", "")
            rule_group = file_group.get("rule_group", "")
            if file and rule_group:
                tasks.append(parse_file_to_list(file))
            else:
                print("No file or No rule group", file_group)

        rule_lists = await asyncio.gather(*tasks)
        for i, file_group in enumerate(file_group_list):
            rule_list = rule_lists[i]
            rule_group = file_group.get("rule_group", "")
            rule = await self.parse_list_to_rule(rule_list, rule_group)
            res += f"#{rule_group}\n"
            res += rule



        print(f"生成rule配置共耗时 {time.time() - start_time} 秒")
        if not res:
            raise ValueError("生成配置为空")
        with open(self.tail_rule_file, 'r') as f:
            default_rule = f.read()

        # default_rule = "- GEOIP,CN,DIRECT\n- MATCH,🐟 漏网之鱼\n"

        return res + default_rule
