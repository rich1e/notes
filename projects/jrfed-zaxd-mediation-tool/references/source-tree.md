---
title: >-
  源码目录布局与模块职责
category: references
tags: [chrome-extension, project-structure, react, typescript]
sources: [projects/jrfed-zaxd-mediation-tool]
summary: >-
  jrfed-zaxd-mediation-tool 源码目录一览：content/ 为核心业务目录，划分 views/components/stores/hooks/utils 五层，背景脚本与侧边栏独立。
provenance:
  extracted: 0.95
  inferred: 0.04
  ambiguous: 0.01
base_confidence: 0.94
lifecycle: active
lifecycle_changed: 2026-07-01
created: 2026-07-01T12:00:00Z
updated: 2026-07-01T12:00:00Z
---

# 源码目录布局

## 顶层结构

```
src/
├── background/          # Service Worker（扩展生命周期事件）
├── content/             # Content Script 核心（主要业务代码）
├── sidepanel/           # SidePanel HTML 入口
├── components/          # 全局共享组件（非 content 专属）
├── assets/              # 静态资源
└── types/               # 全局类型定义
```

## content/ 内部结构

```
content/
├── api/                 # API 环境地址配置（baseapi.tsx）
├── components/          # 公共 UI 组件
│   ├── headerContent/       # 顶部栏
│   ├── menuContent/         # 侧边菜单（含权限过滤）
│   ├── tabsMenu/            # Tab 切换
│   ├── layoutContent/       # 整体布局
│   ├── selectionFloatingWindow/  # 划词浮窗（核心组件）
│   ├── operationRecordModal/     # 操作记录弹窗
│   ├── pageSearch/          # 通用搜索表单
│   ├── summaryContent/      # 汇总展示
│   └── ...（设置、版本检查等辅助组件）
├── config/
│   └── routes.ts            # 前端路由配置（手动注册，非文件路由）
├── hooks/
│   ├── usePermission.ts     # 权限检查 Hook
│   ├── useCurrentComponent.ts  # 当前页面组件
│   └── useShadow.ts         # Shadow DOM
├── stores/
│   ├── userInfoStore.ts     # 登录用户信息
│   ├── menuStore.ts         # 菜单状态 + 权限数据
│   ├── searchParamsStore.ts # 多页面搜索参数联动
│   └── versionStore.ts      # 版本信息
├── styles/
│   ├── global.scss          # 全局样式（Vite additionalData 注入）
│   └── variables.scss       # SCSS 变量（颜色、间距）
├── utils/
│   ├── request.ts           # Axios 封装（Token + 错误处理）
│   ├── storage.ts           # Chrome Storage 封装 + chromeStorage 适配器
│   ├── enum.ts              # 枚举/字典映射常量
│   ├── utils.ts             # 通用工具（roundMoney/maskPhone 等）
│   ├── tracker.ts           # 神策埋点工具函数
│   └── sa.ts                # 神策 SDK 跨世界调用封装
└── views/
    ├── App.tsx              # 应用根组件
    ├── login/               # 登录页
    ├── main/                # 主面板
    ├── earlyRepayment/      # 提前结清
    ├── soothe/              # 安抚金试算
    ├── coupon/              # 优惠券
    ├── rights/              # 权益计算（现行）
    ├── rightsHistory/       # 权益计算（历史订单）
    ├── orderList/           # 外网投诉列表
    ├── identityVerification/ # 征信核身
    ├── supplierTicket/      # 供应商工单
    └── originalOrderRefund/ # 原单退款
```

## 页面目录标准结构

每个 `views/{pageName}/` 目录：

```
views/{pageName}/
├── index.tsx          # 页面入口
├── service.tsx        # API 调用函数（命名：{动词}{业务}Api）
├── data.d.ts          # 类型定义
├── constants.ts       # 页面常量
└── component/         # 页面内子组件
    ├── searchContent/     # 搜索表单
    ├── summary/           # 汇总展示
    └── {featureModal}.tsx # 功能弹窗
```

## 关联页面

- [[projects/jrfed-zaxd-mediation-tool/jrfed-zaxd-mediation-tool]] — 项目总览
