
## 疑难问点

> 包含产品逻辑和技术方案

- **Message Center 入口 icon 消息数目与页面 title 显示的数目，之间的内在逻辑是什么？**
- **文件批量下载、批量暂停的技术方案是什么？能否满足产品需求？**
- **Notification Management 发布消息时，发布时间的验证逻辑是在哪个操作步骤中？如何交互？**

## 模块划分

- Notification
- Download List
- E-Mail
- Notification Management

## 页面功能

- 页面列表增删改查，以及批量删除、批量已读
- 页面列表支持分页、页码、指定每页条目、总数
- 页面详情增删改查

## 列表展示

不同模块，列表内部展示样式不同，操作按钮也不同。

![[assets/2024/Message Center - WEB/IMG-20260403174655005.png]]

![[assets/2024/Message Center - WEB/IMG-20260403174655018.png]]

![[assets/2024/Message Center - WEB/IMG-20260403174655031.png]]

![[assets/2024/Message Center - WEB/IMG-20260403174655044.png]]

## 弹窗展示

![[assets/2024/Message Center - WEB/IMG-20260403174655062.png]]

![[assets/2024/Message Center - WEB/IMG-20260403174655084.png]]

![[assets/2024/Message Center - WEB/IMG-20260403174655100.png]]

![[assets/2024/Message Center - WEB/IMG-20260403174655114.png]]

## 权限功能

进入 Notification Management，需要提供登陆和权限相关的接口。

![[assets/2024/Message Center - WEB/IMG-20260403174655133.png]]

## 消息推送

Message Center **入口 Icon** 、**下拉弹窗**和**页面列表 title** 需要显示消息数目，与后端讨论将使用 `Web Socket` 技术实现。

![[assets/2024/Message Center - WEB/IMG-20260403174655146.png]]

![[assets/2024/Message Center - WEB/IMG-20260403174655169.png]]