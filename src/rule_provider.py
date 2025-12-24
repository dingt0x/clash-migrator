from pathlib import Path
import aiofiles
class RuleProviderRender:
    def __init__(self, tpl_file: Path, fqdn:str):
        self.tpl_file = tpl_file
        self.fqdn = fqdn


    async def exec(self) -> str:
        if not self.fqdn:
            return ""
        if not self.tpl_file.is_file():
            raise FileNotFoundError(f"Template file not found: {self.tpl_file}")

        async with aiofiles.open(str(self.tpl_file), mode='r', encoding='utf-8') as f:
            content = await f.read()
            return content.format(FQDN_RULE_PROVIDER=self.fqdn)
