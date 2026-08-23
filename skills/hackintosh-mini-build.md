---
title: 黑苹果小机箱装机指南（对标 Mac Studio）
category: skills
tags: [macos, tools, programming]
sources:
  - "https://blog.simplenaive.cn/posts/34.html"
  - "http://www.huerpu.cc:7000/?p=846"
created: 2026-07-02
updated: 2026-07-02
summary: 面向程序员的小尺寸高性能黑苹果方案（约 5000 元），对标 M1 Mac Studio 多核性能，支持 macOS/Windows/Linux 三系统。
base_confidence: 0.67
lifecycle: draft
lifecycle_changed: "2026-07-02"
tier: peripheral
provenance:
  extracted: 0.80
  inferred: 0.18
  ambiguous: 0.02
relationships:
  - target: "[[skills/xcode-ide-guide]]"
    type: related_to
  - target: "[[concepts/macos-window-switcher]]"
    type: related_to
  - target: "[[references/macos-window-switchers]]"
    type: related_to
  - target: "[[synthesis/macos-window-switcher × macos-window-switchers]]"
    type: related_to
---

# 黑苹果小机箱装机指南

## 性能对比

| 配置 | CPU | 内存 | R23 多核 | 价格 | 体积 |
|------|-----|------|----------|------|------|
| Mac Studio M1 Ultra | M1 Ultra | 64GB | 23705 | ¥29999 | 3.68L |
| 黑苹果方案 | i7-12700 | 64GB | ~21568 | ~¥4946 | ~4.9L |

**适用人群**：写代码、买不起 Mac Studio、有一定折腾能力。
**不适用**：打游戏、剪视频、懒得折腾。

多核编译同项目：M1 Max 约 6 分钟，黑苹果方案约 4 分钟。

## 推荐配置（对标 M1 Ultra Mac Studio）

| 配件 | 型号 | 参考价 |
|------|------|--------|
| CPU | Intel i7-12700 | — |
| 内存 | 64GB DDR4 | — |
| SSD | 1TB NVMe | — |
| 机箱 | ITX 小机箱（~5L） | — |

## MacBook Pro 2019 拼机方案

通过闲鱼购买拆机件自组 MacBook Pro 2019（适合 DIY 爱好者）：

| 配件 | 参考价（2024）|
|------|--------------|
| 主板（i7 16G 512G 含指纹）| ~¥1500 |
| 主板（i9 16G 1TB 含指纹）| ~¥2800 |
| C 壳（含键盘/扬声器，98 新）| ~¥350 |
| 散热风扇（一对）| ~¥80 |
| 触摸板 | ~¥85 |
| 电池（全新）| ~¥336 |
| 屏幕上半部分 | 较贵 |

**注意**：主板和指纹识别绑定，不同批次主板无法互换指纹键。

## 黑苹果安装要点

- 优先选择 OpenCore 引导
- 网卡：需更换为免驱网卡（如博通 BCM94360 系列）
- 显卡：若不需要 GPU 加速，核显即可；独显需选 AMD（NVIDIA 在 macOS 12+ 无驱动）
- 硬件到位后，网络良好的情况下约半天完成装机
- 装机完成后可正常升级 macOS 后续系统版本

## 相关页面

- concepts/macos-window-switcher
- references/cs193p-spring-2025
- [[skills/xcode-ide-guide]] — macOS 上的 Xcode 开发环境
- [[skills/terminal-music]] — macOS CLI 工具使用
- [[concepts/macos-window-switcher]] — 替代 macOS 内置 Cmd+Tab 的应用/窗口/标签切换工具，核心价值是把"app 粒度"扩展为"window 粒度"，并加入标签下钻、Space 过滤、
- [[references/macos-window-switchers]] — 主流 macOS 窗口切换器横向对比：AltTab / BetterCmdTab / Contexts / Witch 在许可证、macOS 兼容、布局、触发方
- [[synthesis/macos-window-switcher × macos-window-switchers]] — 概念页和参考表都存在，但真正的综合洞见是：4 个独立开发者在同一时间段、用不同设计取舍解决同一问题——这暗示 macOS 内置 Cmd+Tab 的局限是**结构

## Related

- [[synthesis/skills-hackintosh-mini-build × concepts-macos-window-switcher]] — 两个 macOS 用户的"模块化替代默认"范式
