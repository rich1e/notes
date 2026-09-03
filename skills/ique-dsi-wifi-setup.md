---
title: iQue DSi Wi-Fi 联网设置指南
category: skills
tags: [nintendo, ique, networking, nds]
sources: ["buckets/books/DSiSoftware.pdf"]
created: 2026-07-01T00:00:00Z
updated: 2026-08-03T05:47:33Z
summary: iQue DSi 四种 Wi-Fi 设置方法（AOSS/搜索接入点/USB Connector/手动）及高级 WPS 设置的完整步骤。
base_confidence: 0.83
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: supporting
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[entities/nintendo-wansui]]"
    type: related_to

---

# iQue DSi Wi-Fi 联网设置指南

[[entities/ique-dsi|iQue DSi]] 支持通过 Wi-Fi 连接互联网，用于访问 [[references/ique-dsi-shop|iQue DSi 商店]]等服务。网络术语参见 [[references/ique-dsi-wifi-glossary]]。

## 前置条件

- 宽带互联网环境（ADSL、光纤、有线电视等）
- 支持 802.11b 或 802.11g 的无线接入点（路由器）
- iQue DSi 主机

> **飞机上必须关闭无线连接。** 在主机设置 → 设置1 → 无线连接 → 关闭。

## 选择设置方法的决策流程

```
有宽带互联网？
├── 否 → 先准备宽带环境
└── 是 → LAN 环境是有线的吗？
    ├── 否（无线路由器）→ 接入点支持 AOSS 吗？
    │   ├── 是 → 使用 AOSS 自动设置（连接1～3）
    │   └── 否 → 搜索无线接入点设置（连接1～3）
    └── 是（有线）→ Nintendo Wi-Fi USB Connector（连接1～3）
                    或手动设置
高级用户：WPA/代理服务器/WPS → 高级设置（连接4～6）
```

> DS 专用软件无法使用高级设置（连接4～6），请使用普通设置（连接1～3）。

---

## 方法一：使用 AOSS 自动设置（推荐，需 Buffalo 路由器）

适用于支持 AOSS™（Buffalo Inc. 商标）的无线接入点。

1. 主机设置 → 互联网 → **连接设置**
2. 选择「未设置」的连接槽（连接1~3）
3. 点触「AOSS」
4. 按无线接入点上的 **AOSS 键**，直到对应指示灯连续闪烁2次
5. 点触「确定」，进行连接测试

> ⚠️ AOSS 设置完毕后，无线接入点处于重新启动状态，可能导致连接失败，请隔5分钟后重新测试。

---

## 方法二：搜索无线接入点

适用于不支持 AOSS 的普通无线路由器。

1. 主机设置 → 互联网 → **连接设置**
2. 选择未设置连接槽
3. 点触「搜索无线接入点」
4. 点触选择目标接入点（若找不到，请尝试手动设置）
5. 若有锁标图标，输入密钥，点触「确定」
6. 点触「确定」，进行连接测试

### 无线接入点图标说明

| 图标 | 含义 |
|---|---|
| 无锁图标 | 无需密钥（开放网络） |
| 浅色锁图标 | 已设置了对应加密方式，若连接带锁图标的接入点，需在高级设置里设置 |
| 深色锁图标 | 需要输入密钥 |

### 信号强度

0格（红色）～ 3格（绿色），越强通讯越顺畅。

---

## 方法三：Nintendo Wi-Fi USB Connector

将 Nintendo Wi-Fi USB Connector 插入宽带互联网电脑的 USB 端口，电脑作为无线接入点使用（附件尚未发售）。

1. 主机设置 → 互联网 → 连接设置 → 选择「Nintendo Wi-Fi USB Connector」
2. 确认后点触「下一步」
3. 电脑操作：点击系统任务栏通知区域图标 → 显示PC登录工具
4. 在显示的 iQue DSi 主机昵称中，选择允许连接 → 点击「允许连接」
5. DSi 点触「确定」，进行连接测试

---

## 方法四：手动设置

手动配置无线接入点的所有参数（SSID/密码/IP/DNS等）。

1. 主机设置 → 互联网 → 连接设置
2. 选择未设置连接槽
3. 点触「手动设置」
4. 配置各项目：

| 配置项 | 说明 |
|---|---|
| SSID | 无线接入点名称 |
| 安全方式 | 无/WEP/WPA-PSK(TKIP)/WPA2-PSK(AES)等 |
| 密钥/密码 | 对应安全方式的密钥 |
| 自动获取IP地址 | 开启/关闭（关闭时需手动填IP、子网掩码、默认网关、DNS） |
| PC接入服务器设置 | 开启/关闭（代理） |
| 最大数据帧大小（MTU） | 默认 1492 |

5. 设置完毕选「保存」，点触「确定」进行连接测试

---

## 方法五：高级设置（连接4~6，WPA/WPS）

用于使用 iQue DSi 专用软件（连接4~6槽）。

### WPS 按键连接

1. 主机设置 → 互联网 → 连接设置 → **高级设置** → 选择未设置连接（4~6）
2. 点触「搜索无线接入点」→ 在路由器列表选择目标
3. 选「按键连接」→ 按住路由器上的 WPS 键，直到指示灯闪烁
4. 点触「下一步」，填写 SSID 等信息
5. 点触「确定」进行连接测试

> ⚠️ WPS 设置完毕后，无线接入点处于重新启动状态，可能导致连接失败，请隔一段时间后重新测试。

### WPS PIN 码连接

将 DSi 画面上显示的 PIN 码设置到无线接入点（约需2分钟）。

---

## 选项菜单

主机设置 → 互联网 → **选项**：

| 选项 | 功能 |
|---|---|
| 主机信息 | 确认 MAC 地址与 Wi-Fi Connection ID |
| 删除 Wi-Fi 用户信息 | 从主机删除 Wi-Fi 账号 |
| 转移 Wi-Fi 用户信息 | 将 Wi-Fi 账号转移到其他 iQue DSi 主机（需通过「iQue DS 下载游戏」操作） |

> 注意：Wi-Fi 用户信息一旦转移，好友列表等信息从原主机删除；无法转移到 iQue DS / iQue DS Lite。

## 关联页面

- [[references/ique-dsi-wifi-glossary]] — 网络术语解释（SSID/WEP/WPA/AOSS/WPS等）
- [[references/ique-dsi-shop]] — 需要 Wi-Fi 才能访问
- [[entities/ique-dsi]] — 主机概览

- [[entities/nintendo-wansui]] — 任天狗狗（Nintendo Wansui）
