from typing import Any, Dict
import yaml
import aiofiles
# load tmpl file and return dict
class TmplLoader:
    def __init__(self, clash_tmpl_file: str):
        self.clash_tmpl_file = clash_tmpl_file

    async def load_file(self) -> Dict[str, Any]:
        async with aiofiles.open(self.clash_tmpl_file, mode='r', encoding='utf-8') as f:
            content = await f.read()
            return yaml.safe_load(content)
