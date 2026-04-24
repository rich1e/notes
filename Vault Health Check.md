---
author: rich1e
tags: ["maintenance", "vault-health"]
date: <% tp.file.creation_date("YYYY-MM-DD HH:mm:ss") %>
Last modified date: <% tp.file.last_modified_date() %>
---

# 🏥 Vault 健康检查

本页面自动统计和分析 Obsidian 知识库的健康状况，帮助发现需要优化的地方。

## 📊 总览

```dataviewjs
// 获取所有笔记（排除 HomePage）
const allNotes = dv.pages('""').where(p => p.file.name !== "HomePage");
const totalNotes = allNotes.length;

// 获取有入站链接的笔记
const withInlinks = allNotes.where(p => p.file.inlinks && p.file.inlinks.length > 0);

// 获取有出站链接的笔记
const withOutlinks = allNotes.where(p => p.file.outlinks && p.file.outlinks.length > 0);

// 孤立笔记：没有任何入站和出站链接
const orphaned = allNotes.where(p =>
    (!p.file.inlinks || p.file.inlinks.length === 0) &&
    (!p.file.outlinks || p.file.outlinks.length === 0)
);

// 只有入站没有出站的笔记（终点笔记）
const deadEnds = allNotes.where(p =>
    p.file.inlinks && p.file.inlinks.length > 0 &&
    (!p.file.outlinks || p.file.outlinks.length === 0)
);

// 只有出站没有入站的笔记（起点笔记）
const startingPoints = allNotes.where(p =>
    p.file.outlinks && p.file.outlinks.length > 0 &&
    (!p.file.inlinks || p.file.inlinks.length === 0)
);

// 计算各项指标
const inlinkRatio = ((withInlinks.length / totalNotes) * 100).toFixed(1);
const outlinkRatio = ((withOutlinks.length / totalNotes) * 100).toFixed(1);
const orphanedRatio = ((orphaned.length / totalNotes) * 100).toFixed(1);

// 渲染统计卡片
const container = dv.el("div", "", {
    attr: {
        style: "display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:16px;margin-bottom:24px;"
    }
});

const cards = [
    { icon: "📝", title: "总笔记数", value: totalNotes, color: "#3b82f6", desc: "篇笔记" },
    { icon: "🔗", title: "已连接", value: `${withInlinks.length} (${inlinkRatio}%)`, color: "#10b981", desc: "有入站链接" },
    { icon: "📤", title: "有外链", value: `${withOutlinks.length} (${outlinkRatio}%)`, color: "#8b5cf6", desc: "有出站链接" },
    { icon: "🚫", title: "孤立笔记", value: `${orphaned.length} (${orphanedRatio}%)`, color: "#ef4444", desc: "无入站和出站" },
    { icon: "⬇️", title: "终点笔记", value: deadEnds.length, color: "#f59e0b", desc: "只有入站无出站" },
    { icon: "⬆️", title: "起点笔记", value: startingPoints.length, color: "#06b6d4", desc: "只有出站无入站" },
];

cards.forEach(card => {
    const cardEl = container.createEl("div", {
        attr: {
            style: `padding:20px;border-radius:12px;background:linear-gradient(135deg, ${card.color}15, ${card.color}08);` +
                   `border-left:4px solid ${card.color};box-shadow:0 2px 8px rgba(0,0,0,0.05);`
        }
    });

    cardEl.createEl("div", {
        text: `${card.icon} ${card.title}`,
        attr: {
            style: "font-size:0.75em;color:var(--text-muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:0.05em;"
        }
    });

    cardEl.createEl("div", {
        text: card.value,
        attr: {
            style: `font-size:1.8em;font-weight:700;color:${card.color};margin-bottom:4px;`
        }
    });

    cardEl.createEl("div", {
        text: card.desc,
        attr: {
            style: "font-size:0.7em;color:var(--text-muted);"
        }
    });
});
```

## 🔍 孤立笔记分析

孤立笔记是指既没有被其他笔记链接，也没有链接到其他笔记的页面。这些笔记可能需要添加链接以更好地融入知识库网络。

### 孤立笔记列表

```dataview
table file.folder AS 所在文件夹, file.mtime AS 最后修改
from ""
where (length(file.inlinks) = 0 or !file.inlinks) and (length(file.outlinks) = 0 or !file.outlinks)
and file.name != "Vault Health Check"
sort file.mtime desc
```

### 按文件夹分组的孤立笔记

```dataviewjs
// 获取孤立笔记
const allOrphaned = dv.pages('""')
    .where(p =>
        (!p.file.inlinks || p.file.inlinks.length === 0) &&
        (!p.file.outlinks || p.file.outlinks.length === 0) &&
        p.file.name !== "Vault Health Check"
    );

// 手动按文件夹分组
const folderMap = new Map();
allOrphaned.forEach(p => {
    const folder = p.file.folder;
    // 提取一级目录
    const match = folder.match(/^([^\/]+)/);
    const key = match ? match[1] : "根目录";

    if (!folderMap.has(key)) {
        folderMap.set(key, []);
    }
    folderMap.get(key).push(p);
});

// 转换为数组并排序
const groups = [...folderMap.entries()].sort((a, b) => b[1].length - a[1].length);

// 计算总数
const totalCount = allOrphaned.length;

// 渲染分组结果
dv.paragraph(`**共发现 ${totalCount} 个孤立笔记，分布在 ${groups.length} 个文件夹中**`);

for (const [key, notes] of groups) {
    dv.header(4, `📁 ${key} (${notes.length} 篇)`);
    const links = notes.map(n => n.file.link).sort();
    dv.list(links);
}
```

## 📈 连接度分布

显示每个笔记的入站链接数量排名，帮助发现知识库中的核心节点。

```dataview
table length(file.inlinks) as 入站数, length(file.outlinks) as 出站数, file.folder as 位置
from ""
where file.name != "Vault Health Check"
sort length(file.inlinks) desc
limit 20
```

## 🌟 高价值笔记

这些笔记被多个其他笔记引用，是知识库中的重要节点。

```dataview
table length(file.inlinks) as 引用数, file.mtime as 最后修改
from ""
where length(file.inlinks) >= 3 and file.name != "Vault Health Check"
sort length(file.inlinks) desc
limit 15
```

## 🕸️ 未分类笔记

位于根目录或没有明确分类的笔记，建议移动到合适的文件夹中。

```dataview
table file.size as 大小, file.mtime as 最后修改
from ""
where contains(file.path, "/") = false and file.name != "HomePage" and file.name != "Vault Health Check"
sort file.mtime desc
```

## 💡 优化建议

根据以上分析，以下是优化建议：

1. **为孤立笔记添加链接**
   - 浏览上述孤立笔记列表
   - 在相关笔记中添加双向链接 `[[笔记名称]]`
   - 考虑添加合适的标签进行分类

2. **整理未分类笔记**
   - 将根目录下的笔记移动到对应的年份或主题文件夹
   - 建立清晰的文件夹层级结构

3. **完善低连接度笔记**
   - 为只有入站没有出站的笔记（终点笔记）添加相关链接
   - 建立更多的横向关联，形成知识网络

4. **定期维护**
   - 每月运行一次健康检查
   - 及时清理重复或过时的内容
   - 保持标签体系的一致性

## 🔄 自动更新

本页面使用 Dataview 插件自动生成统计数据，每次打开时会自动刷新。最后更新时间：<% tp.file.last_modified_date() %>

---

*💡 提示：安装 Obsidian Graph View 插件可以可视化笔记之间的连接关系，更直观地查看知识库结构*
