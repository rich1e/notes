---
title: 新增业务组件三仓 SOP — 实操清单
category: skills
tags:
  - design-system
  - f2e
  - designable
  - formily
  - koa
  - ai-coding
sources:
  - "_raw/2026-08-07-153809-flowimage-1.txt (Claude Code 多仓会话, 2026-08-07)"
created: 2026-08-07T15:38:09Z
updated: 2026-08-07T15:38:09Z
summary: 在ACME 司 商品中心新增一个 display 类业务组件（如 terms-card）的 9 步可执行清单：核心仓建目录与 6 文件、注册到 preview/config.ts、tsc 校验、BFF 仓建 config+schema、注册到 components/index.ts、curl 验证 query-config、改 proxy target 联调、强制刷新验证、改回 target。
tier: core
lifecycle: draft
lifecycle_changed: "2026-08-07"
base_confidence: 0.88
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[projects/flow-design-system/flow-design-system]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/triple-repo-component-contract]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/designable-iframe-component-bridge]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-component-library-runtime]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/dynamic-require-resolveweak-loading]]"
    type: related_to
---

# 新增业务组件三仓 SOP — 实操清单

> 完整 9 步 SOP 详见 [[projects/flow-design-system/concepts/triple-repo-component-contract]]。本页是**可逐条 copy-paste 跑**的操作清单，以「保险条款卡片 `terms-card`」为案例。

## 准备

```bash
# 三个仓的本地路径（你机器上的实际位置）
CORE_REPO=/Users/rich1e/workspace/code/acme-dplatform-flow-v2-core
DESIGNER_REPO=/Users/rich1e/workspace/code/acme-dplatform-flow-v2
BFF_REPO=/Users/rich1e/workspace/code/acme-core-goods-ai

# 组件三要素（决定目录名 + name + title）
COMP_NAME=terms-card
COMP_TITLE="保险条款卡片"
COMP_CATEGORY=DISPLAY   # CATEGORIES_KEY.DISPLAY = 'display'
```

## 步骤 1-5：核心仓（运行时）

```bash
cd $CORE_REPO

# 1. 建组件目录
mkdir -p src/modules/template/builtin-components/$COMP_NAME

# 2. 写 config.ts
cat > src/modules/template/builtin-components/$COMP_NAME/config.ts <<EOF
import type { DesignableComponent } from '../types';
import schema from './schema';
import { CATEGORIES_KEY } from '../types';

const config: DesignableComponent = {
  name: '$COMP_NAME',
  title: '$COMP_TITLE',
  schema,
  categories: [CATEGORIES_KEY.$COMP_CATEGORY],
};

export default config;
EOF

# 3. 写 schema.ts（按业务需求手写 Formily schema）

# 4. 写 index.ts
cat > src/modules/template/builtin-components/$COMP_NAME/index.ts <<EOF
import './style.scss';
import ${COMP_NAME//-/_} from './${COMP_NAME//-/_}';  # PascalCase
export default ${COMP_NAME//-/_};
EOF

# 5. 写 组件主体（PascalCase.tsx）+ style.scss + types.ts
```

## 步骤 6：核心仓内的「设计器侧注册中心」

```bash
cd $CORE_REPO

# 6a. 追加 import
# 找到 preview/config.ts 末尾的 import 块
# 在 TermsDisplay 之后追加：import TermsCardConfig from '../template/builtin-components/terms-card/config';
# 实际改法：用 Edit 工具精准编辑，避免破坏其他 import

# 6b. 追加到 components 数组
# 找到 components 数组（DESIGNABLE_INITIALIZE_MESSAGE 内）
# 在 TermsDisplay 之后追加 TermsCardConfig
```

## 步骤 7（可选但推荐）：核心仓 llm-wiki 文档

```bash
cd $CORE_REPO

# 7a. 写组件文档（按 llm-wiki/TEMPLATE.md 规范）
cat > llm-wiki/docs/$COMP_NAME.md <<EOF
---
name: $COMP_NAME
title: $COMP_TITLE
categories: [$(echo $COMP_CATEGORY | tr '[:upper:]' '[:lower:]')]
updated: $(date +%Y-%m-%d)
---

# $COMP_TITLE ($COMP_NAME)

## 用途
<!-- 一句话说明 -->

## 配置项速览
<!-- 列出 schema.ts 的主要 props -->

## 关键配置组
<!-- 详细说明 -->
EOF

# 7b/c. 更新索引与分类表
# llm-wiki/wiki/index.md 索引表追加一行
# llm-wiki/wiki/categories.md 分类表追加一行
```

## 步骤 8（设计器侧，仅当 CORE 源生效时）

```bash
# 核心仓 dev server 必须重启
cd $CORE_REPO
npm run dev  # 或 npm run dev:ssr

# 浏览器 Cmd+Shift+R 强制刷新
# 在 DevTools Console 验证：
#   window.addEventListener('message', e => {
#     if (e.data?.type === 'INITIALIZE') {
#       console.log(e.data.payload.components.filter(c => c.name === '$COMP_NAME'));
#     }
#   });
# 应该看到该组件的对象（含 categories: ['$([\$]COMP_CATEGORY | tr A-Z a-Z)']）
```

## 步骤 9：BFF 后端（仅当 AI 源生效时）

判定条件（设计器 URL `tenantFrom ∈ {tenantA, tenantB}` 且 `versionNum≠3` 且 `gcVersion≠v3`）。若是：

```bash
cd $BFF_REPO

# 9a. 建组件目录
mkdir -p app/controller/component-library/library/components/$COMP_NAME

# 9b. 写 config.ts
cat > app/controller/component-library/library/components/$COMP_NAME/config.ts <<EOF
import type { DesignableComponent } from '../../types';
import { CategoriesKey } from '../../types';
import schema from './schema';

const config: DesignableComponent = {
  name: '$COMP_NAME',
  title: '$COMP_TITLE',
  schema,
  categories: [CategoriesKey.$COMP_CATEGORY],
};

export default config;
EOF

# 9c. 写 schema.ts（与核心仓 builtin-components/$COMP_NAME/schema.ts 字段一一对应）

# 9d. 在汇总数组里追加
# 编辑 app/controller/component-library/library/components/index.ts：
#   - import { ... } from './$COMP_NAME/config';
#   - 在 buildComponents() 数组里紧跟同前缀组件追加
```

## 验证（端到端）

### 核心仓类型校验

```bash
cd $CORE_REPO
npx tsc --noEmit -p tsconfig.json 2>&1 | grep -E "$COMP_NAME|${COMP_NAME//-/_}"
# 期望：空输出（零类型错误；项目既有的 node_modules/libpag 报错与本组件无关）
```

### BFF 接口验证

```bash
# 启动 BFF
cd $BFF_REPO && pnpm dev    # 默认 8080

# 验证 query-config 包含新组件
curl -s -X POST http://localhost:8080/public/v1/component-library/query-config \
     -H "Content-Type: application/json" -d '{"isLimitUser":false}' \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
comps = d['data']['components']
print('total:', len(comps))
print('$COMP_NAME in list?', any(c['name']=='$COMP_NAME' for c in comps))
print('同前缀组件:', [c['name'] for c in comps if '$(echo $COMP_NAME | cut -d- -f1)' in c.get('name','')])
"
```

### BFF 单组件验证

```bash
curl -s -X POST http://localhost:8080/public/v1/component-library/components/query-schema \
     -H "Content-Type: application/json" -d "{\"name\":\"$COMP_NAME\"}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('success:', d.get('success')); print('keys:', list(d.get('data',{}).get('component',{}).keys()))"
```

## 设计器面板显示验证（AI 源路径）

```bash
# 1. 临时改 proxy target 联调本机 BFF
cd $DESIGNER_REPO
# 编辑 config/config.ts：把 'http://8636-w-acme-core-goods-ai.test.example.com' 改成 'http://localhost:8080'

# 2. 重启设计器
npm run dev

# 3. 强制刷新设计器
# Cmd+Shift+R，访问 ?tenantFrom=tenantB&... 的页面
# 展开"展示组件"分组，应看到「$COMP_TITLE」可拖拽节点
```

## 收尾（务必做）

```bash
# 改回 proxy target（否则其他同学会被代理到你的本机）
cd $DESIGNER_REPO
git checkout config/config.ts

# 或用 stash 管理
git stash
# 改完测完
git stash pop
```

## 失败速查

| 现象 | 根因 | 修复 |
|------|------|------|
| 核心仓 `tsc` 报错 | 组件 `index.ts` default export 错 / `types.ts` 漏 export | 查 `index.ts` 与 `types.ts` 边界 |
| BFF 接口 404 | 漏 `/public/v1` 前缀 | 完整路径是 `/public/v1/component-library/query-config` |
| 接口通了但组件不在列表 | `components/index.ts` 数组没追加 | 检查 import + 数组 push 两处 |
| 设计器面板没显示 | 走 AI 源 + BFF 没同步 | Network 看 Server IP 是 test 还是 localhost |
| 改了本地 BFF 设计器看不到 | proxy target 写死 test | 临时改 target，重启 Umi，**记得改回** |
| 改完 target 团队同学报错 | 改完没改回 | `git checkout config/config.ts` 立即回退 |

## 相关页面

- [[projects/flow-design-system/flow-design-system]] — 项目总览
- [[projects/flow-design-system/concepts/triple-repo-component-contract]] — 9 步完整 SOP 详解
- [[projects/flow-design-system/concepts/designable-iframe-component-bridge]] — iframe 桥
- [[projects/flow-design-system/concepts/ai-component-library-runtime]] — BFF controller
- [[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]] — 双源路由
- [[projects/flow-design-system/concepts/dynamic-require-resolveweak-loading]] — 运行时加载机制
