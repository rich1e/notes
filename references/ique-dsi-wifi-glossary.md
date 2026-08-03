---
title: iQue DSi 网络术语表
category: references
tags: [nintendo, ique, networking, glossary]
sources: ["buckets/books/DSiSoftware.pdf"]
created: 2026-07-01T00:00:00Z
updated: 2026-08-03T05:47:33Z
summary: iQue DSi 互联网连接相关的网络术语（SSID/WEP/WPA/WPS/AOSS等）的中文解释。
base_confidence: 0.95
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: peripheral
provenance:
  extracted: 0.97
  inferred: 0.03
  ambiguous: 0.00
---

# iQue DSi 网络术语表

[[entities/ique-dsi|iQue DSi]] 互联网连接配置涉及以下网络术语。

## 基本网络术语

| 术语 | 解释 |
|---|---|
| **SSID** | 用于无线接入点的名字，也被称为 ESS-ID 或网络名。 |
| **密钥** | 为了加密 iQue DSi 主机与无线接入点之间连接数据而输入的数值，必须给无线接入点和 iQue DSi 设置相同的数值，也被称为加密密钥/网络密码。 |
| **IP 地址** | 为了指定网络中连接数据的发送地址或接收地址所使用的号码。 |
| **子网掩码** | 在 IP 地址中，表示所属的网络部分显示何种位数的值。 |
| **默认网关** | 所属网络的出入口，在连接的设置中指定此 IP 地址。 |
| **主要域名服务器 / 次要域名服务器** | 查询域名，就可将指定在电脑上定址的服务器，在连接的设置中定义此服务器的 IP 地址。 |
| **DHCP 服务器** | 为您提供连接网络所需的 IP 地址等设置信息的服务器。 |
| **MAC 地址** | 分配给每台网络设备的固定号码，iQue DSi 也拥有 MAC 地址。 |
| **NAT** | 为了让 LAN 中的 iQue DSi 能经互联网连接，通过改变 IP 地址的设置的功能，根据使用的 NAT 的方式，连接互联网的功能可能会发生连接故障。 |
| **MTU** | 表示在网络中传送时，可传送数据的最大值。 |
| **Proxy** | 用于访问各种互联网服务的中继服务器。 |

## 安全加密术语

| 术语 | 解释 |
|---|---|
| **WEP** | 将 iQue DSi 主机和无线接入点之间的连接数据加密的方式。 |
| **WPA-PSK(TKIP) / WPA2-PSK(TKIP)** | 将 iQue DSi 主机和无线接入点之间的连接数据加密的方式，比 WEP 的加密度更大。 |
| **WPA-PSK(AES) / WPA2-PSK(AES)** | 将 iQue DSi 主机和无线接入点之间的连接数据加密的方式，比 WEP 和 TKIP 的加密度更大。 |
| **WPS** | Wi-Fi Protected Setup 的缩写，用于简单进行无线LAN设备连接及密钥设置的规格。 |
| **AOSS** | AirStation One-touch Secure System，Buffalo Inc. 的商标，用于简单设置连接。 |

## WEP 密钥输入规格

- 连接的设置内容画面中，输入的密钥用「*」表示
- 密钥的输入方法有 ASCII 字母（大写英文数字输入方法）和 16 进制（0~9、a~f 的输入方法）
- iQue DSi 主机只能使用密钥进行加密；若使用其他加密方法，需更改无线接入点设置
- 通常在无线接入点中可登录4个密钥，将第4个密钥中第一个登录密钥输入 iQue DSi 主机的连接设置中，之后在无线接入点中也设置为使用该密钥

| 类型 | 字符数 |
|---|---|
| ASCII 字母 | 5、13 或 16 字符 |
| 16 进制 | 10、26 或 32 字符 |

## WPA 密钥输入规格

| 类型 | 字符数 |
|---|---|
| ASCII 字母 | 8~63 个字符 |
| 16 进制 | 64 字符 |

## Wi-Fi 账号术语

| 术语 | 解释 |
|---|---|
| **Wi-Fi Connection ID** | 连接 Nintendo Wi-Fi Connection 进行游戏的用户专属分配的固定号码，第一次连接 Nintendo Wi-Fi Connection 时自动设置。 |
| **Wi-Fi 用户信息** | 结合了连接设置的内容与 Wi-Fi Connection ID 的信息。 |

## 关联页面

- [[skills/ique-dsi-wifi-setup]] — Wi-Fi 具体设置步骤
- [[entities/ique-dsi]] — 主机概览
- [[references/ique-dsi-system-settings]] — 主机设置参考
