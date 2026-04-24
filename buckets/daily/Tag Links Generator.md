---
author: rich1e
tags: ["automation", "linking"]
date: <% tp.file.creation_date("YYYY-MM-DD HH:mm:ss") %>
Last modified date: <% tp.file.last_modified_date() %>
---

# 🏷️ Daily 目录标签链接生成器

此页面自动分析 `/buckets/daily/` 目录中的标签，并为具有相同标签的文档建立双向链接。

## 📊 热门标签统计

```dataviewjs
// 收集所有标签和对应的文件
const tagMap = new Map();

for (const page of dv.pages('"buckets/daily"')) {
    for (const raw of (page.file.tags ?? [])) {
        const name = raw.startsWith("#") ? raw.slice(1) : raw;
        // 过滤掉过短的标签和纯数字
        if (name.length <= 1 || /^\d+$/.test(name)) continue;

        if (!tagMap.has(name)) {
            tagMap.set(name, []);
        }
        tagMap.get(name).push(page.file.link);
    }
}

// 转换为数组并排序
const entries = [...tagMap.entries()]
    .map(([tag, files]) => ({ tag, count: files.length, files }))
    .sort((a, b) => b.count - a.count);

// 只显示前30个热门标签
const topTags = entries.slice(0, 30);

// 渲染统计信息
dv.paragraph(`**共发现 ${entries.length} 种不同的标签，涉及 ${entries.reduce((sum, e) => sum + e.count, 0)} 次使用**`);

// 创建标签云式展示
const container = dv.el("div", "", {
    attr: {
        style: "display:flex;flex-wrap:wrap;gap:8px;margin:20px 0;padding:16px;background:var(--background-secondary-alt);border-radius:8px;"
    }
});

topTags.forEach(({ tag, count }) => {
    const link = container.createEl("a", {
        text: `#${tag} (${count})`,
        attr: {
            href: `#section-${tag}`,
            style: `padding:4px 12px;border-radius:20px;font-size:${Math.min(16 + count * 0.5, 28)}px;` +
                   `background:hsla(${count * 15}, 70%, 60%, 0.2);color:hsl(${count * 15}, 70%, 40%);` +
                   `text-decoration:none;display:inline-block;margin:2px;transition:all 0.2s;`
        }
    });

    link.addEventListener("mouseover", () => {
        link.style.transform = "scale(1.1)";
        link.style.background = `hsla(${count * 15}, 70%, 60%, 0.4)`;
    });
    link.addEventListener("mouseout", () => {
        link.style.transform = "scale(1)";
        link.style.background = `hsla(${count * 15}, 70%, 60%, 0.2)`;
    });
});
```

## 🔗 按标签分组的相关文档

以下列出每个热门标签下的所有相关文档，并为它们添加互相引用的链接。

### 使用说明

1. **手动添加链接**：点击下方的文档链接，在对应笔记中添加 `[[其他相关文档]]`
2. **批量处理**：使用 Obsidian 的查找替换功能批量添加
3. **定期维护**：每月运行一次此页面，更新标签关系

---

```dataviewjs
// 重新收集标签数据用于详细展示
const detailedTagMap = new Map();

for (const page of dv.pages('"buckets/daily"')) {
    for (const raw of (page.file.tags ?? [])) {
        const name = raw.startsWith("#") ? raw.slice(1) : raw;
        if (name.length <= 1 || /^\d+$/.test(name)) continue;

        if (!detailedTagMap.has(name)) {
            detailedTagMap.set(name, []);
        }
        detailedTagMap.get(name).push({
            link: page.file.link,
            path: page.file.path,
            mtime: page.file.mtime
        });
    }
}

// 按使用次数排序
const sortedTags = [...detailedTagMap.entries()]
    .map(([tag, files]) => ({ tag, files: files.sort((a, b) => b.mtime - a.mtime) }))
    .sort((a, b) => b.files.length - a.files.length)
    .slice(0, 20); // 只显示前20个标签

// 渲染每个标签组
for (const { tag, files } of sortedTags) {
    if (files.length < 2) continue; // 跳过只有一个文件的标签

    dv.header(3, `#${tag} (${files.length} 篇文档)`);

    // 创建表格显示相关文档
    const tableData = files.map((file, index) => {
        // 为该标签下的其他文档生成链接建议
        const relatedLinks = files
            .filter((_, i) => i !== index)
            .slice(0, 5) // 最多显示5个相关文档
            .map(f => `[[${f.link.replace(/.*\//, '')}|${f.link.replace(/.*\//, '').replace('.md', '')}]]`)
            .join(', ');

        return [
            file.link,
            file.mtime.toFormat('yyyy-MM-dd'),
            `> 💡 建议链接: ${relatedLinks}`
        ];
    });

    dv.table(['文档', '日期', '相关文档链接建议'], tableData);

    dv.el("div", "---", {
        attr: { style: "margin:20px 0;border-top:1px solid var(--background-modifier-border);" }
    });
}
```

## 🛠️ 自动化链接脚本

以下是一个 Python 脚本，可以自动为具有相同标签的文档添加互相引用：

````markdown
```python
import os
import re
from collections import defaultdict

def extract_tags_from_file(filepath):
    """从文件中提取所有 Markdown 格式的标签"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 #tag 格式的标签
    tags = re.findall(r'#[a-zA-Z0-9_-]+', content)
    return [tag[1:] for tag in tags]  # 去掉 # 符号

def find_daily_files(directory):
    """查找 daily 目录中的所有 markdown 文件"""
    files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.md') and not filename.startswith('.'):
            filepath = os.path.join(directory, filename)
            tags = extract_tags_from_file(filepath)
            files[filename] = tags
    return files

def build_tag_index(files):
    """构建标签到文件的索引"""
    tag_index = defaultdict(list)
    for filename, tags in files.items():
        for tag in tags:
            tag_index[tag].append(filename)
    return tag_index

def generate_link_suggestions(tag_index, min_occurrences=2):
    """生成链接建议（只包含出现2次以上的标签）"""
    suggestions = {}
    for tag, files in tag_index.items():
        if len(files) >= min_occurrences:
            suggestions[tag] = files
    return suggestions

def main():
    daily_dir = '/Users/rich1e/workspace/code/notes/buckets/daily'

    # 扫描文件
    print("正在扫描 daily 目录...")
    files = find_daily_files(daily_dir)

    # 构建索引
    tag_index = build_tag_index(files)

    # 生成建议
    suggestions = generate_link_suggestions(tag_index)

    # 输出结果
    print(f"\n发现 {len(suggestions)} 个有效标签\n")
    print("=" * 60)

    for tag, files in sorted(suggestions.items(), key=lambda x: -len(x[1])):
        print(f"\n#{tag} ({len(files)} 篇文档):")
        for file in files[:10]:  # 最多显示10个
            print(f"  - {file}")

if __name__ == '__main__':
    main()
```
````

## 💡 使用建议

### 方法一：手动添加（推荐小规模）

1. 查看上方表格中的"相关文档链接建议"列
2. 打开对应文档
3. 在合适位置添加 `[[文档名称]]` 链接

### 方法二：半自动处理（中等规模）

1. 复制上方表格中的链接建议
2. 使用 Obsidian 的批量查找替换功能
3. 在多个文件中同时添加链接

### 方法三：全自动处理（大规模）

1. 运行上方的 Python 脚本获取完整列表
2. 使用脚本自动生成链接代码
3. 通过 Git 进行版本控制后批量提交

## 📈 统计信息

```dataviewjs
// 统计总体情况
const allFiles = dv.pages('"buckets/daily"');
const totalFiles = allFiles.length;

let totalTags = 0;
const tagCount = new Map();

for (const page of allFiles) {
    for (const raw of (page.file.tags ?? [])) {
        const name = raw.startsWith("#") ? raw.slice(1) : raw;
        if (name.length <= 1 || /^\d+$/.test(name)) continue;

        totalTags++;
        tagCount.set(name, (tagCount.get(name) ?? 0) + 1);
    }
}

const uniqueTags = tagCount.size;
const avgTagsPerFile = (totalTags / totalFiles).toFixed(2);

dv.table(
    ['指标', '数值'],
    [
        ['📁 总文档数', `${totalFiles} 篇`],
        ['🏷️ 总标签使用次数', `${totalTags} 次`],
        ['✨ 独特标签数量', `${uniqueTags} 种`],
        ['📊 平均每篇标签数', `${avgTagsPerFile} 个`]
    ]
);
```

---

*最后更新：<% tp.file.last_modified_date() %>*

*💡 提示：将此页面添加到每日工作流中，定期维护标签链接关系*
