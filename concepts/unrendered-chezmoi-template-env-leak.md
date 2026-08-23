---
title: "未渲染 chezmoi 模板的 env 泄漏 — 渲染态 × env 注入耦合"
category: concepts
tags: [chezmoi, dotfiles, secrets, env-injection, gotcha, concept]
sources:
  - "rich1e session (2026-08-24)"
created: 2026-08-24
updated: 2026-08-24
summary: chezmoi dotfile 用 `{{ keyring ... }}` 模板注入密钥到 env 时,若 dotfile 未被 `chezmoi apply` 渲染,字面模板字符串会作为"密钥"被下游消费者读到,导致 API 1004 login fail 或其它凭据相关错误。核心抽象:chezmoi 的 source-of-truth 渲染态 与 runtime env 是两层。
base_confidence: 0.85
provenance:
  extracted: 0.9
  inferred: 0.1
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
relationships:
  - target: "[[concepts/chezmoi-workflow]]"
    type: related_to
  - target: "[[concepts/chezmoi-templating]]"
    type: extends
  - target: "[[skills/statusline-template-injection-defense]]"
    type: derived_from
---

## 核心抽象

chezmoi 把 dotfile 当成 **source-of-truth**(源文件),而 runtime shell / 进程读的是 **rendered state**(已渲染状态)。这两层之间存在一个时间窗:

```
source-of-truth (源文件)        rendered state (env)
   ~/.local/share/chezmoi/         ~/.zsh-extend.sh
       dot_zsh-extend.sh.tmpl   →  (chezmoi apply 后)
   {{ keyring ... }} 模板         实际密钥字符串
                                    ↓
                              export MINIMAX_API_KEY=...
                                    ↓
                              下游进程读 env
```

**关键**:source-of-truth 用 `{{ keyring ... }}` 模板是合法的(密钥不入 git),但 rendered state 必须由 `chezmoi apply` 把模板替换成实际密钥字符串。**若渲染未跑,export 的 env 值就是字面模板字符串** —— 它**看起来像** env 中的一个值,下游消费者无法分辨"是模板还是真密钥"。

## 渲染态 × 注入耦合的三个易感场景

| 场景 | 触发条件 | 后果 |
|---|---|---|
| **新机器首启** | dotfile 仓库已 clone,但 `chezmoi apply` 未跑 | 任何 `export KEY={{ keyring ... }}` 都是模板字符串 |
| **dotfile 修改后** | chezmoi 源文件改了,`chezmoi apply` 还没跑(下一次 shell 启动可能错过) | 同上 |
| **chezmoi 模板语法错** | 模板变量未定义/语法错误,渲染失败但 source-of-truth 还在 | 视 chezmoi 版本行为,可能整行原样输出或空字符串 |

## 为什么难发现

1. **HTTP 200 假阳性**:上游 API 收到模板字符串当 Bearer token,通常返回 HTTP 200 但 `base_resp.status_code: 1004`(login fail) —— 不是 401/403。常规 `curl --fail` 检测不到。
2. **长度粗看合理**:模板字符串约 22 字节(`{{ keyring "x" "y" }}`),看似长度 OK。
3. **缓存层掩盖**:statusline 类的健康检查通常按 `status_code == 0` 判断缓存,1004 让"缓存失败"分支接管,UI 显示 `unavailable` 但**不报错**。
4. **env 优先级 > keychain**:statusline / CLI 工具常设计成 env-first + keychain-fallback,**只看 env 的分支就漏了 keychain 路径的诊断价值**。

## 防御原则:fail-closed + 启发式

消费者侧(statusline / API 客户端)必须假设 env **可能不可信**,即使它"看起来有值"。三层防御:

1. **结构启发式**:值含 `{{` / `}}` / 已知模板前缀 → 视为模板,清空
2. **长度启发式**:密钥长度应在合理区间(API key 通常 32+ 字节),过短或过长都可疑
3. **回环验证**:用候选 key 发一次轻量 ping(如 `/v1/user/balance` 之类只读端点),期望 HTTP 200 + `status_code == 0`,否则回退到下一个数据源

第三层最稳但需要网络往返;前两层是本地启发式,延迟为零。**组合使用**:本地启发式拦 99%,边界 case 走网络验证。

## 与 [[concepts/chezmoi-workflow]] 的关系

chezmoi 工作流把渲染放在 `apply` 阶段:

```
add → edit → diff → apply
```

"apply" 是渲染同步(source-of-truth → runtime)的唯一桥梁。env 泄漏 bug 的根因经常是 **diff 通过但 apply 漏跑**(开发者改了 dotfile,diff 看了一下觉得 OK,直接重开 shell)。在 [[concepts/chezmoi-workflow]] 的"apply 不是 optional"清单里值得加一行警告。

## 相关

- [[skills/statusline-template-injection-defense]] — 具体修复 pattern(grep `{{` + keychain 回退)
- [[concepts/chezmoi-workflow]] — chezmoi 工作流:四个动词 + 一次更新
- [[concepts/chezmoi-templating]] — chezmoi 模板语法与 `{{ keyring ... }}` 用法
- [[skills/chezmoi-keyring-template]] — `{{ keyring ... }}` 在 chezmoi 中的具体配置
- [[skills/macos-keychain-getBase64Key]] — macOS keychain 读取 + base64 解码细节
- [[entities/chezmoi]] — chezmoi 项目实体