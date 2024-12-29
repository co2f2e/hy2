#!/usr/bin/env python3
import os
import json

# 彩色输出函数
def green(text):
    return f"\033[32m{text}\033[0m"

def red(text):
    return f"\033[31m{text}\033[0m"

def yellow(text):
    return f"\033[33m{text}\033[0m"

# 用户输入验证函数
def get_input(prompt, validation_func, error_message):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            print(red(error_message))

# 数字验证函数
def is_positive_integer(value):
    return value.isdigit() and int(value) > 0

def is_valid_speed(value):
    return value.isdigit() and 1 <= int(value) <= 9999

# 获取节点配置
def get_node_config(i):
    name = input(green(f"请设置节点{i}的自定义名称: "))
    server = input(green(f"请输入节点{i}的地址: "))
    port = input(green(f"请输入节点{i}的端口号: "))
    password = input(green(f"请输入节点{i}的密码: "))
    return name, server, port, password

def generate_outbounds(names):
    return [f"\"{name}\"" for name in names]

def main():
    clear = lambda: os.system('clear')  # 清屏

    # 输出警告信息
    yellow("此脚本仅适用于hysteria2协议节点!!!")
    print()

    # 获取用户输入
    server_count = int(get_input(green('请输入Hysteria2节点的数量: '), is_positive_integer, "输入有误，请输入大于0的整数"))
    up_mbps = int(get_input(green('请设置上传速度(mbps): '), is_valid_speed, "输入有误，请输入1~9999有效的数字"))
    down_mbps = int(get_input(green('请设置下载速度(mbps): '), is_valid_speed, "输入有误，请输入1~9999有效的数字"))
    
    # 跳过证书验证选项
    choice = input(green("是否跳过证书验证？\n1) 是\n2) 否\n请输入1或2: "))
    secure = True if choice == '1' else False
    
    # 开启TLS选项
    choice = input(green("是否开启TLS？\n1) 是\n2) 否\n请输入1或2: "))
    tls = True if choice == '1' else False

    # 初始化节点信息
    names = []
    servers = []
    ports = []
    passwords = []

    for i in range(1, server_count + 1):
        name, server, port, password = get_node_config(i)
        if name in names:
            print(red("此名称已经存在，请重新设置"))
            i -= 1
            continue
        names.append(name)
        servers.append(server)
        ports.append(port)
        passwords.append(password)

    # 生成outbounds部分
    outbounds = generate_outbounds(names)

    # 生成配置文件内容
    output_data = {
        "log": {
            "disabled": False,
            "level": "debug",
            "timestamp": True
        },
        "dns": {
            "servers": [
                {"tag": "dns_direct", "address": "223.5.5.5", "address_strategy": "ipv4_only", "strategy": "ipv4_only", "detour": "🎯 全球直连"},
                {"tag": "dns_proxy", "address": "tls://8.8.8.8", "address_strategy": "ipv4_only", "strategy": "ipv4_only", "detour": "🚀 节点选择"}
            ],
            "rules": [
                {"outbound": "any", "action": "route", "server": "dns_direct", "disable_cache": True},
                {"rule_set": "geosite-cn", "action": "route", "server": "dns_direct"},
                {"rule_set": "geosite-geolocation-!cn", "action": "route", "server": "dns_proxy"}
            ],
            "final": "dns_proxy",
            "strategy": "ipv4_only"
        },
        "inbounds": [
            {
                "type": "tun",
                "address": "172.19.0.1/30",
                "mtu": 9000,
                "auto_route": True,
                "auto_redirect": False,
                "strict_route": True,
                "stack": "system",
                "platform": {
                    "http_proxy": {
                        "enabled": False,
                        "server": "127.0.0.1",
                        "server_port": 2080
                    }
                }
            },
            {
                "type": "mixed",
                "listen": "127.0.0.1",
                "listen_port": 2080,
                "sniff": True,
                "users": []
            }
        ],
        "outbounds": [
            {"tag": "🚀 节点选择", "type": "selector", "outbounds": outbounds},
            {"tag": "📹 YouTube", "type": "selector", "outbounds": ["🚀 节点选择"] + outbounds},
            {"tag": "🤖 OpenAI", "type": "selector", "outbounds": outbounds},
            {"tag": "🍀 Google", "type": "selector", "outbounds": ["🚀 节点选择"] + outbounds},
            {"tag": "👨‍💻 Github", "type": "selector", "outbounds": ["🚀 节点选择"] + outbounds},
            {"tag": "🪟 Microsoft", "type": "selector", "outbounds": ["🚀 节点选择"] + outbounds + ["🎯 全球直连"]},
            {"tag": "🐬 OneDrive", "type": "selector", "outbounds": ["🚀 节点选择"] + outbounds},
            {"tag": "🎵 TikTok", "type": "selector", "outbounds": ["🚀 节点选择"] + outbounds},
            {"tag": "🎥 Netflix", "type": "selector", "outbounds": ["🚀 节点选择"] + outbounds},
            {"tag": "📲 Telegram", "type": "selector", "outbounds": ["🚀 节点选择"] + outbounds},
            {"tag": "🍏 Apple", "type": "selector", "outbounds": ["🎯 全球直连", "🚀 节点选择"] + outbounds},
            {"tag": "🐠 漏网之鱼", "type": "selector", "outbounds": ["🚀 节点选择", "🎯 全球直连"]},
            {"tag": "🎯 全球直连", "type": "direct"}
          ],
  "route": 
 {
   "auto_detect_interface": true,
   "final": "🐠 漏网之鱼",
   "rules": 
   [
     {"action": "sniff"},
     {"protocol": "dns", "action": "hijack-dns"},
     {"clash_mode": "Direct", "outbound": "🎯 全球直连"},
     {"clash_mode": "Global", "outbound": "🚀 节点选择"},
     {"domain": ["clash.razord.top", "yacd.metacubex.one", "yacd.haishan.me", "d.metacubex.one"], "action": "route", "outbound": "🎯 全球直连"},
     {"rule_set": "geosite-private", "action": "route", "outbound": "🎯 全球直连"},
     {"rule_set": "geosite-chat", "action": "route", "outbound": "🤖 OpenAI"},
     {"rule_set": "geosite-youtube", "action": "route", "outbound": "📹 YouTube"},
     {"rule_set": "geosite-github", "action": "route", "outbound": "👨‍💻 Github"},
     {"rule_set": ["geosite-google", "geoip-google"], "action": "route", "outbound": "🍀 Google"},
     {"rule_set": ["geosite-telegram", "geoip-telegram"], "action": "route", "outbound": "📲 Telegram"},
     {"rule_set": "geosite-tiktok", "action": "route", "outbound": "🎵 TikTok"},
     {"rule_set": ["geosite-netflix", "geoip-netflix"], "action": "route", "outbound": "🎥 Netflix"},
     {"rule_set": ["geosite-apple", "geoip-apple"], "action": "route", "outbound": "🍏 Apple"},
     {"rule_set": "geosite-onedrive", "action": "route", "outbound": "🐬 OneDrive"},
     {"rule_set": "geosite-microsoft", "action": "route", "outbound": "🪟 Microsoft"},
     {"rule_set": "geosite-geolocation-!cn", "action": "route", "outbound": "🚀 节点选择"},
     {"rule_set": ["geoip-cn", "geosite-cn"], "action": "route", "outbound": "🎯 全球直连"}
   ],
    "rule_set": [
      { "tag": "geosite-chat", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/category-ai-chat-!cn.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-youtube", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/youtube.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-google", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/google.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-github", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/github.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-telegram", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/telegram.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-tiktok", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/tiktok.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-netflix", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/netflix.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-apple", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/apple.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-microsoft", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/microsoft.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-onedrive", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/onedrive.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-geolocation-!cn", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/geolocation-!cn.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-cn", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/cn.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geosite-private", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geosite/private.srs", "download_detour": "🎯 全球直连" },   
      { "tag": "geoip-google", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geoip/google.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geoip-telegram", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geoip/telegram.srs", "download_detour": "🎯 全球直连" },     
      { "tag": "geoip-netflix", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geoip/netflix.srs", "download_detour": "🎯 全球直连" },     
      { "tag": "geoip-apple", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo-lite/geoip/apple.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geoip-cn", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geoip/cn.srs", "download_detour": "🎯 全球直连" },
      { "tag": "geoip-private", "type": "remote", "format": "binary", "url": "https://ghgo.xyz/https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/sing/geo/geoip/private.srs", "download_detour": "🎯 全球直连" }
    ]
  }
}

    for i in range(server_count):
        node_config = {
            "tag": names[i],
            "server": servers[i],
            "server_port": int(ports[i]),
            "type": "hysteria2",
            "up_mbps": up_mbps,
            "down_mbps": down_mbps,
            "password": passwords[i],
            "tls": {
                "insecure": secure,
                "enabled": tls
            },
            "tcp_fast_open": False
        }
        output_data["outbounds"].append(node_config)

    # 写入输出文件
    output_file = "/etc/singbox_tun.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(yellow(f"配置文件已生成路径如下：{output_file}"))

if __name__ == "__main__":
    main()