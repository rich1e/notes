
## 疑难问点

> 包含产品逻辑和技术方案

- **使用 uniapp 框架自带 Websocket 连接后端服务，前后端如何协同开发？如何调试？**
- **文件下载后，客户端（Android / iOS）需要保存文件多久？**
- **下次打开 app 是否显示已下载文件？如果 uniapp 框架不支持，如何展示？**
- **文件批量下载、批量暂停的技术方案是什么？能否满足产品需求？**
- **文件是否需要支持断点续传？**

## 模块划分

- Notification
- Download List
- E-Mail

## 页面功能

- 页面列表增删改查，以及批量删除、批量已读
- 页面列表支持分页、指定每页条目、总数
- 页面详情增删改查

## 列表展示

不同模块，列表内部展示样式不同，操作按钮也不同。

![[assets/2024/Message Center - App/IMG-20260430101500594.png]]

![[assets/2024/Message Center - App/IMG-20260430101500631.png]]

![[assets/2024/Message Center - App/IMG-20260430101500662.png]]

## 弹窗展示

![[assets/2024/Message Center - App/IMG-20260430101500690.png]]

![[assets/2024/Message Center - App/IMG-20260430101500719.png]]

## 详情展示

![[assets/2024/Message Center - App/IMG-20260430101500746.png]]

![[assets/2024/Message Center - App/IMG-20260430101500774.png]]

## 消息推送

Message Center **入口 Icon** 、**下拉弹窗**和**页面列表 title** 需要显示消息数目、任务状态（下载中/已完成/toast提示），与后端讨论将使用 `Web Socket` 技术实现。

![[assets/2024/Message Center - App/IMG-20260430101500827.png]]

![[assets/2024/Message Center - App/IMG-20260430101500856.png]]

![[assets/2024/Message Center - App/IMG-20260430101500884.png]]