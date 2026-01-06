import asyncio
import shutil
import time
from pathlib import Path
from typing import List, Dict
import warnings

import aiofiles
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


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

async def download_from_s3(s3_path: str, local_dir: Path) -> bool:
    try:
        # Parse S3 path
        parts = s3_path.split('/', 1)
        if len(parts) != 2:
            warnings.warn(
                f"Invalid S3_CUSTOM_RULE_PATH format: {s3_path}. Expected 'bucket-name/path/to/directory'")
            return False

        bucket_name = parts[0]
        prefix = parts[1]
        if not prefix.endswith('/'):
            prefix += '/'

        # Clean up and create local directory
        if local_dir.exists():
            shutil.rmtree(local_dir)
        local_dir.mkdir(parents=True, exist_ok=True)

        # Initialize S3 client
        s3_client = boto3.client('s3')

        # List and download files
        print(f"Downloading custom rules from S3: s3://{bucket_name}/{prefix}")

        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        file_count = 0
        for page in pages:
            if 'Contents' not in page:
                continue

            for obj in page['Contents']:
                key = obj['Key']
                # Skip directories
                if key.endswith('/'):
                    continue

                # Get filename
                filename = key.split('/')[-1]
                if not filename:
                    continue

                # Download file
                local_file_path = local_dir / filename
                s3_client.download_file(bucket_name, key, str(local_file_path))
                file_count += 1
                print(f"  Downloaded: {filename}")
        print(f"Successfully downloaded {file_count} files from S3 to {local_dir}")
        return True

    except NoCredentialsError:
        warnings.warn("AWS credentials not found. Skipping S3 custom rules download.")
        return False
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code in ['403', 'AccessDenied']:
            warnings.warn(f"Access denied to S3 bucket. Skipping S3 custom rules download. Error: {str(e)}")
        else:
            warnings.warn(f"S3 client error: {str(e)}. Skipping S3 custom rules download.")
        return False
    except Exception as e:
        warnings.warn(f"Unexpected error downloading from S3: {str(e)}. Skipping S3 custom rules download.")
        return False


class RuleGenerator:
    def __init__(self, rule_dir: str, rule_group_map: List[Dict[str, str]], s3_path:str = ""):
        self.rule_dir = rule_dir
        # self.tail_rule_file = tail_rule_file
        self.rule_group_map = rule_group_map
        self.all_rule_set = set()
        self.s3_path = s3_path

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
        
        # Download from S3 if configured
        s3_custom_dir = Path("/tmp/dingt0x-clash-rules")

        if self.s3_path:
            await download_from_s3(self.s3_path, s3_custom_dir)

        for c in self.rule_group_map:
            f = c.get("path", "")
            group_name = c.get("rule", "")
            if not f or not group_name:
                print(f"警告: path or group name not exist in rule_config_map {c}")
                continue

            custom_file_path = custom_rule_dir / f"{f}.list"
            s3_custom_file_path = s3_custom_dir / f"{f}.list"
            group_dir = rule_dir_path / f

            # Check local custom file
            if custom_file_path.exists():
                res.append({"file_path": str(custom_file_path),
                            "rule_group": group_name})
            
            # Check S3 custom file
            if s3_custom_file_path.exists():
                res.append({"file_path": str(s3_custom_file_path),
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



        return res


