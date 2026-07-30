# 开发者知识库规范（LLM Wiki + Obsidian）

## 设计目标

- **单一信息源**：所有知识和资料汇聚于统一的知识库，避免信息碎片化和重复。
- **AI 优先**：利用大语言模型辅助知识提炼、关联和复用，提高效率与质量。
- **增量更新**：支持持续、渐进式的知识积累与优化，保证知识库的动态活力。
- **自动化驱动**：通过自动化流程和钩子，实现资料采集、处理、更新和复盘的闭环管理。

## 整体架构

```
信息采集（Information Collection）
          │
          ▼
   _raw/ / buckets/ / Clippings/
          │
          ▼
知识加工（Knowledge Processing）
          │
          ▼
知识库（Knowledge Base）
          │
          ▼
知识检索（Retrieval）
          │
          ▼
知识复盘（Review）
```

## Vault 目录规范

```
_raw/                    # 暂存区，粗略笔记落地后由下次 ingest 升级
_staging/                # 分段写入暂存目录
_archives/               # 历史归档资料
assets/                  # 附件和图片资源
buckets/                 # 杂项资料分类存放（books/daily/finance/learn/travel 等）
Chronicle/               # 按年份归档的历史记录（2021–2026）
Clippings/               # 网页裁剪内容
concepts/                # 抽象概念、模式、心智模型
Dashboard/               # Obsidian 仪表板页面
entities/                # 具体事物（人物、工具、库、公司）
journal/                 # 时间性条目，每日日志、会话笔记
projects/                # 项目同步页面（每个项目一页）
references/              # 规范、API、配置等参考资料
skills/                  # 技能知识、操作技巧
synthesis/               # 跨概念综合分析
index.md                 # 主索引，所有页面汇总，持续更新
log.md                   # 时序活动日志（ingest、更新、lint）
hot.md                   # 会话热缓存，近期活动的语义快照（约 500 词）
.manifest.json           # 跟踪每个已导入来源：路径、时间戳、生成页面
```

## 资料采集规范

- **Thino**：日常便签和快速记录。
- **Obsidian Web Clipper**：网页内容裁剪，保存翔实且有趣的信息。
- **Buckets**：杂项资料的临时存放区，内容多样。
- **GitHub**：代码仓库、README、发布说明等技术文档。
- **PDF**：论文、白皮书等格式文档。
- **AI Chats**：与 AI 交互产生的知识和灵感。

## 知识加工流程

1. **Ingest（导入）**：将原始资料导入知识库，格式标准化。
2. **Summarize（摘要）**：提炼核心内容，生成简明扼要的摘要。
3. **Split（拆分）**：将长文档或复杂内容拆分成多个主题明确的笔记。
4. **Link（关联）**：建立笔记间的 Wiki Link，形成网络化知识结构。
5. **Taxonomy（分类）**：添加标签和分类，规范知识体系。
6. **Publish（发布）**：将处理好的知识推送至主知识库目录，供检索和复盘使用。

## 知识体系构建命令

### 导入

- `/wiki-ingest` 导入文档、PDF、Markdown 等资料
- `/wiki-history-ingest` 导入历史聊天记录（Claude / Codex / Pi / OpenClaw 等）
- `/github-ingest` 分析**github**仓库并整理成文档保存至`_raw`，再通过`/wiki-ingest`导入wiki

### 更新

- `/wiki-update` 更新当前项目或知识库内容
- `/wiki-lint` 修复知识库结构和格式问题
- `/daily-update` 日常维护，保持知识新鲜度和索引完整

### 查询

- `/wiki-query` 查询知识库内容
- `/wiki-status` 查看知识库当前状态

### 维护

- `/cross-linker` 自动补全 Wiki Link
- `/tag-taxonomy` 标签规范化管理
- `/wiki-synthesize` 发现并填补概念间的综合空白
- `/wiki-dashboard` 创建动态仪表板视图
- `/graph-colorize` 按标签、类别、可见性对图谱进行颜色编码

### 研究

- `/wiki-research` 选择主题，AI 多轮网络调研并归档

## Skills 架构

> 标记说明：✅ 已安装可用 · 🔧 需自定义开发

### 第一层：Information（信息收集）

职责：统一收集原始资料，不做分类。

| Skill                   | 功能说明                                                                     | 状态 |
| ----------------------- | ---------------------------------------------------------------------------- |:---- |
| `wiki-ingest`           | 导入任意来源（文档、PDF、Markdown、URL、文本导出）到知识库，自动生成互联页面 | ✅   |
| `defuddle`              | 用 Defuddle CLI 从网页提取干净 Markdown，去除导航和干扰内容，节省 token      | ✅   |
| `page-archiver`         | 将网页存档至 Obsidian，含图片/视频等富媒体内容                               | ✅   |
| `pdf`                   | PDF 文本提取、表格解析、文档合并/拆分、表单处理                              | ✅   |
| `youtube-clipper`       | 下载 YouTube 视频和字幕，AI 生成章节，剪辑片段并烧录双语字幕                 | ✅   |
| `imagemagick-processor` | 图片格式转换（JPG/PNG/WebP）、压缩、批量处理、元数据提取                     | ✅   |
| `weread-skills`         | 微信读书：搜索书籍、管理书架、查看笔记划线、阅读统计                         | ✅   |
| `github-ingest`         | 抓取 GitHub 仓库 README、Release Notes、Issue 等技术文档                     | ✅   |
| `image-ocr`             | 图片文字识别，将截图/扫描件转为可检索文本                                    | 🔧   |

资料统一进入 `_raw/`（待加工暂存）或 `buckets/`（分类存放）、`Clippings/`（网页裁剪）。

### 第二层：Knowledge Process（知识加工）

职责：将原始资料提炼为可复用知识。

| Skill               | 功能说明                                                                       | 状态 |
| ------------------- | ------------------------------------------------------------------------------ |:---- |
| `wiki-synthesize`   | 扫描知识库，发现跨页面高频共现概念，自动生成综合分析页面                       | ✅   |
| `cross-linker`      | 扫描全库，发现缺失的跨页面引用并自动补写 wikilink                              | ✅   |
| `tag-taxonomy`      | 基于受控词表对全库标签进行规范化，消除同义标签混乱                             | ✅   |
| `wiki-dedup`        | 识别不同名但指向同一概念的页面（如"RSC"与"React Server Components"），合并去重 | ✅   |
| `wiki-capture`      | 将当前对话提炼为结构化知识页面存入知识库，支持快速暂存至 `_raw/`               | ✅   |
| `wiki-stage-commit` | 审查 `_staging/` 中的暂存页面，确认后升级到最终位置                            | ✅   |
| `concept-extractor` | 从长文中自动抽取核心概念，拆分生成独立知识节点                                 | 🔧   |
| `note-splitter`     | 将大段笔记按主题自动拆分为多个聚焦页面                                         | 🔧   |

输出为主题知识页面，并自动建立 Wiki Link、标签和关联。

### 第三层：Knowledge Update（知识更新）

职责：持续维护知识库与项目文档。

| Skill                 | 功能说明                                                                        | 状态 |
| --------------------- | ------------------------------------------------------------------------------- |:---- |
| `wiki-update`         | 将当前项目的架构决策、模式、权衡提炼后同步至 `projects/<name>.md`，支持增量更新 | ✅   |
| `wiki-history-ingest` | 批量导入 Claude / Codex / Pi / Copilot / Hermes 等 AI 工具的历史会话            | ✅   |
| `impl-validator`      | 验证实现是否与目标一致，输出 pass/warn/fail 裁决                                | ✅   |
| `daily-update`        | 日常维护周期：检查各来源新鲜度、更新索引、重新生成 `hot.md`                     | ✅   |
| `wiki-research`       | 指定主题后自动多轮网络调研，结果整理归档至知识库                                | ✅   |
| `git-summary`         | 读取 Git 提交历史，生成变更摘要和决策记录                                       | 🔧   |
| `architecture-review` | 分析仓库结构，输出架构图与模块说明                                              | 🔧   |
| `changelog-builder`   | 基于 Git 提交自动构建结构化变更日志                                             | 🔧   |
| `decision-log`        | 提取并记录技术决策，形成可追溯的决策档案                                        | 🔧   |

建议在每次 Git Commit 或开发结束后执行。

### 第四层：Knowledge Review（知识复盘）

职责：周期性维护和复盘。

| Skill            | 功能说明                                                                                | 状态 |
| ---------------- | --------------------------------------------------------------------------------------- | ---- |
| `wiki-lint`      | 审计知识库健康状况：孤立页面、断链、陈旧内容、格式问题；`--consolidate` 模式可自动修复  | ✅   |
| `wiki-status`    | 显示各来源的导入状态与增量 delta，`insights` 模式分析图谱结构（枢纽页、桥接页、孤岛页） | ✅   |
| `wiki-digest`    | 生成指定周期（日/周/月）的知识摘要，以通讯体裁汇报近期所学                              | ✅   |
| `wiki-dashboard` | 使用 Obsidian Bases 或 Dataview 创建动态可查询的仪表板视图                              | ✅   |
| `graph-colorize` | 按标签、类别或可见性重写 `graph.json`，为图谱节点着色                                   | ✅   |
| `wiki-query`     | 在知识库中检索问题，支持多跳关联推理，返回带 wikilink 引用的综合答案                    | ✅   |
| `memory-bridge`  | 按 AI 工具维度浏览、对比知识，发现不同工具间的知识盲区                                  | ✅   |
| `daily-review`   | 汇总当日 Daily Notes、提交和任务，生成每日复盘                                          | 🔧   |
| `weekly-review`  | 汇总本周学习、项目进展和技术决策，生成周报                                              | 🔧   |
| `monthly-review` | 月度知识盘点，评估知识库增长和质量趋势                                                  | 🔧   |
| `orphan-finder`  | 专项扫描无任何入链的孤立页面，输出待处理列表                                            | 🔧   |

### 第五层：Automation（自动化）

职责：通过自动化钩子和调度，触发各类 Skills。

推荐工具：

- Hooks（Git 钩子、文件系统监听）
- MCP（多通道处理器）
- Claude Code（自动执行代码）
- LaunchAgent / Cron（定时任务）

## Claude Code Hooks

推荐自动触发点：

- **PostCommit** → 自动执行 `/wiki-update`
- **Save _raw/** → 自动执行 `/wiki-ingest`
- **Weekly** → 自动执行 `/weekly-review`

## MCP 建议

- **GitHub MCP**：监听 GitHub 事件，触发知识更新和摘要生成。
- **Filesystem MCP**：监控文件变动，自动导入和处理新资料。
- **Obsidian MCP**：集成 Obsidian 编辑器事件，实现实时知识加工。
- **Browser MCP**：捕获浏览器剪辑内容，自动归档至 `Clippings/`。
- **Fetch MCP**：定时抓取外部数据源，补充资料库。

## Daily Notes 工作流

每日模板示例：

```
# 今日工作 - {{date}}

## 今日完成
- 

## 学习收获
- 

## 决策记录
- 

## 遇到的问题
- 

## 明日计划
- 
```

通过每日笔记跟踪工作进展和知识积累。

## Git 工作流

1. **提交代码（Commit）**：完成代码和文档变更。
2. **更新知识库**：执行 `/wiki-update`，同步知识库内容。
3. **生成变更日志**：自动构建项目变更日志，便于回顾和发布。

## 图片整理

![[assets/README/IMG-20260702110047245.png]]

1. 下载当前文件的附件。
2. 附件管理：重新排列所有链接附件。

> 通过上述两步操作，可以将图片以文件为目录保存至 `assets/` 目录下，方便管理和引用。

## 建议开发的自定义 Skills

### 学习类

- `/tech-digest`：扫描 `buckets/Chronicle/Clippings/` 中最新技术文章、GitHub README、发布说明，生成「本周 AI 技术周报」，自动链接已有知识节点。
- `/weekly-tech-review`：汇总本周阅读文章、提交记录和 Daily Notes，生成技术周报。

### 项目类

- `/project-retrospective`：读取最近一周的 Git 提交、Daily Notes 和项目文档，自动生成项目周报，包括完成事项、技术决策、踩坑记录、待优化项和后续建议，并同步至 Obsidian。
- `/repo-architecture`：自动分析仓库结构，输出架构图和模块说明。

### AI 类

- `/github-release-digest`：自动阅读 GitHub Release，生成升级摘要和 Breaking Changes。
- `/paper-to-note`：PDF 转 Wiki，提取摘要、关键观点和实验结果。
- `/prompt-library`：自动整理 AI Prompt，去重、分类、建立关联。

### 维护类

- `/knowledge-refactor`：扫描重复、碎片化笔记，自动建议合并或拆分。

## 已知问题与规范

### `_raw/` 文件格式规范

**问题**：gitingest 抓取的 GitHub 仓库内容会将仓库中所有文件拼接成一个文件。如果目标仓库本身是文档站（如 VitePress、MkDocs 构建的站点），每个页面都带有 YAML frontmatter，拼接后文件内会包含数百至数千个 `---` 分隔符。将此类文件保存为 `.md` 后缀时，Obsidian 的 Dataview、obsidian-linter、omnisearch 等插件会扫描全文所有 `---`，触发 O(n²) 解析或批量报警，导致索引报错。

**规范**：`github-ingest` skill 保存的抓取结果统一使用 `.txt` 后缀（`_raw/github-<owner>-<repo>.txt`），避免 Obsidian 插件索引。wiki-ingest 读取文件内容不依赖后缀，传完整路径即可正常处理。

**受影响仓库类型**：VitePress、MkDocs、Docusaurus、Jekyll、Hugo 等文档站仓库，以及任何每个 `.md` 文件都带 frontmatter 的仓库。普通代码仓库（frontmatter 数量 < 200）保存为 `.md` 通常无问题。

**参考数据**：

| 仓库 | `---` 数量 | 保存格式 | Obsidian 状态 |
|------|-----------|---------|--------------|
| `danielmiessler/Fabric` | 139 | `.md` | 正常 ✅ |
| `sebastienrousseau/dotfiles.github.io`（VitePress，22 语言） | 2549 | `.txt` | 正常 ✅（原 `.md` 报错 ❌） |

### `userIgnoreFilters` 的局限性

Obsidian 的「排除文件夹」功能（`app.json` 的 `userIgnoreFilters`）只排除搜索结果、Graph View 和 Unlinked Mentions，**不能阻止** Dataview、obsidian-linter、omnisearch 等插件扫描文件。如需彻底排除，将目录改为点开头（如 `_raw/.archived`）是唯一可靠方案。

## 最佳实践

- 统一使用 `_raw/` 作为待加工原始资料的暂存入口，网页裁剪进 `Clippings/`，分类资料进 `buckets/`。
- 保持知识加工流程的标准化和自动化。
- 定期执行知识复盘，保证内容的时效性和准确性。
- 充分利用 AI 辅助，提升知识提炼和关联效率。
- 采用清晰规范的标签和分类体系。
- 编写每日工作日志，形成持续的知识积累。
- 结合 Git 工作流，实现代码与文档的同步更新。
- 图片和附件统一管理，保持目录结构整洁。
- 利用自动化钩子和 MCP，减少手动操作。
- 定期回顾和优化知识库结构，保持活力与可用性。