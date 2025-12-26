# clash-migrator
迁移、合并与转换 Clash 配置文件

# Python 版本
python版本： `python3.13`

# 快速开始
1. 为项目创建python 3.13 版本的venv
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate  
   ```
2. 安装本地依赖
   ```bash
   make dependency-dev  
   ```
3. 参考`.env.sample` 文件，创建`.env` 文件. 
   * `URL1` - `URL8` ， 至少写一个
   * PROXY_FILTER: 如果不需要节点过滤，请写空值
   * AUTO_PROXY_FILTER: 自动节点过滤，如果不需要自动选择，请写空值,
   * FQDN_RULE_PROVIDER: 需要结合模板实际填写
   * 最简单配置如下
     ```ini
     URL1="https://noname-subscribe.com/clsh.yaml?token=noname-token"
     PROXY_FILTER=""
     AUTO_PROXY_FILTER=""
     FQDN_RULE_PROVIDER=""
     ```
      
4. 运行 `make test` ， 会在`.cache` 生成 `clash_rule_test.yaml` 文件。

# .env 文件说明 
**`.env` 为最高优先级配置，会覆盖`config.py`中的配置**

线上部署, 务必在`aws lambda` 中配置环境变量.

本地运行，请使用.env文件



# TODO 
## 1. 部署脚本, 部署至aws中 
完成

## 2. 将proxy_group 拆分出来
完成


## 3. 新增自定义分组
两种方式,待定
1) 使用env(已经做了---)
```
NEW_GROUP="🇯🇵日本-Zhao,日本-自有;🇺🇸美国,美国-100M"
```
2) 使用config(第一种方式吧~)


