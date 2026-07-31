---
title: >-
  chezmoi Templating — User Guide
category: references
tags: [chezmoi, templates, dotfiles, go-template]
sources:
  - "https://www.chezmoi.io/user-guide/templating/"
source_url: "https://www.chezmoi.io/user-guide/templating/"
created: 2026-07-25T02:27:13Z
updated: 2026-07-25T02:27:13Z
summary: >-
  chezmoi 用户指南——模板系统。基于 Go text/template + sprig 扩展，介绍变量来源、语法、可复用模板。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.67
lifecycle: draft
tier: supporting
lifecycle_changed: 2026-07-25
relationships:
  - target: "[[entities/chezmoi]]"
    type: related_to

---

# chezmoi Templating — User Guide

- **URL**: https://www.chezmoi.io/user-guide/templating/
- **角色**: 模板系统权威说明（用户侧）

## 模板语言

- 使用 Go 标准库 `text/template` 语法
- 扩展 [sprig](http://masterminds.github.io/sprig/) 库的大量 helper
- 加上 chezmoi 自有的函数（如 `lookup`、`stat`、`quoteList`、`fromJson`、`toYaml`、`jq`、`include`、`decrypt`）

## 何时被视作模板

满足以下任一条件即触发模板渲染：

- 文件后缀为 `.tmpl`
- 文件位于 `.chezmoitemplates` 目录（或子目录）

## 变量来源（按优先级，后者覆盖前者）

1. `.chezmoi` — chezmoi 内置，如 `.chezmoi.os`、`.chezmoi.hostname`、`.chezmoi.kernel.osrelease`
2. `.chezmoidata.$FORMAT` 文件（json/jsonc/toml/yaml），按字母顺序读取
3. 配置文件 `chezmoi.toml` 中 `data` 段

调试方法：`chezmoi data` 一键查看当前机器上所有可用变量。

## 核心语法

```gotemplate
{{ .chezmoi.hostname }}

{{ if eq .chezmoi.os "darwin" }}
# darwin
{{ else if eq .chezmoi.os "linux" }}
# linux
{{ else }}
# other
{{ end }}
```

### 空白控制

`{{-` 与 `-}}` 删除前后空白：

```gotemplate
HOSTNAME={{- .chezmoi.hostname }}
```
→ `HOSTNAME=myhostname`

### 布尔与整数比较

- 布尔：`eq`、`not`、`and`、`or`
- 整数：`len`、`eq`、`ne`、`lt`、`le`、`gt`、`ge`

### 嵌套运算需显式加括号

```gotemplate
{{ if (and (eq .chezmoi.os "linux") (ne .email "me@home.org")) }}
{{ end }}
```

## 创建与编辑模板

- `chezmoi add --template ~/.zshrc`
- `chezmoi chattr +template ~/.zshrc`（已托管文件）
- 手工命名（加 `.tmpl` 后缀）
- 放到 `.chezmoitemplates/` 目录

编辑：`chezmoi edit ~/.zshrc`（保存时检查语法，`--apply` 立即生效）

## `.chezmoitemplates/`：可复用模板片段

默认以 `nil` 数据执行，向下传参需显式传 `.`：

```gotemplate
{{ template "part.tmpl" . }}
```

支持带参数：

```gotemplate
{{- template "alacritty" 12 -}}
```

或在 config 文件预定义结构化数据，再按名引用：

```yaml
data:
  alacritty:
    small: {fontsize: 12, font: DejaVu Sans Mono}
```

## 运行时数据源

chezmoi 可在模板渲染时调用：

- 密码管理器（1Password、Bitwarden、Vault、pass 等）
- 环境变量
- 文件系统
- 自定义脚本

这些以模板函数形式暴露，而非全局变量。

## 局限性

- 模板执行失败即中断整个 `apply`，没有内置 fallback
- 通过 SSH 调用密码管理器时容易超时——需在条件中兜底
- 暂无官方非英文文档

## 相关链接

- [[concepts/chezmoi-templating]]
- [[concepts/chezmoi-three-state-model]]
- [[references/chezmoi-source-state-attributes]]
- [[references/chezmoi-workflow-discussion]]