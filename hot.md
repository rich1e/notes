---
title: Hot Cache
updated: 2026-07-27T06:25:00Z
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-07-27 06:25] INGEST github:sebastienrousseau/dotfiles.github.io — 5 页新建 + 2 页更新。Trusted Shell Platform（官网 dotfiles.io）是以 chezmoi 为核心的工程级 shell 分发版：dot CLI 53 条命令（诊断 14 条，AI 包装器 7 个），1,250+ 别名 48 类（[[concepts/shell-alias-taxonomy]]），VitePress 22 语言文档站（[[skills/vitepress-multilingual-docs]]）。新增实体 [[entities/sebastienrousseau-dotfiles]] 和 [[entities/trusted-shell-platform]]，命令参考 [[references/dot-cli-commands]]；在 [[entities/chezmoi]] 加"知名使用案例"章节，在 [[concepts/dotfile-manager]] 加工程级完整案例段落。
- [2026-07-26 10:00] INGEST Clippings batch-1 (6 files: 3 new + 3 modified) — 3 pages new, 4 pages updated, 2 pages refreshed-only. 三大主题：(A) **Zellij 终端复用器完整 skill** — 新建 [[skills/zellij-terminal-multiplexer]]。Rust 写，开箱即可用的状态栏+键位提示；YAML 布局文件 + WebAssembly 插件系统（`compact-bar` / `strider` 内置）；KDL 配置 DSL（比 tmux.conf 更结构化）；与 tmux 6 维度对比表（UI/插件/布局/学习曲线/跨平台/性能）。同步在 [[skills/tmux]] 加 `related_to` 链接。最关键的工程决策：把 `Ctrl+p`（窗格模式）改 `Alt+p` 避 Vim 冲突，KDL 配置 5 行可完成。(B) **MCP server 作用域陷阱** — 新建 [[concepts/mcp-server-protocol-quirks]] + [[skills/notebooklm-mcp-setup]]。`claude mcp add` 默认是项目级，写入 `~/.claude.json` 的 `projects.<路径>.mcpServers`；`$HOME` 不被特殊处理（与 `git config` 一致）；只有 `--global` 才落顶层 `mcpServers`。文档化两个常见坑：①在 `~/projects/foo` 下 add → 只对 foo 生效；②在 `~` 下 add → 写入 `/home/<user>` 这条路径对应的项目条目。解决：`--global` 或手动迁移 `~/.claude.json`。同步在 [[skills/claude-code-settings]] 加 "MCP servers 作用域（两层）" 章节，保持四层级 vs 两层级的对称。(C) **chezmoi + VSCode 集成** — 新建 [[skills/chezmoi-vscode-integration]]，同步更新 [[concepts/chezmoi-workflow]] 加 "编辑器与 diff 工具自定义" 章节。核心配置：`[edit] command="code" args=["--wait"]` + `[diff] command="code" args=["--wait", "--diff", "{{ .Destination }}", "{{ .Target }}"]`，`--wait` 必填（VSCode 默认非阻塞）。3 张 modified 文件（Feather / FE 序章 / NDS 回忆录）经核对已 100% 覆盖在现有实体页+journal页，仅刷新源头时间戳和 hash。source_type=document（Clipper 抓的 Web 文章）。
- [2026-07-26 04:00] WIKI_SYNTHESIZE — 5 个新合成页：①[[synthesis/concepts-mixture-of-experts × entities-kimi-k3]]（MoE 教科书 vs K3 实证的路由器/激活控制具体落点：Quantile Balancing/Per-Head Muon/SiTU/Gated MLA 把通用 MoE 的"模糊项"落实为可验证工程决策）；②[[synthesis/concepts-kimi-delta-attention × entities-kimi-k3]]（KDA 单独看是 6.3× 加速，嵌入全栈后变"长程 Agent"可行性基础 — KDA+AttnRes+MoE+QAT 缺一不可）；③[[synthesis/concepts-dotfile-manager × entities-chezmoi]]（五大流派中段定位的具体含义：Stow 太简、Nix 太繁，chezmoi 在"逐文件差异化"这块空白有产品）；④[[synthesis/concepts-chezmoi-templating × concepts-chezmoi-attribute-prefixes]]（runtime 渲染 vs 文件系统语义的互补，前缀 17 个 token 是设计哲学而非 bug）；⑤[[synthesis/concepts-ptp-clock-types × entities-white-rabbit]]（PTP 标准角色 vs CERN 工业极端实现：SyncE+PTP 双协议达成 sub-ns，WR 是"特定场景极端需求"非"通用最佳实践"）。
- [2026-07-26 03:30] LINT_CONSOLIDATE — 3 真破损修复（1 真 + 2 parser artifact）+ 10 orphans 救 11 入链。报告写入 [[synthesis/consolidation-2026-07-26]]。
- [2026-07-26 03:35] REL_FIX — 10 条 `synthesized_in` 统一改 `related_to`（concepts/entities/references/projects 跨类批量）。
- [2026-07-26 03:00] INGEST_URL https://github.com/LiveContainer/LiveContainer/issues/1456 — 新建 1 页 [[misc/web-github-com-livecontainer-issues-1456]]（LiveContainer 3.7.14 Nightly + iPadOS 26.3 下 SideStore Refresh All 报 "Unable to manage profiles on the device"）。维护者 hugeBlack 结论：iOS 26+ 必须用 RPPairing 替代旧 Lockdown 配对文件；若 iloader 不生成，用 jkcoxson 的 idevice_pair v0.1.14+ 自行生成。
- [2026-07-25 10:57] INGEST Clippings batch-0 (20 files) — 3 页新建，15 页更新。三大主题：chezmoi 9 篇教程整合 + iOS 侧载 3 篇 + 前端/工具链 7 篇。详见 [[synthesis/consolidation-2026-07-23]]。
- [2026-07-25 08:30] INGEST Clippings batch-2 (5 files) — 1 页新建（references/chezmoi-encryption-backends），5 页增量更新。
- [2026-07-25 02:27] WIKI_RESEARCH "chezmoi" — 3 轮研究完成，12 页新建。

## Active Threads

- **Trusted Shell Platform / sebastienrousseau/dotfiles（2026-07-27 新建）** — [[entities/sebastienrousseau-dotfiles]] + [[entities/trusted-shell-platform]] + [[references/dot-cli-commands]] + [[concepts/shell-alias-taxonomy]] + [[skills/vitepress-multilingual-docs]] 五件套。核心洞察：chezmoi 作为底层状态机，上面叠加 53 条命令+1250 别名构成"shell 分发版"而非"dotfile 管理器"——这是"裸 chezmoi"到产品级工具的标准演进路径。dot CLI 的"诊断类命令最多（14条）"揭示作者的可观测性优先哲学；AI 命令（`cl/gemini/kiro/ollama` 包装器）是现代 dotfile 体系的新必备。chezmoi 知识集群现通过"知名使用案例"章节与 Trusted Shell Platform 双向链接。
- **Zellij + tmux 双轨知识集群（2026-07-26 batch-1 新建）** — [[skills/zellij-terminal-multiplexer]] 和 [[skills/tmux]] 形成 tmux 友好的现代替代对照。新页提供 6 维度对比表 + 完整安装指南 + KDL 配置示例 + YAML 布局 + 浮动/堆叠窗格 + 何时选哪个的决策指南。两页已 `related_to` 互链，但仍是两个独立 skill 而非合成页（用户可能两者都用）。
- **MCP server 作用域陷阱（2026-07-26 batch-1 新建概念）** — [[concepts/mcp-server-protocol-quirks]] + [[skills/notebooklm-mcp-setup]] + [[skills/claude-code-settings]] 三个交叉点。解决了 90% 的 "MCP 装上不生效" 投诉。这条线与 [[skills/claude-code-token-optimization]] 互不直接相关，但同属 "Claude Code 用好要知道的 5 件事" 集。
- **chezmoi 完整知识集群（2026-07-25 + 2026-07-26 增量补完）** — 在 [[entities/chezmoi]] + [[concepts/chezmoi-three-state-model]] + [[concepts/chezmoi-attribute-prefixes]] + [[concepts/chezmoi-templating]] + [[concepts/chezmoi-workflow]] + [[references/chezmoi-encryption-backends]] + [[references/chezmoi-nix-darwin-integration]] + [[references/chezmoi-bitwarden-keychain]] + [[references/chezmoi-patterns-recipes]] 的 12 页研究中轴上，batch-1 加入 (10) [[skills/chezmoi-vscode-integration]]：把 `chezmoi edit` 和 `chezmoi diff` 都换成 VSCode，dotfile 体验接近 IDE。这是研究范围外的新维度（编辑器集成），未触发新合成。
- **iOS 侧载完整知识集群（2026-07-25 batch-0 增厚 + 2026-07-26 refresh）** — 在已有 [[entities/feather-ios-sideload]] + [[skills/ios-sideloading-fundamentals]] + [[skills/ios-emulator-setup]] 三件套基础上，二次摄入 Feather 源（无损对齐）、iOS 26.4 RPPairing 案例页同步入库。
- **Fourier 分析概念页（2026-07-25 batch-0 全新）** — [[concepts/fourier-series]]：Euler 公式 → 复正弦 → 本轮链 → 方/三角/锯齿波展开；与 [[concepts/animation-easing-functions]] 同属"曲线合成"但维度不同（频域 vs 时域）。
- **Kimi K3 完整知识集群（2026-07-23，官方博客已消化）** — [[entities/kimi-k3]] 权重计划 2026-07-27 发布（明天）。重点：MiniTriton 开源 + Delta Attention 独立复现 + Quantile Balancing 跨模型迁移。
- **5 new synthesis pages (2026-07-23)** — Swift×SwiftUI / pattern-categories×iOS-arch / battle-tested×GoF / iOS17-book×CS193P / Fabric×Claude Code。
- **5 new synthesis pages (2026-07-07)** — PTP×LinuxPTP / Trek auth×MCP / Zustand core×entity / ARC×Swift concurrency / macOS window switcher×reference list。
- **CS193P Swift cluster (2026-07-10)** — 3 页更新 + 1 新参考页。
- **Fabric AI cluster (2026-07-09)** — entity + concept + skill + synthesis 四页。
- **battle-tested-patterns cluster (2026-07-08)** — 46 patterns, 5 类别；与 GoF 23 模式互补。
- **PTP cluster (2026-07-03)** — 6 概念页 + linuxptp 实体 + white-rabbit 实体。
- **Trek cluster (2026-07-02)** — 8 新页，含 auth-system ↔ mcp-server 合成。
- **macOS window switcher cluster** — 4 实体 + 1 概念 + 1 合成，解释"为什么 4 个独立工具能并存"。

## Key Takeaways

- Vault 健康：105 页（3 新增）+ 55 源。`pages_updated=4 pages_created=3` 接近 10-15 目标（4+3=7 个工作单元 + 2 刷新-only），下次 batch 可考虑 12-15 张。
- MCP server 作用域的"git config 类比"是教学锚点——降低 90% 的认知负担。值得在 [[skills/claude-code-settings]] 顶部就引用。
- Zellij 的 KDL 配置比 tmux.conf 更结构化，但 Zellij 模式化键位（`Ctrl+p` 进入 pane 模式后按 `n`）需要先于 tmux 单层组合习惯建立心智模型。
- chezmoi + VSCode 是 dotfile + IDE 工具链的标准组合，但关键细节是 `--wait`（VSCode 默认非阻塞，chezmoi 会继续后续流程）。
- "modified 但内容已覆盖" 是常见的重复摄入场景——3 张 modified 文件确认无损后只刷 hash 和 updated 时间戳。

## Flagged Contradictions

*None yet.*
