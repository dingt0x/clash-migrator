rule-providers:
  reject:
    type: http
    behavior: domain
    url: "https://{FQDN_RULE_PROVIDER}/reject.yaml"
    path: ./ruleset/reject.yaml
    interval: 86400

  icloud:
    type: http
    behavior: domain
    url: "https://{FQDN_RULE_PROVIDER}/icloud.yaml"
    path: ./ruleset/icloud.yaml
    interval: 86400

  apple:
    type: http
    behavior: domain
    url: "https://{FQDN_RULE_PROVIDER}/apple.yaml"
    path: ./ruleset/apple.yaml
    interval: 86400

  google:
    type: http
    behavior: domain
    url: "https://{FQDN_RULE_PROVIDER}/google.yaml"
    path: ./ruleset/google.yaml
    interval: 86400

  proxy:
    type: http
    behavior: domain
    url: "https://{FQDN_RULE_PROVIDER}/proxy.yaml"
    path: ./ruleset/proxy.yaml
    interval: 86400

  direct:
    type: http
    behavior: domain
    url: "https://{FQDN_RULE_PROVIDER}/direct.yaml"
    path: ./ruleset/direct.yaml
    interval: 86400

  private:
    type: http
    behavior: domain
    url: "https://{FQDN_RULE_PROVIDER}/private.yaml"
    path: ./ruleset/private.yaml
    interval: 86400

  gfw:
    type: http
    behavior: domain
    url: "https://{FQDN_RULE_PROVIDER}/gfw.yaml"
    path: ./ruleset/gfw.yaml
    interval: 86400

  greatfire:
    type: http
    behavior: domain
    url: "https://{FQDN_RULE_PROVIDER}/greatfire.yaml"
    path: ./ruleset/greatfire.yaml
    interval: 86400

  tld-not-cn:
    type: http
    behavior: domain
    url: "https://{FQDN_RULE_PROVIDER}/tld-not-cn.yaml"
    path: ./ruleset/tld-not-cn.yaml
    interval: 86400

  telegramcidr:
    type: http
    behavior: ipcidr
    url: "https://{FQDN_RULE_PROVIDER}/telegramcidr.yaml"
    path: ./ruleset/telegramcidr.yaml
    interval: 86400

  cncidr:
    type: http
    behavior: ipcidr
    url: "https://{FQDN_RULE_PROVIDER}/cncidr.yaml"
    path: ./ruleset/cncidr.yaml
    interval: 86400

  lancidr:
    type: http
    behavior: ipcidr
    url: "https://{FQDN_RULE_PROVIDER}/lancidr.yaml"
    path: ./ruleset/lancidr.yaml
    interval: 86400

  applications:
    type: http
    behavior: classical
    url: "https://nas.tindings.fun:5091/applications.yaml"
    path: ./ruleset/applications.yaml
    interval: 86400