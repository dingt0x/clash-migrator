rule-providers:
  ai: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/AI.yaml', path: './ruleset/{ruleset_path}/AI.yaml', interval: 86400}}
  openai: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/OpenAi.yaml', path: './ruleset/{ruleset_path}/OpenAi.yaml', interval: 86400}}
  reject: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/reject.yaml', path: './ruleset/{ruleset_path}/reject.yaml', interval: 86400}}
  icloud: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/icloud.yaml', path: './ruleset/{ruleset_path}/icloud.yaml', interval: 86400}}
  apple: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/apple.yaml', path: './ruleset/{ruleset_path}/apple.yaml', interval: 86400}}
  google: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/google.yaml', path: './ruleset/{ruleset_path}/google.yaml', interval: 86400}}
  proxy: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/proxy.yaml', path: './ruleset/{ruleset_path}/proxy.yaml', interval: 86400}}
  direct: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/direct.yaml', path: './ruleset/{ruleset_path}/direct.yaml', interval: 86400}}
  private: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/private.yaml', path: './ruleset/{ruleset_path}/private.yaml', interval: 86400}}
  gfw: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/gfw.yaml', path: './ruleset/{ruleset_path}/gfw.yaml', interval: 86400}}
  greatfire: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/greatfire.yaml', path: './ruleset/{ruleset_path}/greatfire.yaml', interval: 86400}}
  tld-not-cn: {{type: http, behavior: domain, url: 'https://{FQDN_RULE_PROVIDER}/tld-not-cn.yaml', path: './ruleset/{ruleset_path}/tld-not-cn.yaml', interval: 86400}}
  telegramcidr: {{type: http, behavior: ipcidr, url: 'https://{FQDN_RULE_PROVIDER}/telegramcidr.yaml', path: './ruleset/{ruleset_path}/telegramcidr.yaml', interval: 86400}}
  cncidr: {{type: http, behavior: ipcidr, url: 'https://{FQDN_RULE_PROVIDER}/cncidr.yaml', path: './ruleset/{ruleset_path}/cncidr.yaml', interval: 86400}}
  lancidr: {{type: http, behavior: ipcidr, url: 'https://{FQDN_RULE_PROVIDER}/lancidr.yaml', path: './ruleset/{ruleset_path}/lancidr.yaml', interval: 86400}}
  applications: {{type: http, behavior: classical, url: 'https://{FQDN_RULE_PROVIDER}/applications.yaml', path: './ruleset/{ruleset_path}/applications.yaml', interval: 86400}}
