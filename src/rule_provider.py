from pathlib import Path
import aiofiles
import hashlib
import yaml

class RuleProviderRender:
    def __init__(self, tpl_file: Path, fqdn:str):
        self.tpl_file = tpl_file
        self.fqdn = fqdn


    async def exec(self) -> str:
        if not self.fqdn:
            return ""
        if not self.tpl_file.is_file():
            return ""

        async with aiofiles.open(str(self.tpl_file), mode='r', encoding='utf-8') as f:
            ruleset_path=hashlib.md5(self.fqdn.encode()).hexdigest()[0:8]
            content = await f.read()
            res_content = content.format(FQDN_RULE_PROVIDER=self.fqdn,ruleset_path=ruleset_path)
            providers = yaml.safe_load(res_content)
            if not providers["rule-providers"]:
                return ""
            else:
                return res_content


