---
title: iOS 模拟器运行时日志抓取与"代码是否真在跑"的验证
category: skill
tags: [ios, xcode, debugging, swift]
relationships:
  - target: "[[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]"
    type: complements
sources: [projects/dayfold]
summary: >-
  抓 iOS 模拟器 App 的 NSLog 须用 simctl launch --console-pty；strings 查不到
  Swift 字符串字面量不能证明代码未执行；构建成功不等于模拟器已装新包。
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
base_confidence: 0.9
lifecycle: reviewed
lifecycle_changed: 2026-09-02
---

# iOS 模拟器运行时日志抓取与"代码是否真在跑"的验证

## Context

在模拟器上排查一个只在真机交互时才复现的布局 bug，需要把临时诊断日志（`NSLog`）打出来看运行时数值。此时若日志"抓不到"，极易误判为"代码没被编译/没执行"，从而把排查带向完全错误的方向。

## Procedure

### 抓取 App 的 NSLog

```bash
xcrun simctl terminate booted <bundle-id> 2>/dev/null
nohup xcrun simctl launch --console-pty booted <bundle-id> > /tmp/app.log 2>&1 &
sleep 4
grep "<自定义前缀>" /tmp/app.log
```

`--console-pty` 直接接管 App 的 stdout/stderr，是可靠路径。

### 三个会浪费时间的陷阱

1. **`simctl spawn booted log stream` 抓不到 App 的 NSLog。** 即使 `--predicate` 写对了也常返回空文件，进而被误读为"代码没执行"。

2. **macOS 没有 `timeout` 命令**（那是 GNU coreutils）。`timeout 90 xcrun simctl launch ...` 会静默失败为 `command not found`，导致启动命令**根本没执行**，而日志文件里只有上一次遗留内容——看起来就像"新代码没生效"。

3. **`strings` 在 `.app` 里搜不到 Swift 字符串字面量，不能据此断言代码未被编译。** Swift 字符串在二进制中并非明文可搜。曾因此误判为增量构建问题，白做一次 `clean build`，并让复现多跑两轮。

### 验证代码确实在跑

只看**运行时日志**，不看二进制内容。若确需确认包已更新，比对时间戳与显式重装：

```bash
xcrun simctl install booted <path-to-.app>
xcrun simctl launch booted <bundle-id>
```

## Implications

- **构建成功 ≠ 模拟器上跑的是新包。** 改完代码必须显式 `install`，否则测的是旧二进制——由此得到的"问题仍存在"反馈会把排查引向错误结论。这一条在本次排查中实际发生过。
- 排查顺序应是：先确认日志管道通畅（能看到任意一条自己的日志），再解读数值。跳过这一步就容易在"零输出"上做过度推理。^[inferred]
- CLI 环境下 SourceKit 对跨文件类型/模块会误报（如 `No such module 'UIKit'`），一律以 `xcodebuild` 的 `BUILD SUCCEEDED` / `FAILED` 为准。

## Related

- [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]] — 用本方法定位到的 intrinsic 宽度 bug
- [[projects/dayfold/concepts/architecture-overview]] — Dayfold 架构概览
