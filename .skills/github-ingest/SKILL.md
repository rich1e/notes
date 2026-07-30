---
name: github-ingest
description: Fetch GitHub repository technical docs (README, code tree, CHANGELOG)
  using gitingest CLI and save to _raw/ with github tag for wiki-ingest processing.
  Use when the user says "ingest this github repo", "grab the readme from <url>",
  "抓取 GitHub 仓库", "fetch github docs for <owner/repo>", "把这个仓库加入 wiki",
  "save this repo to my wiki", or pastes a GitHub URL and says "add this to my wiki" /
  "save this repo". Also triggered by "/github-ingest <url>". Always use this skill
  when the user provides any github.com URL and wants to learn about or preserve the
  repo's content.
---

# github-ingest

Fetch a GitHub repository's content using `gitingest` and save it to `_raw/` as a structured markdown file with proper frontmatter, ready for `wiki-ingest` to distill into wiki pages.

## Prerequisites

Check that `gitingest` is available:

```bash
which gitingest
```

If not found, install via pipx:

```bash
pipx install gitingest
```

## Input formats

Accept any of these:

| Format | Example |
|--------|---------|
| Full URL | `https://github.com/owner/repo` |
| Short form | `owner/repo` |
| With branch | `https://github.com/owner/repo/tree/branch` |
| With token (private repo) | `https://github.com/owner/repo` + env `GITHUB_TOKEN` |

Parse out `owner`, `repo`, and optionally `branch` from the input. Default branch is `main`.

## Execution

Run gitingest and capture output to a temp file:

```bash
gitingest https://github.com/<owner>/<repo> -o /tmp/github-<owner>-<repo>.txt
```

For a specific branch:

```bash
gitingest https://github.com/<owner>/<repo> -b <branch> -o /tmp/github-<owner>-<repo>.txt
```

For private repos (if the user provides a token or GITHUB_TOKEN is set):

```bash
gitingest https://github.com/<owner>/<repo> -t "$GITHUB_TOKEN" -o /tmp/github-<owner>-<repo>.txt
```

gitingest outputs a single text file containing: directory tree + all source files + README content.

### Large repositories

Well-known large repos (react, vue, angular, linux, chromium, etc.) or repos with more than ~500 files benefit from filtering to docs only. Use `--include-pattern` to fetch only markdown files:

```bash
gitingest https://github.com/<owner>/<repo> --include-pattern "*.md" -o /tmp/github-<owner>-<repo>.txt
```

If you're unsure about repo size, run without filtering first. If gitingest reports >1000 files or the output file exceeds 30MB, re-run with `--include-pattern "*.md"` and note this in the output file's summary field.

## Output file

Construct the final file at:

```
_raw/github-<owner>-<repo>.txt
```

**保存为 `.txt` 而非 `.md`**：gitingest 会将整个仓库所有文件拼接成一个文件，其中可能包含数百至数千个内嵌 YAML frontmatter 块（`---` 分隔符）。若保存为 `.md`，Obsidian 的 Dataview、obsidian-linter、omnisearch 等插件会扫描全文所有 `---`，触发 O(n²) 解析或批量报警，导致索引报错。`.txt` 后缀让 Obsidian 完全跳过此文件，wiki-ingest 读取时不受影响。

The file must have this structure:

```
---
title: "<repo> GitHub 技术文档"
category: references
tags: [github, <repo-name>]
sources: ["https://github.com/<owner>/<repo>"]
created: <ISO 8601 timestamp, e.g. 2026-07-03T10:00:00Z>
updated: <ISO 8601 timestamp>
summary: "GitHub 仓库 <owner>/<repo> 的代码结构、README 和文档摘要，由 gitingest 抓取"
github_repo: "<owner>/<repo>"
github_branch: "<branch>"
---

# <repo>

> 通过 gitingest 于 <YYYY-MM-DD> 抓取自 https://github.com/<owner>/<repo>

<contents of /tmp/github-<owner>-<repo>.txt>
```

Write this file using Python (handles encoding and large files reliably):

```bash
python3 -c "
import sys, datetime

owner = '<owner>'
repo = '<repo>'
branch = '<branch>'
now = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
date = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d')

with open('/tmp/github-{owner}-{repo}.txt', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

frontmatter = f'''---
title: \"{repo} GitHub 技术文档\"
category: references
tags: [github, {repo}]
sources: [\"https://github.com/{owner}/{repo}\"]
created: {now}
updated: {now}
summary: \"GitHub 仓库 {owner}/{repo} 的代码结构、README 和文档摘要，由 gitingest 抓取\"
github_repo: \"{owner}/{repo}\"
github_branch: \"{branch}\"
---

# {repo}

> 通过 gitingest 于 {date} 抓取自 https://github.com/{owner}/{repo}

'''

vault_path = '/Users/rich1e/workspace/code/notes'
output_path = f'{vault_path}/_raw/github-{owner}-{repo}.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(frontmatter + content)

import os
size = os.path.getsize(output_path)
print(f'Saved: {output_path}')
print(f'Size: {size:,} bytes ({size/1024/1024:.1f} MB)')
".format(owner=owner, repo=repo, branch=branch)
```

In practice, construct the Python snippet dynamically with the actual `owner`, `repo`, `branch` values substituted in — don't pass them as shell variables, write them directly into the script string.

## Update .manifest.json

After saving the file, add an entry to `.manifest.json` under the `sources` key:

```json
"https://github.com/<owner>/<repo>": {
  "ingested_at": "<ISO timestamp>",
  "size_bytes": <file size>,
  "modified_at": "<ISO timestamp>",
  "content_hash": "gitingest",
  "source_type": "github_repo",
  "github_repo": "<owner>/<repo>",
  "github_branch": "<branch>",
  "project": null,
  "pages_created": [],
  "pages_updated": []
}
```

Read the current `.manifest.json`, merge the new entry, and write it back.

## Completion message

After saving, tell the user:

```
已保存：_raw/github-<owner>-<repo>.txt

下一步：运行 wiki-ingest 将其蒸馏为 wiki 页面
  → "ingest _raw/github-<owner>-<repo>.txt"
  → 或者 "process the github-<repo> raw file"
```

## Error handling

- **gitingest not found**: prompt user to run `pipx install gitingest`, then retry
- **Network error / repo not found**: show the error from gitingest and ask user to verify the URL
- **Private repo 403**: ask user to provide a GitHub token (`GITHUB_TOKEN` env var or pass with `-t`)
- **Output file too large** (>50MB): warn the user; consider using `--include-pattern "*.md"` to fetch only docs

## Re-ingesting

If `_raw/github-<owner>-<repo>.txt` already exists, tell the user and ask whether to overwrite (default: yes, update the `updated` timestamp).

## 不要做什么

- **不要保存为 `.md` 后缀**：gitingest 拼接的仓库内容通常含数百至数千个内嵌 `---` 分隔符（每个源文件的 frontmatter），会触发 Obsidian 插件报错
- **不要在 wiki-ingest 时直接传 `.txt` 文件名前缀**：wiki-ingest 读取内容不依赖后缀，传完整路径即可
- **不要对超过 30MB 的输出文件继续后续步骤**：直接警告用户，建议用 `--include-pattern "*.md"` 重跑
- **不要把 vault_path 硬编码在 skill 里**：Python 脚本里的路径应从上下文（config/.env）解析，或直接使用当前 vault 路径；skill 示例中的路径仅为占位符
- **不要把 GitHub token 打印到输出**：使用 `-t "$GITHUB_TOKEN"` 时，不要在 completion message 里回显 token 值
