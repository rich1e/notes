---
banner: "https://images.unsplash.com/photo-1665430922646-5f4fecfc02bd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1332&q=80"
banner_y: 0.5
---

## Diary

[[Daily Record]]: 工作日志

## Frontend

[[Front-end Technology]]

## Work Records

[[work-records/vscode-vim]]: VSCode Vim 操作手册

```dataview
table file.mtime AS 修改时间
from "work-records"
sort file.mtime desc
limit 5
```

## Travel

```dataview
table date, address
from ""
where contains(file.path, "travel")
```

## Undone

```dataview
table date, address
from ""
where contains(file.tags, "undone")
```

## 储物柜

[[Buckets]]: 笔记、网摘等内容

## 归档

[[Archives File]]

## 笔记年度统计

```dataviewjs
// 统计2021-2026年的笔记数量
const yearFolders = ['2021', '2022', '2023', '2024', '2025', '2026'];
const yearStats = [];

for (const year of yearFolders) {
  const pages = dv.pages(`"${year}"`);
  yearStats.push({
    year: year,
    count: pages.length
  });
}

// 计算最大值用于比例
const maxCount = Math.max(...yearStats.map(s => s.count));
const total = yearStats.reduce((sum, s) => sum + s.count, 0);

// 渲染
const root = dv.el("div", "");

// 顶部统计卡片
const hdr = root.createEl("div", { attr: {
    style: "display:flex;gap:28px;flex-wrap:wrap;margin-bottom:20px;" +
           "padding:12px 18px;border-radius:10px;" +
           "background:var(--background-secondary)"
}});

[
    ["📅", "统计年份", `${yearFolders.length} 年`],
    ["📝", "笔记总数", `${total} 篇`],
    ["📊", "平均数量", `${Math.round(total/yearFolders.length)} 篇/年`],
].forEach(([icon, label, val]) => {
    const cell = hdr.createEl("div", { attr: { style: "display:flex;flex-direction:column;gap:3px" } });
    cell.createEl("span", { text: `${icon}  ${label}`, attr: {
        style: "font-size:0.68em;color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em"
    }});
    cell.createEl("span", { text: val, attr: {
        style: "font-size:0.95em;font-weight:600;color:var(--text-normal)"
    }});
});

// 柱状图
const chart = root.createEl("div", { attr: {
    style: "display:flex;flex-direction:column;gap:8px;margin-top:12px"
}});

const COLORS = ["#7c6af7","#38bdf8","#34d399","#fb923c","#f472b6","#a78bfa"];

yearStats.forEach((stat, i) => {
    const pct = maxCount > 0 ? Math.round((stat.count / maxCount) * 100) : 0;
    const color = COLORS[i % COLORS.length];

    const row = chart.createEl("div", { attr: {
        style: "display:flex;align-items:center;gap:12px"
    }});

    // 年份标签
    row.createEl("span", { text: stat.year, attr: {
        style: "min-width:60px;text-align:right;" +
               "font-size:0.85em;font-weight:600;color:var(--text-accent)"
    }});

    // 进度条
    const track = row.createEl("div", { attr: {
        style: "flex:1;height:28px;border-radius:6px;overflow:hidden;" +
               "background:var(--background-modifier-border)"
    }});

    const bar = track.createEl("div", { attr: {
        style: `width:${Math.max(pct, 2)}%;height:100%;border-radius:6px;` +
               `background:${color};opacity:.85;` +
               "transition:width 0.3s ease"
    }});

    // 在柱状图内显示数量
    bar.createEl("span", { text: stat.count, attr: {
        style: "display:inline-block;padding:0 10px;line-height:28px;" +
               "font-size:0.8em;font-weight:600;color:white"
    }});

    // 百分比
    row.createEl("span", { text: `${pct}%`, attr: {
        style: "min-width:45px;text-align:right;font-size:0.75em;" +
               "color:var(--text-muted);font-variant-numeric:tabular-nums"
    }});
});
```

## 标签统计

```dataviewjs
// ── 1. 收集全库标签 ───────────────────────────────────────
const tagMap = new Map();
const isNoise = n =>
    /^[0-9a-fA-F]{3,8}$/.test(n) ||   // 十六进制色值
    /^\d+$/.test(n)                 ||   // 纯数字
    n.length <= 1;                       // 过短

for (const page of dv.pages()) {
    for (const raw of (page.file.tags ?? [])) {
        const name = raw.startsWith("#") ? raw.slice(1) : raw;
        if (isNoise(name)) continue;
        const key = raw.startsWith("#") ? raw : "#" + raw;
        tagMap.set(key, (tagMap.get(key) ?? 0) + 1);
    }
}

const entries = [...tagMap.entries()].sort((a, b) => b[1] - a[1]);
const total   = entries.reduce((s, [, v]) => s + v, 0);
const max     = entries[0]?.[1] ?? 1;
const logMax  = Math.log1p(max);

// ── 2. 渲染 ───────────────────────────────────────────────
const root = dv.el("div", "");

// 顶部统计卡片
const hdr = root.createEl("div", { attr: {
    style: "display:flex;gap:28px;flex-wrap:wrap;margin-bottom:16px;" +
           "padding:12px 18px;border-radius:10px;" +
           "background:var(--background-secondary)"
}});

[
    ["🏷️", "独特标签",   String(entries.length)],
    ["📝", "总使用次数", String(total)],
    ["🔥", "TOP 标签",   `${entries[0]?.[0] ?? "—"}  ×${entries[0]?.[1] ?? 0}`],
].forEach(([icon, label, val]) => {
    const cell = hdr.createEl("div", { attr: { style: "display:flex;flex-direction:column;gap:3px" } });
    cell.createEl("span", { text: `${icon}  ${label}`, attr: {
        style: "font-size:0.68em;color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em"
    }});
    cell.createEl("span", { text: val, attr: {
        style: "font-size:0.95em;font-weight:600;color:var(--text-normal)"
    }});
});

// 水平条形图（对数刻度，避免 daily 独占）
const COLORS = [
    "#7c6af7","#38bdf8","#34d399","#fb923c",
    "#f472b6","#a78bfa","#22d3ee","#4ade80",
    "#fbbf24","#f87171"
];

const chart = root.createEl("div", { attr: {
    style: "display:flex;flex-direction:column;gap:6px"
}});

entries.forEach(([tag, count], i) => {
    const pct   = Math.max(2, Math.round((Math.log1p(count) / logMax) * 96));
    const color = COLORS[i % COLORS.length];

    const row = chart.createEl("div", { attr: {
        style: "display:flex;align-items:center;gap:10px"
    }});

    // 标签名
    row.createEl("span", { text: tag, attr: {
        style: "min-width:116px;max-width:116px;text-align:right;" +
               "font-size:0.8em;white-space:nowrap;overflow:hidden;" +
               "text-overflow:ellipsis;color:var(--text-accent)"
    }});

    // 进度条轨道
    const track = row.createEl("div", { attr: {
        style: "flex:1;height:12px;border-radius:6px;overflow:hidden;" +
               "background:var(--background-modifier-border)"
    }});
    track.createEl("div", { attr: {
        style: `width:${pct}%;height:100%;border-radius:6px;background:${color};opacity:.85`
    }});

    // 次数
    row.createEl("span", { text: String(count), attr: {
        style: "min-width:36px;text-align:right;font-size:0.75em;" +
               "color:var(--text-muted);font-variant-numeric:tabular-nums"
    }});
});
```

## 最近修改

```dataview
table file.mtime AS 修改时间, file.folder AS 位置
from ""
where file.name != "HomePage"
sort file.mtime desc
limit 10
```