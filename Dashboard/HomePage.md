---
banner: "https://images.unsplash.com/photo-1665430922646-5f4fecfc02bd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1332&q=80"
banner_y: 1
---

## Diary

[[buckets/workspce/Daily Record]]: 工作日志

## Frontend

[[buckets/workspce/Front-end Technology]]

## Work Records

[[buckets/work-records/vscode-vim]]: VSCode Vim 操作手册

```dataview
table file.mtime AS 修改时间
from "buckets/work-records"
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

[[buckets/workspce/Buckets]]: 笔记、网摘等内容

## 归档

[[buckets/workspce/Archives File]]

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

## 🌈 彩色词云

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

// ── 2. 渲染参数 ───────────────────────────────────────────
// 加大字号差异：最小 vs 最大比例约为 1:6（扩大2倍）
const MIN_FONT = 8;    // 最小字体 (px)
const MAX_FONT = 80;   // 最大字体 (px) - 超大标签更突出
const SHOW_TOP = 80;   // 显示的标签数量

const visible = entries.slice(0, SHOW_TOP);
const counts = visible.map(([, c]) => c);
const minC = Math.min(...counts);
const maxC = Math.max(...counts);
const logMin = Math.log1p(minC);
const logMax = Math.log1p(maxC);
const range = logMax - logMin || 1;

// 配色方案 (更多颜色组合)
const COLORS = [
    "#b91c1c", "#dc2626", "#ef4444",  // 红色系
    "#15803d", "#16a34a", "#22c55e",  // 绿色系
    "#1e40af", "#2563eb", "#3b82f6",  // 蓝色系
    "#a16207", "#ca8a04", "#eab308",  // 黄色系
    "#7c3aed", "#8b5cf6", "#a78bfa",  // 紫色系
    "#0f766e", "#0d9488", "#14b8a6",  // 青色系
    "#c026d3", "#d946ef", "#e879f9",  // 粉色系
    "#ea580c", "#f97316", "#fb923c",  // 橙色系
];

// ── 3. 碰撞检测工具函数 ───────────────────────────────────
const placed = []; // 已放置的标签 {x, y, w, h}

// 估算文本尺寸（像素）
function estimateSize(fontSize, text) {
    const charWidth = fontSize * 0.55; // 平均字符宽度系数
    const w = text.length * charWidth;
    const h = fontSize * 1.3;
    return { w: Math.ceil(w), h: Math.ceil(h) };
}

// 检查两个矩形是否重叠
function overlaps(x1, y1, w1, h1, x2, y2, w2, h2, padding = 4) {
    return !(x1 + w1 + padding < x2 ||
             x2 + w2 + padding < x1 ||
             y1 + h1 + padding < y2 ||
             y2 + h2 + padding < y1);
}

// 检查是否与所有已放置的标签重叠
function checkCollision(x, y, w, h) {
    for (const p of placed) {
        if (overlaps(x, y, w, h, p.x, p.y, p.w, p.h)) {
            return true;
        }
    }
    return false;
}

// 检查是否在安全边界内（考虑边距）
function isInBounds(x, y, w, h) {
    return x >= SAFE_MARGIN &&
           y >= SAFE_MARGIN &&
           x + w <= CONTAINER_WIDTH - SAFE_MARGIN &&
           y + h <= CONTAINER_HEIGHT - SAFE_MARGIN;
}

// 阿基米德螺旋线搜索最佳位置（带边界约束）
function findSpiralPosition(centerX, centerY, maxRadius, size) {
    const step = 2; // 螺旋步长
    const goldenAngle = 137.508 * Math.PI / 180; // 黄金角度

    for (let i = 0; i < 2000; i++) {
        const radius = step * Math.sqrt(i);
        if (radius > maxRadius) break;

        const angle = i * goldenAngle;
        const x = centerX + radius * Math.cos(angle) - size.w / 2;
        const y = centerY + radius * Math.sin(angle) - size.h / 2;

        // 先检查碰撞，再检查边界
        if (!checkCollision(x, y, size.w, size.h) && isInBounds(x, y, size.w, size.h)) {
            return { x, y };
        }
    }

    // 如果螺旋失败，尝试随机位置（严格限制在边界内）
    for (let attempt = 0; attempt < 100; attempt++) {
        const x = SAFE_MARGIN + Math.random() * (CONTAINER_WIDTH - size.w - SAFE_MARGIN * 2);
        const y = SAFE_MARGIN + Math.random() * (CONTAINER_HEIGHT - size.h - SAFE_MARGIN * 2);
        if (!checkCollision(x, y, size.w, size.h)) {
            return { x, y };
        }
    }

    // 最后手段：在中心区域找一个不重叠的位置（放宽边界检查）
    for (let attempt = 0; attempt < 50; attempt++) {
        const x = CONTAINER_WIDTH * 0.2 + Math.random() * (CONTAINER_WIDTH * 0.6 - size.w);
        const y = CONTAINER_HEIGHT * 0.2 + Math.random() * (CONTAINER_HEIGHT * 0.6 - size.h);
        if (!checkCollision(x, y, size.w, size.h)) {
            return { x, y };
        }
    }

    // 极端情况：放置在中心偏上位置
    return {
        x: (CONTAINER_WIDTH - size.w) / 2,
        y: (CONTAINER_HEIGHT - size.h) / 2 - 50
    };
}

// ── 4. 创建容器 ───────────────────────────────────────────
const CONTAINER_WIDTH = 900;
const CONTAINER_HEIGHT = 450;
const SAFE_MARGIN = 15; // 安全边距（像素），防止标签贴边被截断

const root = dv.el("div", "", {
    attr: {
        style: `position:relative;width:100%;height:${CONTAINER_HEIGHT}px;border-radius:14px;` +
               `background:linear-gradient(135deg, rgba(240,240,255,0.15), rgba(255,240,245,0.15));` +
               `overflow:hidden;`
    }
});

// ── 5. 按权重排序并布局 ───────────────────────────────────
// 先按使用次数降序排列，确保大词优先放置
const sortedTags = visible.sort((a, b) => b[1] - a[1]);

const centerX = CONTAINER_WIDTH / 2;
const centerY = CONTAINER_HEIGHT / 2;

sortedTags.forEach(([tag, count], i) => {
    // 计算字体大小和样式
    const ratio = Math.pow((Math.log1p(count) - logMin) / range, 1.5);
    const fontSize = MIN_FONT + ratio * (MAX_FONT - MIN_FONT);
    const angle = (Math.random() * 40 - 20).toFixed(1); // ±20° 轻微旋转
    const color = COLORS[i % COLORS.length];
    const opacity = 0.55 + ratio * 0.45;
    const fontWeight = ratio > 0.5 ? '700' : '500';

    // 估算尺寸
    const displayTag = tag.startsWith("#") ? tag.substring(1) : tag;
    const size = estimateSize(fontSize, displayTag);

    // 螺旋搜索位置（带边界约束）
    const maxRadius = Math.min(CONTAINER_WIDTH, CONTAINER_HEIGHT) * 0.4 - SAFE_MARGIN;
    const pos = findSpiralPosition(centerX, centerY, maxRadius, size);

    // 最终边界检查，确保不超出安全区域
    const finalX = Math.max(SAFE_MARGIN, Math.min(pos.x, CONTAINER_WIDTH - size.w - SAFE_MARGIN));
    const finalY = Math.max(SAFE_MARGIN, Math.min(pos.y, CONTAINER_HEIGHT - size.h - SAFE_MARGIN));

    // 记录已放置的位置（使用修正后的坐标）
    placed.push({ x: finalX, y: finalY, w: size.w, h: size.h });

    // 转换为百分比坐标
    const leftPct = (finalX / CONTAINER_WIDTH * 100).toFixed(2);
    const topPct = (finalY / CONTAINER_HEIGHT * 100).toFixed(2);

    const span = root.createEl("span", {
        text: displayTag,
        attr: {
            style: `
                position:absolute;
                left:${leftPct}%;
                top:${topPct}%;
                font-size:${fontSize}px;
                font-weight:${fontWeight};
                color:${color};
                padding:${ratio > 0.6 ? '6px 14px' : ratio > 0.4 ? '3px 8px' : '2px 5px'};
                transform:rotate(${angle}deg);
                cursor:pointer;
                transition:all 0.25s ease;
                opacity:${opacity};
                z-index:${Math.floor(ratio * 100)};
                text-shadow:${ratio > 0.6 ? '0 2px 6px rgba(0,0,0,0.12)' : 'none'};
                white-space:nowrap;
                line-height:1.1;
            `
        }
    });

    // 悬停效果
    span.addEventListener("mouseenter", () => {
        span.style.transform = "rotate(0deg) scale(1.25)";
        span.style.opacity = "1";
        span.style.zIndex = "9999";
        span.style.textShadow = `0 4px 12px ${color}50`;
    });
    span.addEventListener("mouseleave", () => {
        span.style.transform = `rotate(${angle}deg) scale(1)`;
        span.style.opacity = `${opacity}`;
        span.style.zIndex = `${Math.floor(ratio * 100)}`;
        span.style.textShadow = ratio > 0.6 ? '0 2px 6px rgba(0,0,0,0.12)' : 'none';
    });
});

// ── 5. 底部说明 ───────────────────────────────────────────
dv.el("div", `🏷️ 展示 ${visible.length} 个标签 (总计 ${entries.length} 个) · 字号反映使用频次 · 允许重叠旋转`, {
    attr: {
        style: "margin-top:20px;font-size:0.72em;color:var(--text-muted);text-align:center;" +
               "font-style:italic;"
    }
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