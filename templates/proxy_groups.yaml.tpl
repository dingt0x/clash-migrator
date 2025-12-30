proxy-groups:
  - name: '♻️ 自动选择'
    type: url-test
    proxies: []
    tolerance: 50
    lazy: true
    url: 'http://www.gstatic.com/generate_204'
    interval: 150
    include_filters: []
    exclude_filers: []

  - name: '🇯🇵 日本'
    type: select
    proxies: []
    include_filters: []
    exclude_filers: []

  - name: '🇯🇵 日本 ♻️ 自动选择'
    type: url-test
    proxies: []
    tolerance: 50
    lazy: true
    url: 'http://www.gstatic.com/generate_204'
    interval: 150
    include_filters: []
    exclude_filers: []

  - name: '🇺🇸 美国'
    type: select
    proxies: []
    include_filters: []
    exclude_filers: []

  - name: '🔰 手动选择'
    type: select
    proxies:
      - '♻️ 自动选择'
      - '🇯🇵 日本'
      - '🇯🇵 日本 ♻️ 自动选择'
      - '🇺🇸 美国'
    include_filters: []
    exclude_filers: []

  - name: '⚛️ AI'
    type: select
    proxies:
      - '🔰 手动选择'
      - '♻️ 自动选择'
      - '🇯🇵 日本'
      - '🇯🇵 日本 ♻️ 自动选择'
      - '🇺🇸 美国'

  - name: '🎬 Movies and TV'
    type: select
    proxies:
      - '🔰 手动选择'
      - '♻️ 自动选择'
      - '🇯🇵 日本'
      - '🇯🇵 日本 ♻️ 自动选择'
      - '🇺🇸 美国'

  - name: 'Ⓜ️ 微软服务'
    type: select
    proxies:
      - DIRECT
      - '🔰 手动选择'
      - '♻️ 自动选择'
      - '🇯🇵 日本'
      - '🇯🇵 日本 ♻️ 自动选择'
      - '🇺🇸 美国'

  - name: '🍎 Apple'
    type: select
    proxies:
      - DIRECT
      - '🔰 手动选择'
      - '♻️ 自动选择'
      - '🇯🇵 日本'
      - '🇯🇵 日本 ♻️ 自动选择'
      - '🇺🇸 美国'

  - name: '🎯 游戏平台'
    type: select
    proxies:
      - DIRECT
      - '🔰 手动选择'
      - '♻️ 自动选择'
      - '🇯🇵 日本'
      - '🇯🇵 日本 ♻️ 自动选择'
      - '🇺🇸 美国'

  - name: '🌎 全球代理'
    type: select
    proxies:
      - '🔰 手动选择'
      - '♻️ 自动选择'
      - '🇯🇵 日本'
      - '🇯🇵 日本 ♻️ 自动选择'
      - '🇺🇸 美国'

  - name: '🛑 广告拦截'
    type: select
    proxies:
      - REJECT
      - DIRECT
      - '🔰 手动选择'
      - '♻️ 自动选择'
      - '🇯🇵 日本'
      - '🇯🇵 日本 ♻️ 自动选择'
      - '🇺🇸 美国'

  - name: '🐟 漏网之鱼'
    type: select
    proxies:
      - DIRECT
      - '🔰 手动选择'
      - '♻️ 自动选择'
      - '🇯🇵 日本'
      - '🇯🇵 日本 ♻️ 自动选择'
      - '🇺🇸 美国'