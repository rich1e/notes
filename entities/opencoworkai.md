---
title: "OpenCoworkAI"
category: entities
tags: [organization, opencoworkai, open-source, mit, ai-coding, entity]
sources:
  - "https://github.com/OpenCoworkAI/open-codesign"
  - "https://github.com/OpenCoworkAI/open-codesign/blob/main/CHANGELOG.md"
  - "https://github.com/OpenCoworkAI"
source_url: "https://github.com/OpenCoworkAI"
created: "2026-08-24T02:00:00Z"
updated: "2026-08-24T02:00:00Z"
summary: "OpenCoworkAI 是发布 Open CoDesign(本机 figma 项目实际依赖的上游)的 MIT 团队,旗下产品定位是 Claude Design / v0 / Lovable / Bolt.new 的开源替代,BYOK + 本地优先。"
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-24
base_confidence: 0.78
provenance:
  extracted: 0.72
  inferred: 0.23
  ambiguous: 0.05
relationships:
  - target: "[[entities/open-codesign]]"
    type: derived_from
  - target: "[[entities/pi-coding-agent]]"
    type: uses
  - target: "[[references/open-codesign-readme]]"
    type: related_to
---

# OpenCoworkAI

## 概况

OpenCoworkAI 是 GitHub 组织 `github.com/OpenCoworkAI`,旗下旗舰项目是 [Open CoDesign](https://github.com/OpenCoworkAI/open-codesign)(MIT 许可)。品牌定位:**「Open-source Claude Design alternative」**——BYOK(支持 Claude / GPT / Gemini / Kimi / GLM / Ollama 多模型)+ 本地优先。

## 产品哲学

- **本地优先**:SQLite 加密 + Electron safeStorage,敏感数据不出本地
- **BYOK**:用户自带 API key,不强制订阅
- **Multi-model**:同一 UI 切换多家模型供应商
- **开源**:MIT 协议 + 公开 CHANGELOG + CycloneDX SBOM + SHA256SUMS
- **Agentic**:v0.2.0 「Agentic Design」从一次性生成器升级为本地 agent

## 分发渠道

| 渠道 | 状态 |
|---|---|
| Homebrew Cask `opencoworkai/tap/open-codesign` | live |
| Scoop bucket `opencoworkai/scoop-bucket` | live |
| winget (microsoft/winget-pkgs#372310) | pending |
| Flathub | deferred |
| Snap | best-effort |
| 官网文档 `opencoworkai.github.io/open-codesign/` | live |

## 旗下项目

- **[open-codesign](https://github.com/OpenCoworkAI/open-codesign)** — 主项目,Electron 桌面 app
- **[scoop-bucket](https://github.com/OpenCoworkAI/scoop-bucket)** — Scoop 安装源

## 主要贡献者

来自 v0.2.0 CHANGELOG 致谢列表:`@hqhq1025`、`@Sun-sunshine06`、`@snowopsdev`(安全加固 PR#311)、`@mussonking`(workspace + Files 面板 PR#271)、`@MoveCloudROY`(Files 面板 PR#173)、`@cifuentesantonio`、`@VoidLight00`、`@Jiangxy-1`、`@GoDiao`、`@L4b0R`、`@cydxxzg`、dependabot。

## 与 vault 已有实体的关系

- [[entities/open-codesign]] — OpenCoworkAI 发布的主项目
- [[entities/pi-coding-agent]] — 依赖的 agent loop 框架
- [[synthesis/Research: OpenCoworkAI open-codesign]] — 完整研究
