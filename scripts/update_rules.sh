#!/bin/bash
# https://github.com/ACL4SSR/ACL4SSR/blob/master/Clash/config/ACL4SSR_Online_Full.ini
set -e

cat <<EOF >/dev/null
# refer
置规则标志位
ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/LocalAreaNetwork.list
ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/UnBan.list
ruleset=🛑 广告拦截,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/BanAD.list
ruleset=🍃 应用净化,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/BanProgramAD.list
ruleset=📢 谷歌FCM,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/GoogleFCM.list
ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/GoogleCN.list
ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/SteamCN.list
ruleset=Ⓜ️ 微软Bing,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Bing.list
ruleset=Ⓜ️ 微软云盘,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/OneDrive.list
ruleset=Ⓜ️ 微软服务,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Microsoft.list
ruleset=🍎 苹果服务,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Apple.list
ruleset=📲 电报消息,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Telegram.list
ruleset=💬 Ai平台,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/AI.list
ruleset=💬 Ai平台,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/OpenAi.list
ruleset=🎶 网易音乐,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/NetEaseMusic.list
ruleset=🎮 游戏平台,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Epic.list
ruleset=🎮 游戏平台,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Origin.list
ruleset=🎮 游戏平台,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Sony.list
ruleset=🎮 游戏平台,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Steam.list
ruleset=🎮 游戏平台,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Nintendo.list
ruleset=📹 油管视频,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/YouTube.list
ruleset=🎥 奈飞视频,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Netflix.list
ruleset=📺 巴哈姆特,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Bahamut.list
ruleset=📺 哔哩哔哩,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/BilibiliHMT.list
ruleset=📺 哔哩哔哩,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Bilibili.list
ruleset=🌏 国内媒体,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaMedia.list
ruleset=🌍 国外媒体,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyMedia.list
ruleset=🚀 节点选择,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyGFWlist.list
;ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaIp.list
ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaDomain.list
ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaCompanyIp.list
ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Download.list
;ruleset=🎯 全球直连,[]GEOIP,LAN
ruleset=🎯 全球直连,[]GEOIP,CN
ruleset=🐟 漏网之鱼,[]FINAL
;设置规则标志位
EOF

# https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/Providers/Ruleset/AI.yaml
#provider_source_prefix="https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/Providers/Ruleset"

repo_base_dir=$(git rev-parse --show-toplevel 2>/dev/null)
source "${repo_base_dir}/.env"
cd "${repo_base_dir}"
download_rule_path="${repo_base_dir}/templates/rules"
source_prefix="https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash"

if [ -n "$GH_PROXY" ]; then
    source_prefix="${GH_PROXY}/${source_prefix}"
fi


download() {
    rule_group=$1
    ruleset_prefix="${3-""}"

    if [ "${ruleset_prefix}" = "" ]; then
        uri_suffix="$2"
    else
        uri_suffix="${ruleset_prefix}/$2"
    fi

    dst_path="$download_rule_path/${rule_group}"

    if [ ! -e "$dst_path" ]; then
        mkdir "$dst_path"
    fi

    echo "Downloading $uri_suffix to ${dst_path}/$2 ... "
    echo "curl -s -o ${dst_path}/$2 ${source_prefix}/$uri_suffix"

    if curl -s -o "${dst_path}/$2" "${source_prefix}/$uri_suffix"; then
        echo "Successful!"
    else
        echo "Failed!"
        return 1
    fi
}

download_ruleset() {
    download "$1" "$2" "Ruleset"
}

download_rulesets_to_dir() {
    # direct
    download "direct" "LocalAreaNetwork.list"
    download "direct" "UnBan.list"
    download_ruleset "direct" "BilibiliHMT.list"
    download_ruleset "direct" "Bilibili.list"
    download "direct" "ChinaMedia.list"
    download_ruleset "direct" "SteamCN.list"
    download "direct" "GoogleCN.list"
    download_ruleset "direct" "NetEaseMusic.list"
    download "direct" "ChinaDomain.list"
    download "direct" "ChinaCompanyIp.list"
    download "direct" "Download.list"
    #
    #
    download_ruleset "ai" "AI.list"
    download_ruleset "ai" "OpenAi.list"
    download_ruleset "movie" "YouTube.list"
    download_ruleset "movie" "Netflix.list"
    download_ruleset "movie" "Bahamut.list"
    download "movie" "ProxyMedia.list"
    #
    #
    download_ruleset "proxy" "GoogleFCM.list"
    download "proxy" "ProxyGFWlist.list"
    download "proxy" "Telegram.list"
    #
    download_ruleset "game" "Epic.list"
    download_ruleset "game" "Origin.list"
    download_ruleset "game" "Sony.list"
    download_ruleset "game" "Steam.list"
    download_ruleset "game" "Nintendo.list"
    #
    #
    download "microsoft" "Bing.list"
    download "microsoft" "OneDrive.list"
    download "microsoft" "Microsoft.list"
    download "apple" "Apple.list"

    if git diff --quiet "${dst_path}"; then
        echo "✅ No rule changes detected."
    else
        echo "🛑 Rule changes detected. Please review modifications with: git diff rule"
    fi

}


download_rulesets_to_dir
