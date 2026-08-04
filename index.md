---
title: Wiki Index
---

# Wiki Index

*This index is automatically maintained. Last updated: 2026-08-04T11:35:00Z*

## Concepts

- [[concepts/serverless-image-hosting]] — 无服务器图床范式：边缘 serverless 函数 + 外包对象存储（R2/S3/Telegram）+ KV/D1 元数据，成本趋零、免运维、可移植
- [[concepts/tmux-config-importance-override]] — `#!important` 后缀标记让 perl sed 阶段保留用户原文 bind/set，绕过主 conf 后写覆盖
- [[concepts/tmux-installer-safety-pattern]] — install.sh 的 5 道安全闸：拒绝 root、bash 必填、tmux 必装、PERMISSIVE+DRY_RUN、anti-piping TTY 复核
- [[concepts/tmux-key-notation-btab]] — `B<Tab>` = `<prefix> Tab`、`B<C-c>` = `<prefix> C-c`：`B` 是 prefix 占位符
- [[concepts/obsidian-wiki-vault-structure]] — obsidian-wiki 框架规定的目录布局：9 类目（concepts/entities/skills/references/synthesis/journal/projects/misc/sources）+ 4 系统文件（index.md/log.md/hot.md/.manifest.json）+ _meta/_insights/_raw 等内部目录
- [[concepts/wiki-framework-self-reference]] — Ingest 框架本源仓库（Ar9av/obsidian-wiki）时的特殊拓扑：vault 已在用此框架，直接 distill 等于重复入库，只保留 3 页索引
- [[concepts/tmux-pane-maximize-stateful]] — `<prefix> +` 比 `resize-pane -Z` 强：maximize 到专用 window 后仍可 split，跨 window 保留状态
- [[concepts/tmux-prefix-double-binding]] — `C-b`（默认）+ `C-a`（GNU Screen 兼容）双 prefix 共存，`send-prefix -2` 转发
- [[concepts/tmux-local-override-pattern]] — 主 conf 不可改、`.local` 走 `tmux_conf_*` 变量覆写、`#!important` 解决冲突
- [[concepts/ptp-ieee1588]] — IEEE 1588 精确时间协议，四时间戳法实现纳秒级分布式时钟同步
- [[concepts/ptp-bmca]] — BMCA 最佳主时钟选举算法，基于 clockClass/Accuracy/priority 分布式选举
- [[concepts/ptp-clock-types]] — PTP 四种时钟角色：GM 提供时间源，BC 转发，TC 补偿驻留延迟，OC 终端
- [[concepts/ptp-delay-measurement]] — E2E 与 P2P 四时间戳延迟测量机制
- [[concepts/ptp-tlv-extension]] — PTP TLV 插件系统，支撑 IEEE 1588-2019 向后兼容扩展
- [[concepts/ptp-message-types]] — PTP 10 种报文：事件报文（需硬件时间戳）和通用报文
- [[concepts/ptp-port-state-machine]] — PTP 端口 9 种状态，由 BMCA 结果和链路事件驱动转换
- [[concepts/llm-speculative-decoding]] — 推测解码加速 LLM 推理：草稿模型 + 并行验证，DSpark 半自回归架构
- [[concepts/prompt-caching]] — LLM 提示缓存机制，KV 缓存复用原理
- [[concepts/javascript-event-loop]] — JavaScript 事件循环：调用栈、微任务、宏任务
- [[concepts/browser-process-model]] — Chrome 多进程架构，Renderer 进程与线程模型
- [[concepts/frontend-storage-cache]] — Cookie / LocalStorage / HTTP 缓存全览
- [[concepts/mobile-timer-accuracy]] — 移动端定时器精度问题与解决方案
- [[concepts/swift-fundamentals]] — Swift 5.9 类型系统、集合、闭包、可选值、协议导向编程
- [[concepts/swiftui-framework]] — SwiftUI 声明式 UI、View 协议、状态管理（@State/@Binding/@ObservedObject）
- [[concepts/arc-memory-management]] — ARC 自动引用计数、强/弱/无主引用、循环引用解决方案
- [[concepts/swift-concurrency]] — async/await、Task/TaskGroup、Actor 数据隔离、MainActor
- [[concepts/ios-app-architecture]] — iOS 架构模式对比：MVC/MVVM/VIPER/Redux 及常见反模式
- [[concepts/zustand-core-architecture]] — Zustand createStore 约 30 行核心：闭包 + Set`<Listener>` + 浅合并，StoreApi 接口设计
- [[concepts/zustand-middleware-system]] — Zustand 中间件系统：StoreMutators 类型扩展、persist/devtools/immer/redux/subscribeWithSelector
- [[concepts/zustand-react-integration]] — Zustand React 层：useSyncExternalStore + 选择器 + useShallow 浅比较防多余重渲染
- [[concepts/macos-window-switcher]] — macOS 窗口切换器：替代 Cmd+Tab 的 app→window 粒度扩展，含 Space 过滤/标签下钻/快速动作
- [[concepts/mcp-server-protocol-quirks]] — `claude mcp add` 默认项目级，`$HOME` 不被特殊处理，`--global` 才能真正全局（与 git config 一致）；`-s user` 与 `--global` 同义
- [[concepts/design-system-as-ai-context]] — DESIGN.md 把设计系统升级为 AI 硬约束输入，避免 agent 在 padding/spacing 等设计决策上反复耗 token
- [[concepts/ai-tool-specialization]] — AI 工具栈专业化分工：让每个 agent 守一段（视觉/逻辑/数据），通过 MCP 协议级协作而非造 mega-agent
- [[concepts/design-md-format-spec]] — DESIGN.md 文件 schema：YAML tokens + 8 必备 prose 章节（awesome-design-md 扩展到 11 节）
- [[concepts/design-md-token-interpolation]] — `{path.to.token}` 引用机制：让组件保持"换主题 = 改一处"，借鉴 DTCG 2025.10
- [[concepts/design-md-anti-patterns]] — Do's and Don'ts 章节约束 "AI taste"（默认漂向 gradient/glow/emoji 的均值审美）
- [[concepts/asciidoc-markup]] — AsciiDoc 标记语言：表格/脚注/交叉引用/属性/条件内容内置，docs-as-code 友好
- [[concepts/animation-easing-functions]] — 缓动函数：Penner 缓动 + Apple 参数化运动学 + 卷积滤波 + PD/PID 反馈控制四条路线
- [[concepts/programming-pattern-categories]] — 编程模式五大分类（数据结构/并发/系统/内存/行为），按运行时职责切分，与 GoF 互补
- [[concepts/fabric-patterns]] — Fabric Patterns：290+ 可复用 AI Prompt 单元，覆盖分析/提取/创作/安全等场景
- [[concepts/mixture-of-experts]] — MoE 混合专家架构：稀疏激活降低每 token 算力，内存与算力的核心权衡
- [[concepts/kimi-delta-attention]] — Kimi Delta Attention：Moonshot 提出的长上下文 KV 缓存优化，100 万 token 下最高 6.3× 加速
- [[concepts/dotfile-manager]] — Dotfile 管理工具五大流派（裸 git/Stow/chezmoi/Nix/云同步）的设计空间与权衡
- [[concepts/shell-alias-taxonomy]] — Shell 别名分类体系：48 类 1250+ 别名的工程级组织方法
- [[concepts/chezmoi-three-state-model]] — chezmoi 三态模型：源态/目标态/实际态，`apply` 是协调三个状态的过程
- [[concepts/chezmoi-attribute-prefixes]] — chezmoi 17 个属性前缀（dot_/private_/encrypted_/modify_ 等），命名即元数据
- [[concepts/chezmoi-templating]] — chezmoi 模板系统：Go text/template + sprig 扩展，按机器差异化
- [[concepts/chezmoi-workflow]] — chezmoi 四动词工作流（add/edit/diff/apply）+ update/init + czpush/czpull/czapply 三段式别名
- [[concepts/fourier-series]] — 傅里叶分析：单位圆 + Euler 公式串联复正弦、本轮链与傅里叶级数展开
- [[concepts/llm-training-pipeline]] — 现代 LLM 训练三阶段：预训练 → SFT → RLHF/RLVR（Karpathy 2025 教科书类比）
- [[concepts/llm-learning-path]] — LLM 学习双轨（Engineer vs Scientist）+ 四阶段路径 + 时间预算
- [[concepts/rag-vs-finetuning]] — Prompt / RAG / Fine-tuning 决策矩阵：知识 vs 行为的关键区分
- [[concepts/test-time-compute]] — 2025 范式转向：推理时扩展 + RLVR（DeepSeek-R1 / OpenAI o1）
- [[concepts/mechanistic-interpretability]] — 逆向工程神经网络内部电路：SAE、induction heads、circuit discovery
- [[concepts/claude-mem-memory-architecture]] — claude-mem 记忆三段：hook 捕获 → haiku 压成 observation 存 SQLite+Chroma → 第二次会话起 SessionStart 注入
- [[concepts/claude-code-hooks-lifecycle]] — Claude Code 6 个生命周期 hook（Setup/SessionStart/UserPromptSubmit/PostToolUse/PreToolUse/Stop），claude-mem 的挂载点
- [[concepts/weak-rng-key-generation]] — 弱随机数私钥生成漏洞：私钥安全取决于随机源的熵而非算法强度，MT19937（2^32 种子空间）可暴力枚举
- [[concepts/workflow-automation-platform]] — 工作流自动化平台：节点+连线+DAG 低代码抽象，Zapier/Make/n8n 三主流对比
- [[concepts/fair-code-license]] — 受限源码可用许可：可自托管可改可商用，但禁同质竞品；代表 n8n 的 Sustainable Use License
- [[concepts/ai-agent-node-pattern]] — AI Agent 节点模式：把 LLM/工具/记忆/RAG/MCP 作为可视化一等节点
- [[concepts/agent-operating-system]] — AOS：多会话连续 AI 工作流的五层 memory 框架（Handoff/Auto/claude-mem/ADR/KB）+ compact checkpoint 模板 + 事件驱动更新
- [[concepts/transformer-architecture]] — Transformer：自注意力(Q/K/V+多头+位置编码)驱动的序列建模骨架，当代 LLM 统一底座
- [[concepts/scaling-laws]] — Scaling laws：损失随参数/数据/算力呈幂律下降，Chinchilla 指出参数与数据应等比放大
- [[concepts/instruction-tuning]] — 指令微调：预训练后用「指令-回答」SFT，把续写模型改造成听懂指令的助手
- [[concepts/ai-agent]] — AI Agent：以 LLM 为大脑、感知-规划-行动闭环、工具调用+记忆的自主系统
- [[concepts/git-worktree-pool-pattern]] — git worktree 池化复用：detached HEAD 隔离 + acquire/use/return 状态机，保留依赖/构建缓存供下一 agent 立即使用
- [[concepts/worktree-durable-lease]] — Worktree durable lease：进程无关的持久租约（128-bit LeaseID + LeaseHolder + LeasedAt），`--if-lease-id` ABA 防护条件 return
- [[concepts/atomic-state-recovery]] — 状态文件原子写（temp+fsync+rename）与 corrupt 自愈：解析失败时扫描池目录重建条目，全部默认 leased 等用户显式确认
- [[concepts/safe-destroy-by-default]] — 破坏性 CLI 默认安全设计：dry-run by default + 风险类别独立 opt-in（--include-unlanded/-in-use/-leased），拒绝 blanket --force
- [[concepts/ai-agent-sandbox]] — AI 编码 agent 的工作树隔离：多 agent 并行写同一仓库所需的 acquire/lease/cache/safe-delete 五件套
- [[concepts/static-analysis-knowledge-graph]] — 用图算法(import/call/types/tests/IaC/spec)替代 embedding 做代码检索与定位，确定性 + 可重放 + 可追 Evidence
- [[concepts/deterministic-agent-memory]] — 确定性 agent 记忆：同问题同答案、stale 显式标注、引用可点回源码、与概率型 claude-mem 互补
- [[concepts/no-llm-hot-path]] — Hot path 不放 LLM：确定性算法跑 hot,LLM 只在 generate/verify/consolidate 等 cold path opt-in
- [[concepts/commit-gate-guardrails]] — Commit gate guardrails:drift(代码改了 spec 没改)+ decisions(决策未经人审)+ check_architecture(编辑时 layer 校验)三类独立 opt-in

## Entities

- [[entities/cloudflare-imgbed]] — 开源自托管图床（MarSeventh，MIT）：Serverless+Docker 双部署、六大存储后端、Vue 3 前端，脱胎自 Telegraph-Image
- [[entities/sanyue-imghub]] — CloudFlare ImgBed 的前端仓库（Vue 3 + Element Plus），前后端分离可独立换皮
- [[entities/feather-ios-sideload]] — iOS 付费开发者签名工具 Feather
- [[entities/nds-flashcard]] — NDS 烧录卡（R4 / DSTWO）使用指南
- [[entities/neogeo-mame]] — NEOGEO / MAME 模拟器配置
- [[entities/ique-dsi]] — 神游 DSi（iQue DSi）主机，型号 TWL-001(CHN)，双摄/Wi-Fi/内置软件
- [[entities/nintendo-wansui]] — iQue DSi 内置任天狗狗虚拟宠物游戏
- [[entities/ios17-app-development-book]] — iOS 17 App Development for Beginners（书籍），Arpit Kulsreshtha 著，Swift 5.9/SwiftUI/Xcode 15
- [[entities/zustand]] — Zustand：pmndrs 出品的轻量 React 状态管理库，无 Provider，Hook 驱动，~1KB
- [[entities/linuxptp]] — Linux 平台工业级 PTP 实现，包含 ptp4l/phc2sys/pmc 工具
- [[entities/white-rabbit]] — CERN 开发的亚纳秒级时间同步协议，PTP 扩展 + DMTD 相位测量
- [[entities/alttab]] — AltTab：lwouis 出品的开源 macOS 窗口切换器，悬停顶层预览 + 21 语言
- [[entities/bettercmdtab]] — BetterCmdTab：rokartur 出品的永久免费开源 Cmd+Tab 替代，macOS 13+
- [[entities/contexts]] — Contexts：边栏式 macOS 窗口切换器，触控板边缘下滑手势 + 多显示器独立边栏
- [[entities/witch]] — Witch：Many Tricks 出品的付费窗口切换器，多粒度切换器并存
- [[entities/battle-tested-patterns]] — Totoro-jam 出品的开源 46 模式目录项目（React/Linux/Go/PostgreSQL 等代码级编程模式，行号精确引用）
- [[entities/fabric-ai]] — Fabric：danielmiessler 出品的开源 AI 增强框架，290+ Patterns，20+ AI 提供商，Go 编写
- [[entities/kimi-k3]] — Kimi K3：全球首个 3T 级开权重 LLM（2.8T 参数，MoE），代码评测第一，2026-07-27 发布
- [[entities/moonshot-ai]] — Moonshot AI（月之暗面）：Kimi 品牌开发商，K 系列超大规模模型，架构创新应对算力限制
- [[entities/chezmoi]] — chezmoi：twpayne 维护的跨平台 dotfile 管理工具，单 Go 二进制，三态模型 + 模板 + 加密
- [[entities/sebastienrousseau-dotfiles]] — Trusted Shell Platform：chezmoi + dot CLI(53条) + 1250+ 别名的完整 shell 分发版
- [[entities/google-stitch]] — Google Labs AI 设计工具（Gemini 2.5 Pro 驱动），输出 DESIGN.md 设计系统 + 结构化 HTML/CSS，可通过 MCP 与 Claude Code 协作
- [[entities/obsidian-wiki-framework]] — GitHub 仓库 Ar9av/obsidian-wiki — 本 vault 使用的 SKILL-based Obsidian 知识库框架，39 个 markdown skill + Python CLI + Chrome 捕获扩展，源自 Karpathy LLM Wiki gist
- [[entities/Ar9av]] — obsidian-wiki 框架作者（GitHub @Ar9av / X @_ar9av），MIT 协议，PyPI 包名 `obsidian-wiki`
- [[entities/gpakosz-tmux]] — gpakosz 自 2012 年维护的 tmux 配置（Oh my tmux!）：Powerline 主题、双 prefix、`<prefix> +` 跨 window maximize、`.local` 覆写层、WTFPLv2+MIT 双协议
- [[entities/claude-code]] — Anthropic 终端式 AI 编码 agent，承担逻辑与组件架构，通过 MCP 接外部服务、通过提示缓存控制 token
- [[entities/google-labs-code-design]] — Google Labs 官方 DESIGN.md 规范仓库 + @google/design.md CLI（26.5K stars、Apache-2.0）
- [[entities/awesome-design-md]] — VoltAgent 团队维护的 74 个真实站点 DESIGN.md 精选集（105K stars）
- [[entities/voltagent]] — awesome-design-md 仓库与 getdesign.md 目录服务的运营组织
- [[entities/trusted-shell-platform]] — Trusted Shell Platform 平台理念：幂等、声明式、跨平台 shell 环境分发
- [[entities/gnu-stow]] — GNU Stow：symlink 农场式 dotfile 管理器，最简镜像流派代表
- [[entities/andrej-karpathy]] — Andrej Karpathy：Zero to Hero / nanoGPT / nanochat 作者，LLM 教育事实标准制定者
- [[entities/sebastian-raschka]] — Sebastian Raschka：《Build a Large Language Model (From Scratch)》作者，工程化 PyTorch 路线
- [[entities/li-hongyi]] — 李宏毅：台大教授，中文 ML/GenAI 课程主讲，2025《生成式AI导论》
- [[entities/claude-mem]] — claude-mem：thedotmack 出品的 Claude Code 长期记忆插件（Apache-2.0），hook 驱动，本地 SQLite+Chroma
- [[entities/n8n]] — n8n-io/n8n：fair-code 工作流自动化平台，TypeScript，2.0 起原生 multi-agent + MCP + Data Tables
- [[entities/czlonkowski-n8n-mcp]] — czlonkowski/n8n-mcp：把 n8n API 暴露为 MCP server，让 Claude/Windsurf/Cursor 用自然语言搭 workflow
- [[entities/zapier]] — Zapier：纯云无代码工作流自动化 SaaS，集成数量业界最多，n8n/Make 竞品
- [[entities/make]] — Make（原 Integromat）：纯云工作流自动化 SaaS，可视化 scenario 画布最强
- [[entities/treehouse]] — treehouse：kunchenguid 出品的 AI agent 并行 worktree 池 CLI（Go v2.1.1），无守护进程，durable lease + 原子 state 自愈 + safe-by-default destroy
- [[entities/openlore]] — OpenLore：clay-good 出品的 AI agent 静态分析记忆层（TypeScript v2.1.x），hot path 0 LLM，MCP 73 tools / 6 capability family，substrate 默认 13 tools，commit gate + 架构不变量 guardrail

## Skills

- [[skills/stitch-upload-design-md]] — Stitch DESIGN.md 上传操作技巧（含 Auto Mode 凭证检测问题解法）
- [[skills/claude-code-token-optimization]] — Claude Code Token 优化策略（提示缓存 + 会话管理）
- [[skills/claude-code-settings]] — Claude Code 四级配置作用域与权限系统
- [[skills/ios-sideloading-fundamentals]] — iOS 证书类型、JIT 原理、SideStore/LiveContainer 机制完整解析
- [[skills/ios-emulator-setup]] — iOS 上的 3DS（ManicEMU）与 Switch（MeloNX）模拟器安装与 JIT 配置
- [[skills/hackintosh-mini-build]] — 5000 元黑苹果小机箱（对标 Mac Studio），程序员装机指南
- [[skills/tmux]] — Tmux 快捷键速查、推荐配置、关闭会话的 4 种替代方式（kill-server / kill-session -a / :kill-session / exit 级联）
- [[skills/tmux-gpakos-config]] — gpakosz/.tmux 实战：安装（自动/手动/XDG）、热重载、`.local` 定制、Powerline 字体、TMUX_CONF_LOCAL env、卸载
- [[skills/terminal-music]] — macOS 终端本地音乐播放（afplay + shell 函数）
- [[skills/ique-dsi-camera]] — iQue DSi趣照 11种趣味相机、相册、幻灯片、照片管理完整操作
- [[skills/ique-dsi-sound]] — iQue DSi趣音 麦克风录音、声音变换、SD卡 AAC 音乐播放
- [[skills/ique-dsi-wifi-setup]] — iQue DSi Wi-Fi 四种联网方法（AOSS/搜索/USB/手动/WPS）
- [[skills/ique-dsi-parental-control]] — iQue DSi 亲子管理设置、可限制功能、密码找回
- [[skills/pictochat]] — PictoChat 涂鸦聊天最多16人，绘图工具与键盘操作
- [[skills/ique-ds-download-play]] — iQue DS 下载游戏 1台对多台无线游戏广播
- [[skills/xcode-ide-guide]] — Xcode 15 界面布局、快捷键、模拟器、Playground、Organizer、Xcode Cloud
- [[skills/ios-data-persistence]] — UserDefaults/Plist/SQLite/Core Data/SwiftData CRUD 完整指南
- [[skills/ios-networking]] — URLSession/Alamofire REST 请求、JSON 解码、连接可达性检测
- [[skills/ios-multithreading]] — GCD 三种队列、QoS 优先级、DispatchGroup、NSOperation
- [[skills/ios-app-store-publishing]] — 证书/Identifier/Profile 创建、Archive 打包、App Store Connect 配置、TestFlight
- [[skills/zustand-patterns]] — Zustand 最佳实践：Slices、Flux 模式、外部 actions、重置状态、Map/Set、URL 同步
- [[skills/zustand-ssr-nextjs]] — Zustand Next.js SSR：per-request store 工厂函数 + Context Provider 模式
- [[skills/zustand-typescript]] — Zustand TypeScript：双括号语法原因、Slices 类型、中间件组合类型
- [[skills/ptp-implementation]] — ptp-lite 约 1000 行 C 实现：报文编解码、主时钟发布、从时钟偏移计算
- [[skills/ptp-troubleshooting]] — PTP 故障排查：pmc 诊断工具、日志解读、常见问题处理
- [[skills/pattern-study-method]] — 用 battle-tested-patterns 系统学习 46 模式：4 阶段路径 + 配套练习 + AI 编程助手技能（adopt-pattern/audit-pattern）
- [[skills/fabric-usage-patterns]] — Fabric CLI 高频用法：YouTube 分析、Shell 别名、REST API、Obsidian 集成
- [[skills/gitingest-token-error]] — gitingest 即便拿到合法 40 字 PAT 仍报 Invalid format，回退路径是 unset + 走公开仓库 git clone，根因未确认
- [[skills/chezmoi-bitwarden-secrets]] — chezmoi Bitwarden 密钥注入 + 跨平台 Keychain/DPAPI 自动解锁 + git-filter-repo 历史清理
- [[skills/vitepress-multilingual-docs]] — VitePress 22 语言文档站：SEO/PWA/无障碍/多语言同步策略
- [[skills/chezmoi-vscode-integration]] — chezmoi edit/diff 配 VSCode（`code --wait` + `--diff`），dotfile 体验接近 IDE
- [[skills/zellij-terminal-multiplexer]] — Rust 终端复用器，状态栏 + 提示键开箱即用，YAML 布局 + WebAssembly 插件
- [[skills/notebooklm-mcp-setup]] — NotebookLM MCP 完整安装：uv + cookbook auth + `claude mcp add --global`，23 个笔记本手工验证可读
- [[skills/claude-code-mcp-auth-patterns]] — Claude Code MCP 两种鉴权范式：API key 头（轻量 5 分钟）vs OAuth Proxy（重度自动 refresh），含 `.env` 干扰 OAuth 的故障清单
- [[skills/claude-mem-memory-usage]] — 在 Claude 中用 claude-mem 管长期记忆：插件市场装（别用 npm -g）→ 自动注入 → search/timeline/get_observations 3 层查历史 → /knowledge-agent 知识大脑 → settings 调优
- [[skills/treehouse-cli]] — treehouse CLI 日常用法：install/get/enter/return/prune/destroy 速查，ABA-safe 条件 return，损坏 state 恢复流程
- [[skills/openlore-cli]] — OpenLore CLI 日常用法：install/orient/review/prove/enforce/mcp/drift,6 capability family,substrate preset 默认,commit gate 三件套

## Synthesis

- [[synthesis/Research: chezmoi]] — chezmoi 3 轮研究综合：三态模型 + 17 前缀 + Go 模板 + age/GPG + 四动词工作流
- [[synthesis/concepts-fourier-series × concepts-animation-easing-functions]] — 频域合成(傅里叶/本轮链)与时域参数化(缓动函数)的正交关系,两条路线控制维度不同
- [[synthesis/references-mechanical-watch-mechanics × concepts-animation-easing-functions]] — 摆轮+擒纵是 PD 反馈控制器的物理实现,游丝=K_p,阻尼=K_d,与 spring 动画同源
- [[synthesis/skills-hackintosh-mini-build × concepts-macos-window-switcher]] — 两个 macOS 用户的"模块化替代默认"范式,软件/硬件两侧的同构工匠精神

## Projects

- [[projects/dayfold/dayfold]] — 暖色风格 iOS 日记 App（SwiftUI + Core Data/CloudKit + MapKit + WeatherKit）+ Stitch 设计系统（暖灰深夜阅读室风格）
- [[projects/dayfold/concepts/architecture-overview]] — 抽屉式根容器 + MVVM + 共享 CoreDataStack 单例
- [[projects/dayfold/concepts/core-data-cloudkit-fallback]] — CloudKit 134400 降级本地存储实现
- [[projects/dayfold/concepts/swiftui-context-propagation]] — sheet/cover 必须显式注入 managedObjectContext
- [[projects/dayfold/concepts/fetchrequest-vs-observedobject]] — 列表增删 vs 行内属性刷新的两套机制
- [[projects/dayfold/concepts/drawer-architecture]] — 85% 屏宽抽屉 + 0.38/0.82 弹簧贯穿全 App
- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]] — imagesChanged 脏标记避免 MediaAsset 误删
- [[projects/dayfold/skills/soft-delete-with-trash]] — deletedAt 时间戳 + FetchRequest predicate 隔离
- [[projects/dayfold/skills/warm-theme-tokens]] — Color.warmPaper / Font.warmHeadline / .warmCard() 视觉 token
- [[projects/dayfold/skills/swipe-to-delete-row]] — 自定义左滑删除 + 速度阈值 + 圆角并入
- [[projects/dayfold/references/source-tree]] — 源码目录布局与各模块职责
- [[projects/dayfold/references/stitch-design-system]] — Stitch 设计系统资产索引（Project ID、Asset ID、已生成屏幕、本地文件布局）
- [[projects/xk-ai-talk-desk-ui/xk-ai-talk-desk-ui]] — AI 外呼热转坐席前端（React 19 + JsSIP + 信科 CC SDK）
- [[projects/xk-ai-talk-desk-ui/concepts/call-center-sdk-integration]] — CC SDK 集成：useSoftbar Hook 封装 LaihuAPI
- [[projects/xk-ai-talk-desk-ui/concepts/agent-state-machine]] — 坐席状态机（agentState + callState 双层设计）
- [[projects/xk-ai-talk-desk-ui/skills/phonebar-call-flow]] — PhoneBar 热转/外呼完整通话流程
- [[projects/jrfed-zaxd-mediation-tool/jrfed-zaxd-mediation-tool]] — 金融客服协谈助手 Chrome 扩展（MV3 + React + Zustand + Antd）
- [[projects/jrfed-zaxd-mediation-tool/concepts/permission-system]] — 菜单/按钮/浮窗三级权限管控，usePermission Hook
- [[projects/jrfed-zaxd-mediation-tool/concepts/chrome-extension-architecture]] — MV3 三层架构与 Content Script 双世界注入策略
- [[projects/jrfed-zaxd-mediation-tool/skills/zustand-chrome-storage]] — Zustand persist + chromeStorage 适配器（禁止 localStorage）
- [[projects/jrfed-zaxd-mediation-tool/skills/sensorsdata-dual-world]] — 神策 SDK world:MAIN 注入方案
- [[projects/jrfed-zaxd-mediation-tool/references/source-tree]] — 源码目录布局
- [[projects/trek/trek]] — Trek 自托管实时协同旅行计划器（NestJS + React + SQLite + MCP）
- [[projects/trek/concepts/architecture-overview]] — Monorepo 架构，NestJS 模块化后端 + React SPA + 单容器部署
- [[projects/trek/concepts/addon-system]] — 管理员可切换的插件系统（Lists/Costs/Collab/Atlas/Journey/MCP 等）
- [[projects/trek/concepts/mcp-server]] — 内置 MCP 服务器，OAuth 2.1，150+ 工具，27 个 scope
- [[projects/trek/concepts/realtime-sync]] — WebSocket Room 模型广播 + MutationQueue 离线同步
- [[projects/trek/concepts/auth-system]] — JWT + OIDC + WebAuthn Passkeys + TOTP MFA + OAuth 2.1
- [[projects/trek/references/database-schema]] — SQLite 表结构（users/trips/days/places/addons 等）
- [[projects/trek/references/environment-variables]] — 全量环境变量配置参考

## References

- [[references/mechanical-watch-mechanics]] — 机械表七大部件与能量链原理速查
- [[references/ique-dsi-menu-software]] — iQue DSi 所有内置软件图标一览及软件位置移动方法
- [[references/ique-dsi-system-settings]] — iQue DSi 主机设置四页全部选项（软件管理/亮度/用户信息/亲子管理/互联网）
- [[references/ique-dsi-wifi-glossary]] — iQue DSi 网络术语表（SSID/WEP/WPA/AOSS/WPS等）
- [[references/ique-dsi-shop]] — iQue DSi 商店与 iQue 点数购买、充值、限制说明
- [[references/ios-design-patterns]] — GoF 23 种设计模式速查（创建/结构/行为）+ iOS 常见反模式清单
- [[references/ptp-book-overview]] — PTP技术书（Lularible），41节从思想实验到 LinuxPTP 源码到 ptp-lite 实现
- [[references/macos-window-switchers]] — macOS 窗口切换器对比速查：AltTab / BetterCmdTab / Contexts / Witch 在许可证/macOS 兼容/布局/触发方式上的差异
- [[references/pattern-catalog-battle-tested-patterns]] — battle-tested-patterns 46 模式完整目录（数据结构/并发/系统/内存/行为），每条带"Proven In"精确行号链接
- [[references/cs193p-spring-2025]] — Stanford CS193P Spring 2025 课程参考：Paul Hegarty 主讲，6周叙事式 + 5次作业 + 3周自选项目，SwiftUI 核心课
- [[references/chezmoi-official-site]] — chezmoi.io 官方首页：五大特性 + 单命令引导 + 当前版本
- [[references/dot-cli-commands]] — dot CLI 53 条命令完整参考（Core/Diagnostics/Security/AI/Secrets 等 8 类）
- [[references/chezmoi-templating-guide]] — 官方模板权威说明：Go text/template + sprig + 内置/数据/config 变量来源优先级
- [[references/chezmoi-source-state-attributes]] — 17 个属性前缀 + 2 个后缀的完整参考
- [[references/chezmoi-workflow-discussion]] — GitHub Discussions #2673：v3 方向 + 一周上手 + 七大常见坑
- [[references/chezmoi-encryption-backends]] — chezmoi 加密三后端实操：GPG（非对称/对称）、Gnome Keyring（Linux+macOS Keychain）、KeePassXC（数据库化）
- [[references/chezmoi-bitwarden-keychain]] — Bitwarden 模板注入密钥 + macOS Keychain / Windows DPAPI 免手输主密码 + git-filter-repo 历史清理
- [[references/chezmoi-nix-darwin-integration]] — chezmoi + nix-darwin 分层组合：用户级配置 + 系统级声明，.chezmoidata.yaml profile + Justfile 维护命令
- [[references/chezmoi-patterns-recipes]] — chezmoi 社区实战模式集：安装矩阵、文件名前缀、跨平台变量、加密矩阵、4 种 run_* 钩子、.chezmoiroot/.chezmoiignore 协作
- [[references/kimi-k3-technical-overview]] — Kimi K3 技术深度分析：2.8T MoE、Delta Attention、QAT、基准、定价
- [[references/kimi-k3-geopolitical-context]] — Kimi K3 地缘政治与市场背景：HBM 限制、算力绕过策略、DeepSeek 类比
- [[references/kimi-k3-video-review-lingdu]] — 零度解说实测视频：DeepSWE/LiveBench 基准、虚拟机 Agent 演示、3D 生成、越狱
- [[references/kimi-k3-video-analysis-reportify]] — 哈佛老徐深度分析：Kimi 官方原文、Anthropic Fable-5 禁令、国产芯片全球化路径
- [[references/kimi-k3-official-blog]] — Kimi K3 官方发布博客：代码案例（MiniTriton/芯片设计）、知识工作、Stable LatentMoE 组件、完整基准表
- [[references/cve-2023-39910]] — Libbitcoin Explorer（bx）弱种子漏洞：`bx seed` 用 MT19937（2^32 熵）生成钱包种子，私钥可被 GPU 暴力枚举
- [[sources/andrej-karpathy-zero-to-hero]] — Karpathy「Neural Networks: Zero to Hero」8 讲视频 + notebooks，从 micrograd 到 GPT
- [[sources/sebastian-raschka-llms-from-scratch-book]] — Raschka Manning 2024 书 + GitHub 仓库：PyTorch 实现 GPT 全流程
- [[sources/stanford-cs336-spring2025]] — Stanford CS336 (Hashimoto & Liang) Spring 2025：5 作业 + 19 讲座，数据/架构/系统/对齐全覆盖
- [[sources/li-hongyi-genai-2025]] — 李宏毅 2025《生成式AI导论》13 讲：中文母语零基础友好
- [[sources/dakingrai-mech-interp-papers]] — 机制可解释性论文清单（配 arXiv:2407.02646 综述）：Techniques/Evaluation/Findings/Tools 四分组
- [[sources/n8n-github-repo]] — n8n-io/n8n GitHub 仓库：198.7K stars，TypeScript，双许可（Sustainable Use + Enterprise），1500+ 集成
- [[sources/n8n-official-home]] — n8n.io 官方主页：500+ 商业集成、Microsoft/NVIDIA/Meta 企业客户、SOC 2/GDPR 合规
- [[sources/n8n-queue-mode]] — docs.n8n.io Queue Mode 文档：main/webhook/worker 三角色解耦、Redis BullMQ + Postgres 生产架构
- [[sources/czlonkowski-n8n-mcp]] — czlonkowski/n8n-mcp：npx 一行配置，让 Claude 用自然语言搭 n8n workflow
- [[sources/n8n-2-0-release]] — n8n 2.0（2025-12）：multi-agent 编排 + MCP client/server 一等节点 + 内建 Data Tables
- [[sources/cloudflare-imgbed-github]] — MarSeventh/CloudFlare-ImgBed 主仓库：Serverless+Docker 双部署、多存储后端、MIT
- [[sources/cloudflare-imgbed-docs]] — CloudFlare ImgBed 官方文档站：完整能力清单 + 架构（Vue 3/Hono/KV·D1/PBKDF2）
- [[sources/telegraph-image-github]] — cf-pages/Telegraph-Image 上游：Cloudflare Pages + Telegram Bot API 免费图床，其局限催生 ImgBed

## Synthesis

- [[synthesis/ptp-ieee1588 × linuxptp]] — PTP 协议理论 × LinuxPTP 工业实现：协议 vs 实现的工程空白（PI 伺服、PHC 桥接、硬件时间戳三级精度）
- [[synthesis/trek-auth-system × trek-mcp-server]] — Trek 认证 × MCP 服务器：AI 客户端的认证特化（受众绑定、scope 切分、级联吊销、插件边界）
- [[synthesis/zustand-core-architecture × zustand]] — Zustand 内部架构 × 库品牌：30 行不是省略，是有意暴露（vanilla 闭包 vs React 包装）
- [[synthesis/arc-memory-management × swift-concurrency]] — ARC × Swift Concurrency：同一引用类型的两种正交安全机制（生命周期 vs 访问安全）
- [[synthesis/macos-window-switcher × macos-window-switchers]] — macOS 窗口切换器 概念 × 对比：4 款独立工具为何解决同一问题（结构性局限）
- [[synthesis/consolidation-2026-07-07]] — 2026-07-07 自动合并报告（wiki-lint --consolidate）：PTP 反斜杠修复、chapter1 孤儿拯救
- [[synthesis/Research: Fabric AI Framework]] — Fabric AI 框架研究综合：Patterns 设计哲学、290+ Pattern 分类、多提供商架构、REST API
- [[synthesis/consolidation-2026-07-23]] — 2026-07-23 自动合并报告（wiki-lint --consolidate）：21 个破损链接修复、6 个孤儿救援、4 个 Fabric lifecycle 修复、8 个 tag 规范化
- [[synthesis/consolidation-2026-08-04]] — 2026-08-04 自动合并报告（wiki-lint --consolidate）：13 处 xk-ai-talk-desk-ui wikilink 双前缀断链修复、4 个孤儿救援、6 处 bad_type 关系（example_of/documented_by → related_to）
- [[synthesis/swift-fundamentals × swiftui-framework]] — Swift 类型系统是 SwiftUI 的运行时：函数式/POP 范式如何构成 SwiftUI DSL 的基础
- [[synthesis/programming-pattern-categories × ios-app-architecture]] — 代码级五分类 × iOS 架构模式：横切面 vs 纵切面，三层模式语言覆盖不同粒度
- [[synthesis/battle-tested-patterns × ios-design-patterns]] — GoF 对象模式 × battle-tested 代码模式：两套语言的坐标轴，组合使用才能覆盖两个维度
- [[synthesis/ios17-app-development-book × cs193p-spring-2025]] — 书（地图）× 课（罗盘）：两条 iOS/SwiftUI 学习路径的互补结构
- [[synthesis/fabric-patterns × claude-code-settings]] — Fabric Patterns × Claude Code 配置：AI Unix 管道哲学在 Prompt 层与工具层的平行实践
- [[synthesis/Research: Kimi K3]] — Kimi K3 研究综合：3T 级 MoE、Delta Attention、代码第一、整体接近 Fable 5，2026-07-27 权重发布
- [[synthesis/concepts-mixture-of-experts × entities-kimi-k3]] — MoE 通用架构 × K3 首个 3T 实证：K3 用 Quantile Balancing/Per-Head Muon/SiTU/Gated MLA 重塑路由器与激活控制
- [[synthesis/concepts-kimi-delta-attention × entities-kimi-k3]] — KDA × K3：单点注意力创新嵌入全栈后变成「长程 Agent」系统基础
- [[synthesis/concepts-dotfile-manager × entities-chezmoi]] — dotfile 五大流派 × chezmoi：中段定位的具体含义（比 Stow 复杂、比 Nix 简单、专注跨机器差异化）
- [[synthesis/concepts-chezmoi-templating × concepts-chezmoi-attribute-prefixes]] — chezmoi 两条核心机制：模板（runtime 内容差异化）vs 命名前缀（文件系统语义元数据）
- [[synthesis/concepts-ptp-clock-types × entities-white-rabbit]] — PTP 四种时钟角色 × White Rabbit 工业实现：sub-ns 精度 + SyncE + 大量 TLV 扩展
- [[synthesis/Research: 学习AI大模型]] — LLM 学习系统化路径 3 轮研究综合：双轨 + 四阶段 + 三大资源坐标系 + 2025 Test-Time Compute 转向
- [[synthesis/Research: claude-mem 长期记忆]] — claude-mem 研究综合：hook 驱动 capture→compress→inject 流水线，本地 SQLite+Chroma，第二次会话起注入，3 层检索省 10× token，本地免费/上云付费
- [[synthesis/Research: n8n]] — n8n 三轮调研综合：fair-code 开源工作流自动化平台，2.0 升 multi-agent + MCP + Data Tables，Queue Mode 成熟生产方案
- [[synthesis/Research: CloudFlare ImgBed]] — CloudFlare ImgBed 三轮调研综合：MIT 开源自托管图床，Serverless+Docker 双部署，六存储后端，脱胎自 Telegraph-Image 并补足其单后端/配额局限
- [[synthesis/Research: treehouse]] — treehouse 研究综合：把 git worktree 池化成 AI agent runtime 的 5 条独立但勾连的设计线（池化、dead agent 终止、lease、safe-destroy、crash-safe + 自愈）与 3 条可复用原则
- [[synthesis/Research: OpenLore]] — OpenLore 研究综合:静态分析驱动的代码知识图谱 + 确定性 fact layer + hot path 0 LLM + 编辑时架构 guardrail + commit gate,4 条设计线 + 4 条可复用原则,与 claude-mem/treehouse 形成 agent 本地基础设施三件套
- [[synthesis/concepts-agent-operating-system × concepts-ai-agent]] — AOS 五层 memory 框架 × agent 通用:框架对 agent 是约束还是赋能,五层中谁是 agent 自驱谁是框架强加
- [[synthesis/concepts-mcp-server-protocol-quirks × entities-google-stitch]] — MCP 鉴权三层 + Stitch 实战:协议层故意简洁,鉴权复杂度甩给上层应用,OAuth proxy 对 .env 敏感
- [[synthesis/concepts-agent-operating-system × concepts-ai-agent-sandbox]] — AOS 必须把 sandbox 当作隐式第六层:compact checkpoint 应包含 sandbox state(worktree path / HEAD / lease / dirty),否则 session resume 会撕裂
- [[synthesis/concepts-agent-operating-system × concepts-worktree-durable-lease]] — Durable lease 让 AOS Handoff 有了"原子承诺"语义:--if-lease-id 把"我是上次那个人"写成状态文件 CAS,防止多人续写 Handoff 时撕裂

## Misc

- [[misc/web-adamchanadam-github-io-agent-handoff-kit]] — Adam Chan 的 npm 工具 Agent Handoff Kit(v0.3.56):一句 init 铺好交接文件 + 分任务工作规则包,让本地 AI agent(Claude Code/Codex/Gemini CLI 等)跨会话「开工/收工」接力,高风险操作强制预演+确认;是 [[concepts/agent-operating-system]] Handoff 层的工具化落地
- [[misc/web-zhuanlan-zhihu-com-p-2013213227740325799]] — 知乎「技术极简主义」文章：Claude Code 两层项目记忆机制,CLAUDE.md（开发者手写规则,四级作用域）+ MEMORY.md/Auto Memory（Claude 自维护,200 行限制、按需加载主题文件）,含 @ 导入、.claude/rules/ 模块化、子智能体记忆
- [[misc/web-github-com-livecontainer-issues-1456]] — SideStore 内置 Refresh All 触发 Unable to manage profiles on the device（LiveContainer 3.7.14 Nightly + iPadOS 26.3）；维护者结论：iOS 26+ 必须用 RPPairing 替代旧 Lockdown 配对文件
- [[misc/web-medium-com-devsecops-ai-how-google-stitch-claude-codes-mcp-integration]] — Google Stitch + Claude Code MCP 协作实操：两种鉴权路径（API key header vs OAuth proxy），`-s user` 等价 `--global`，`.env` 文件干扰 OAuth 的故障清单
- [[misc/web-brainz-fun-bitcoin-seizure]] — brain-zhang 博文：美国政府大额比特币没收案不是攻破密码算法，而是利用弱私钥生成漏洞（MT19937/CVE-2023-39910），以 2025 DOJ 没收陈志/太子集团 12.7 万 BTC 为中心案例
- [[sources/awesome-design-md-repo]] — VoltAgent/awesome-design-md：74 个真实站点 DESIGN.md（Claude / Vercel / Notion / Stripe 等）的 inspired interpretation
- [[sources/google-design-md-spec]] — google-labs-code/design.md：DESIGN.md 官方格式规范 + `@google/design.md` CLI（lint / diff）
- [[sources/stitch-design-md-docs]] — Stitch 官方 DESIGN.md 文档（JS-rendered SPA，机器读不到正文）
- [[sources/getdesign-md-marketplace]] — getdesign.md：VoltAgent 运营的 DESIGN.md 目录与私人订制服务
- [[synthesis/Research: DESIGN.md 工作流]] — DESIGN.md 三轮研究综合：Google Labs 规范 + VoltAgent 74 个真实样本 + Stitch 自动产出 + Claude Code MCP 集成

## Journal

- [[journal/fire-emblem-new-mystery-prologue]] — FE 新·黑暗龙序章四部分攻略
- [[journal/fire-emblem-mystery-chapter1]] — FE 新·黑暗龙第1章攻略：マルスの旅立ち
- [[journal/nds-flashcard-memories]] — NDS 世代烧录卡横评回忆录
