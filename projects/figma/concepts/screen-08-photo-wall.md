---
title: Screen 08 手账 · 相册墙 UI 设计
category: concepts
tags: [ui, codesign, react, figma, journal, inline-svg]
sources:
  - store/project for X/figma/App.jsx (PhotoWallScreen L1236-1609)
  - store/project for X/figma/DESIGN.md (Screen 07/08 spec)
  - store/project for X/figma/SCREEN08_PATCH_NOTE.md (设计要求与已知 bug)
created: 2026-08-23T16:15:00Z
updated: 2026-08-23T16:15:00Z
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: "2026-08-23"
summary: 三段日期分区(07/06/05)+ Polaroid + WashiTape + ThumbPin + PaperClip 四件套原语,纯内联 SVG 实现,所有原语可复用为屏 N 的贴照片场景基座
---

# Screen 08 · 手账 · 相册墙 UI 设计

## Context

Photo Album Mobile UI 在七屏基线(屏1-7)验证后,追加的第 8 屏是手账风格的相册墙 — 把屏5/6 散落的回忆以"贴上墙"的方式聚合展示。这是验证屏7(单条手账 detail)风格能否横向扩展的关键屏。^[extracted:SCREEN08_PATCH_NOTE.md "Full Screen 08 design"]

## 三段分区结构

| 段 | 标题(中文 + 编号) | polaroid 数 | washi tape 颜色 |
|---|---|---|---|
| 07 | 京都的夏天 | 3 (竹林 / 雨后桥 / 町屋灯笼) | mint `#a8d4c0` |
| 06 | 海边日落 | 3 (橘色海 / 脚印贝壳 / 夜空下) | rose `#e8b4a0` |
| 05 | 一个人的咖啡馆 | 3 (拿铁 / 半本书 / 蛋糕) | pink `#f4c7c7` |

每段高度 ~96-102px,横向绝对定位 polaroid + 顶层覆盖 thumb pin + 右上角 washi tape 旋转 -3°~+3°。^[extracted:App.jsx L1325-1559]

## 4 个原语(全部内联 SVG)

| 原语 | props | 用途 |
|---|---|---|
| `PaperClip` | color / rotation / top / left / scale | 回形针夹 polaroid 角(屏8 左上) |
| `ThumbPin` | color / rotation / top / left / size | 彩色图钉钉 polaroid(屏8 各 polaroid 顶点) |
| `Polaroid` | caption / date / scene / width / height / rotation / top / left + children | 复用屏7 的 props,但加定位字段 |
| `WashiTape` | color / rotation / width / top / left / opacity | 复用屏7 的 washi tape(opacity=0.85 固定) |

`PaperClip` 与 `ThumbPin` 在屏7 不存在,是屏8 独有,定位 zIndex 6-7(在 polaroid 之上、装饰层之下)。^[extracted:App.jsx L1200-1232]

## 必须保留的视觉规律

- **cursive 中文标题**(`Snell Roundhand` 栈)在每段左上,带 `transform: rotate(-2deg~-3deg)`
- **贴纸 emoji 行**用屏7 的 `StickerChip`(✿夏日 / ◐黄昏 / ✦心情)
- **hashtag chips** 用屏7 的 `JournalHashtag`(`text=` / `rotation=` / `color=`,**不是** `label=` / `rotate=`)
- **底部 action row**:编辑 / 排序 / 分享 / 更多(4 个透明按钮,cyan 1.8px 描边)— 与屏7 的 edit/lock/share/delete **结构不同**,屏8 多了"排序"
- **header 副标题**:`~ 把我喜欢的瞬间都贴在墙上 ~`(cursive 字体,屏7 没有这个层)

## JOURNAL_PALETTE 是扁平结构(屏8 早期踩坑)

```js
const JOURNAL_PALETTE = {
  bg, paper, kraft, ink, inkMuted, accent,
  washiMint, washiRose, washiPink, washiCream,  // 平铺
  dotted, sticker
};
```

**没有** `washi.mint` / `washi.cream` 这种嵌套子对象。SCREEN08_PATCH_NOTE 列了 6 处需要从 `washi.*` 改为平铺 `washiXxx` 的修复点(Line 1227/1273/1276/1317/1337/1346)。^[extracted:SCREEN08_PATCH_NOTE.md "Then additionally fix"]

## 已知失败模式(从 SCREEN08_PATCH_NOTE 学到的)

- **str_replace 失败连环触发**:旧 anchor 因为之前 replace 没匹配而漂移,后续 replace 都失败 → 必须用 `view` 读全文重新对 anchor
- **JournalTopBar / JournalActionRow 占位组件**:屏8 早期版本引用了屏7 的占位组件,后来改成内联 SVG(屏8 的 nav 是 back + 相册墙 + share,不是屏7 的 back + title + share)
- **JournalHashtag props 改名**:从 `label= / rotate=` → `text= / rotation=`,4 处调用要同步改

## Implications

- 屏8 与屏7 共享 journal 设计 token,但不复用屏7 的 component(屏7 是 detail page 单条手账,屏8 是 wall — 模式不同)
- 所有原语纯 SVG + 内联样式,可移植到任何"贴照片"场景,是屏9 / Screen N 的复用基座
- 屏8 顺利落地后,屏9 / 屏 N 的新加不必再经历 str_replace 失败循环 — 可以直接走 create 完整覆盖 + 已知 bug 列表

## Related

- [[projects/figma/figma]] — 项目概览
- [[projects/figma/skills/codesign-session-jsonl-recovery]] — 屏8 源码已通过 session JSONL 重建过一次
- [[concepts/atomic-state-recovery]] — 状态被破坏时的二次证据还原(类似思路)
- [[entities/figwright]] — 与本项目无关的另一套 Figma 集成