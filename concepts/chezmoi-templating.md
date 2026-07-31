---
title: >-
  chezmoi Templating — Go 模板 + sprig 的差异化机制
category: concepts
tags: [chezmoi, templates, go-template, sprig, concept]
sources:
  - "https://www.chezmoi.io/user-guide/templating/"
  - "https://axionl.me/p/%E5%BD%92%E6%A1%A3-%E7%94%A8-chezmoi-%E7%AE%A1%E7%90%86%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6/"
  - "https://yangzh.cn/posts/posts/chezmoi-dotfiles-secrets.html"
  - "https://cn.x-cmd.com/install/chezmoi"
created: 2026-07-25T02:27:13Z
updated: 2026-07-25T10:00:00Z
summary: >-
  chezmoi 用 Go text/template + sprig 模板做差异化。.tmpl 后缀触发；变量来自内置/数据文件/config；可调用密码管理器与脚本。
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.66
lifecycle: draft
tier: core
lifecycle_changed: 2026-07-25
relationships:
  - target: "[[entities/chezmoi]]"
    type: related_to

---

# chezmoi Templating — Go 模板 + sprig 的差异化机制

chezmoi 用模板解决 dotfile 管理最棘手的问题：**同一份源态如何适配多台异构机器**。

## 选型逻辑

- **Go `text/template` 标准库**：与 chezmoi 自身用 Go 写的事实一致
- **Sprig**：约 100+ 模板 helper（base64、quote、split、env、ternary）
- **chezmoi 自有函数**：`lookup`（密码管理器）、`stat`、`quoteList`、`fromJson`、`toYaml`、`jq`、`include`、`decrypt`

为什么不用 Jinja2/Handlebars 这类更"主流"的模板语言？答：**与运行时同栈**。Go 模板在 chezmoi 二进制内即可执行，不依赖外部解释器，单文件分发保持简单。

## 模板触发条件

满足其一即可：

1. 文件后缀 `.tmpl`
2. 位于 `.chezmoitemplates/` 目录

## 变量优先级（后者覆盖前者）

```
内置 .chezmoi.*   >   .chezmoidata.<format> 文件   >   config.data 段
```

`.chezmoi` 提供：

- `.chezmoi.os` / `.chezmoi.hostname` / `.chezmoi.kernel.osrelease`
- `.chezmoi.username`
- `.chezmoi.git`（若源目录是 git 仓库）

## 可调用运行时数据源

- 1Password、Bitwarden、Vault、pass（密码管理器）
- 环境变量
- 文件系统
- 自定义脚本

调用方式统一为模板函数：

```gotemplate
{{- onepasswordRead "op://Personal/GitHub/api_token" -}}
```

## 可复用片段（DRY）

`.chezmoitemplates/` 目录支持命名片段，类似"include"机制：

```gotemplate
{{ template "common-shell-aliases" . }}
```

支持参数：

```gotemplate
{{- template "alacritty" 12 -}}
```

## 与其他模板场景的差异

| 场景 | 模板运行时机 | 模板可访问的能力 |
|---|---|---|
| chezmoi | 文件落盘前（构建期） | 密码管理器查询、shell 命令、文件系统 |
| Helm/Kustomize | 集群部署时 | 集群 API、values 文件 |
| GitHub Actions | workflow 触发时 | secrets、env |

chezmoi 的特殊之处是**模板渲染与密钥查询紧密耦合**——模板执行就是密钥查询的执行。

## 调试方式

- `chezmoi data` 列出所有可用变量
- `chezmoi execute-template '{{ .chezmoi.hostname }}'` 单文件试跑
- `chezmoi execute-template --init --promptString email=a@b.com < test.tmpl` 配合交互式参数
- `chezmoi diff` 看渲染后与目标的差异

## 自动生成模板 — `chezmoi add --autotemplate`

```sh
chezmoi add --autotemplate ~/.gitconfig
```

根据现有配置文件自动生成 `.gitconfig.tmpl`，推断可变量化的字段（如 `{{ .name }}`、`{{ .email }}`）。但 axionl 提醒：自动推断不总是符合预期——比如 hostname == username 时生成的模板在别的机器上会失败，仍需手动调整。

## 多格式配置文件

chezmoi 配置支持 JSON / HCL / YAML / TOML，由 [spf13/viper](https://github.com/spf13/viper) 解析，按 chezmoi 后缀命名（如 `chezmoi.yaml` / `chezmoi.toml`）；找到的第一个配置文件生效。

`.chezmoiignore` 也支持 Go 模板语法，与主配置共用变量：

```gotemplate
# .chezmoiignore
{{ if ne .chezmoi.os "darwin" }}
.bashrc_darwin
{{ end }}
```

## 模板函数 `promptString` — 交互式数据采集

```gotemplate
{{- $email := promptString "email" -}}
[data]
    email = "{{ $email }}"
```

搭配 `--init --promptString key=value` 在命令行动态喂数据：

```sh
chezmoi execute-template --init --promptString email=axionl@example.com < ~/test.tmpl
```

可手工完成"自动模板生成误判 → 用户手动修正 → 调式试跑"的迭代。

## 密码管理器注入：Bitwarden 模板函数

模板不必把 API key 写进源仓库，可以在渲染阶段从 Bitwarden 查询安全笔记：

```gotemplate
export ANTHROPIC_AUTH_TOKEN="{{ (bitwarden "item" "ANTHROPIC_AUTH_TOKEN").notes }}"
```

调用前需让 Bitwarden CLI 已解锁并设置 `BW_SESSION`。跨平台 shell 可提供统一的 `bw-unlock` 函数：macOS 从 Keychain 的 `security find-generic-password` 取主密码，Windows 则从 DPAPI 保护的文件经 `ConvertTo-SecureString` 读取。模板按 `.chezmoi.os` 选择实现。首次部署存在循环依赖，必须先手动保存凭据并执行一次 `bw unlock --raw`，之后才可由渲染后的函数自动解锁。

X-CMD 教程还列出 1Password、Bitwarden、LastPass、KeePassXC、gopass、pass 等后端；它们是运行时数据源，不等同于 `encrypted_` 文件加密。密码管理器缓存未同步时，`bw get item` 的 Not found 可能需要先执行 `bw sync`。

## 主机映射与一次性提示

`.chezmoi.toml.tmpl` 可以用 hostname 映射到机器短名，未知主机用 `promptStringOnce` 询问路径或 profile；该值写入配置后不会重复询问。这样同一仓库可以在工作机、个人机上使用不同的 Obsidian 路径、Git 身份或密钥引用。

## 相关链接
- [[concepts/chezmoi-three-state-model]]
- [[concepts/chezmoi-attribute-prefixes]]
- [[concepts/chezmoi-workflow]]
- [[concepts/dotfile-manager]]
- [[references/chezmoi-templating-guide]]

## 相关页面

- [[synthesis/concepts-chezmoi-templating × concepts-chezmoi-attribute-prefixes]] — synthesis
