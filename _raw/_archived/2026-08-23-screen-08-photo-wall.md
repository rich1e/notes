---
title: Screen 08 手账 · 相册墙 UI 设计要点
slug: screen-08-photo-wall
created: 2026-08-23
tags: [ui, codesign, react, figma, journal]
sources:
  - "DESIGN.md (Photo Album Mobile UI)"
  - "SCREEN08_PATCH_NOTE.md"
  - "App.jsx PhotoWallScreen implementation"
summary: >-
  Screen 08 是把已有七屏基线延伸到第三层手账场景的关键屏:三段日期分区 +
  Polaroid + WashiTape + ThumbPin + PaperClip 四件套原语,纯内联 SVG,无外部资源。
project: store/project for X/figma
base_confidence: 0.8
provenance:
  extracted: 0.7
  inferred: 0.3
  ambiguous: 0.0
lifecycle_changed: 2026-08-23
---

# Screen 08 · 手账 · 相册墙 UI 设计要点

## Context

Photo Album Mobile UI 项目在七屏基线(屏1-7)验证后,追加的第 8 屏是手账风格的相册墙 — 把已有的回忆(地图上的、回忆时间线上的)以"贴上墙"的方式聚合展示。

## Finding

### 三大分区结构

屏8 把回忆按"日期编号"组织成三段:

| 段 | 标题 | 数量 | 视觉重点 |
|---|---|---|---|
| 07 | 京都的夏天 | 3 polaroid + washi mint | 雨后桥 / 竹林 / 灯笼 |
| 06 | 海边日落 | 3 polaroid + washi rose | 橘色海 / 脚印贝壳 / 夜空 |
| 05 | 一个人的咖啡馆 | 3 polaroid + washi pink | 拿铁 / 半本书 / 蛋糕 |

### 4 个原语(全部内联 SVG)

- **PaperClip**(回形针,`:-18deg` ~ `:+14deg` 旋转,压在 polaroid 角上)— 金属感灰色,顶层 zIndex 6
- **ThumbPin**(彩色图钉,`#c7502a` / `#69c5d8` / `#f0a04e` / `#58a89f` 等)— 圆头 + 短钉,带 drop-shadow
- **Polaroid**(白色卡纸 + 7px 内边距 + 30px 底部 caption)— 复用屏7 的 `caption/date/scene` props,但用 `width/height/top/left/rotation` 定位
- **WashiTape**(分三段颜色)— 复用屏7 的 `color/rotation/width/top/left/opacity`,这里固定 `opacity=0.85`

### 必须保留的视觉规律

- **cursive 中文标题**(`Snell Roundhand` 栈)在每段左上,带 `transform: rotate(-2deg~-3deg)`
- **贴纸 emoji 行**(✿夏日 / ◐黄昏 / ✦心情)用屏7 的 `StickerChip`
- **hashtag chips**(`#京都的夏天` 等)用屏7 的 `JournalHashtag`,三个一组
- **底部 action row**:编辑 / 排序 / 分享 / 更多(4 个透明按钮,cyan 1.8px 描边)— 与屏7 的编辑/锁/分享/删除结构不同

### 已知九大 bug 修复要点(SCREEN08_PATCH_NOTE 列出的)

1. `JOURNAL_PALETTE.washi.cream` → `washiCream`(JOURNAL_PALETTE 是**扁平**结构,没有 `washi.*` 嵌套)
2. 同样处理 `.washi.mint / .washi.rose / .washi.pink`
3. `<JournalHashtag label=... rotate=... />` → `text=... rotation=...`(props 命名改了)
4. 不要用占位的 `<JournalTopBar />` / `<JournalActionRow />`,内联 SVG 自己画

## Implications

- Screen 08 与 Screen 07 共享 journal 设计 token,但**不复用**屏7 的组件(屏7 是 detail page 单条手账,屏8 是 wall — 模式不同)。
- 所有原语都是纯 SVG + 内联样式,不依赖任何栅格图,完全可移植。
- 屏8 顺利成为屏9 / Screen N 的复用基座:PaperClip / ThumbPin 在任何"贴照片"的场景里都能直接搬。

## Related

- [[codesign-session-jsonl-recovery]] — 屏8 探索过程反复失败后,用 session 日志恢复了源码
- [[concepts/atomic-state-recovery]] — 类似思路:破坏后从二次证据还原