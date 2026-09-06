---
title: macOS 多 Xcode 共存时如何切换 —— 用 DEVELOPER_DIR 而非 sudo
tags: [xcode, macos, toolchain, environment]
summary: >-
  macOS 上并存多个 Xcode 时，临时切换工具链不需要 sudo 修改 xcode-select，
  用 DEVELOPER_DIR 环境变量即可让 xcodebuild / xcrun / devicectl 全链路生效。
project: dayfold
created: 2026-09-06
updated: 2026-09-06
sources:
  - "dayfold session (2026-09-06)"
summary: |
  macOS 同时有 /Applications/Xcode.app (16.4) 与 /Applications/Xcode-old.app (26.6)
  时，临时调用 Xcode 26.6 的工具链：
  export DEVELOPER_DIR=/Applications/Xcode-old.app/Contents/Developer
  之后 xcodebuild / xcrun / devicectl 自动指向该版本。
  不需要 sudo xcode-select -s（需要交互密码，在自动化场景不可行）。
provenance:
  extracted: 1.0
  inferred: 0.0
  ambiguous: 0.0
base_confidence: 0.95
lifecycle: draft
lifecycle_changed: 2026-09-06
---

## 用法

```bash
export DEVELOPER_DIR=/Applications/Xcode-old.app/Contents/Developer
xcodebuild -version   # → Xcode 26.6 Build 17F113
xcrun devicectl list devices
xcrun devicectl device install app --device <UDID> <App.app>
```

- 整个会话级别生效
- 不影响 `xcode-select -p` 的全局指向
- 关闭 shell 后失效，无副作用

## 为什么不直接 sudo xcode-select

```
sudo: a terminal is required to read the password
```

- 自动化脚本 / Claude Code 等无终端场景无法输入密码
- 修改 `xcode-select -p` 是全局副作用，影响其他 IDE / 工具

## 验证

```
$ export DEVELOPER_DIR=/Applications/Xcode-old.app/Contents/Developer
$ xcodebuild -version
Xcode 26.6
Build version 17F113
$ xcode-select -p
/Applications/Xcode.app/Contents/Developer    # 未变
```

## 相关

- [[ios26-xcode26-required]]
- [[ios-bundle-id-case-sensitivity]]