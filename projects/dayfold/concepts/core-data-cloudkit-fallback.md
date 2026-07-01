---
title: Core Data + CloudKit 降级策略
category: project
tags: [ios, core-data, cloudkit, error-handling]
sources: [projects/dayfold]
summary: >-
  NSPersistentCloudKitContainer 在无 iCloud 账号时返回 134400
  (CKAccountStatusNoAccount)，用 description.cloudKitContainerOptions = nil 二次加载
  回退到纯本地存储。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-06-29
tier: supporting
created: 2026-06-29T00:00:00Z
updated: 2026-06-29T00:00:00Z
---

# Core Data + CloudKit 降级策略

文件：`dayfold/dayfold/Services/CoreDataStack.swift`

## 关键问题

`NSPersistentCloudKitContainer` 在模拟器或未登录 iCloud 的真机上启动时，`loadPersistentStores`
会失败并报 **`NSCocoaErrorDomain` code `134400`**（即 `CKError.Code.accountTemporarilyUnavailable`
对应 `CKAccountStatusNoAccount`）。如果不处理，CloudKit 镜像会反复进入 recovery 循环，
刷满错误日志。

## 实现

```swift
description.cloudKitContainerOptions = NSPersistentCloudKitContainerOptions(
    containerIdentifier: "iCloud.com.Yuqi.dayfold"
)

container.loadPersistentStores { storeDescription, error in
    if let error = error as NSError? {
        if error.domain == NSCocoaErrorDomain, error.code == 134400 {
            description.cloudKitContainerOptions = nil  // 关键：清空 CloudKit 选项
            container.loadPersistentStores { _, retryError in
                if let retryError {
                    print("Core Data failed to load: \(retryError.localizedDescription)")
                } else {
                    print("Core Data loaded successfully (local only)")
                }
            }
        } else {
            print("Core Data failed to load: \(error.localizedDescription)")
        }
    } else {
        print("Core Data loaded successfully")
        self.checkCloudKitAvailability()
    }
}
```

## 设计要点

- **不是 `try!`**：用 closure 形式才能在错误回调里做降级；`try!` 直接 crash。
- **必须先清空 `cloudKitContainerOptions = nil` 再二次 `loadPersistentStores`**，否则
  仍然以 CloudKit 模式启动。`description` 是 `container.persistentStoreDescriptions.first`
  引用，修改它会作用在容器的同一对象上。
- **降级只触发一次**：第二次 `loadPersistentStores` 不会再失败（本地 store 无网络依赖）。
- **`automaticallyMergesChangesFromParent = true`**：保证多 context 的写入合并到 viewContext。
- **`mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy`**：合并冲突时以内存属性为准
  （适合本地编辑优先的场景）。
- **历史跟踪 + 远程变更通知**：

  ```swift
  description.setOption(true as NSNumber, forKey: NSPersistentHistoryTrackingKey)
  description.setOption(true as NSNumber,
      forKey: NSPersistentStoreRemoteChangeNotificationPostOptionKey)
  ```

  CloudKit 镜像把另一设备的写入落到 store 后，会触发
  `.NSPersistentStoreRemoteChange` → `viewContext` 自动 `mergeChanges` → `@FetchRequest`
  列表刷新。

## 状态暴露

- `@Published var isCloudKitAvailable = false`：在 `checkCloudKitAvailability()` 内
  `CKContainer(identifier:).accountStatus` 异步拿到 `.available` 时设为 true；UI 可据此
  显示同步状态徽章（目前尚未在 UI 暴露）。

## 已知细节 ^[inferred]

- 降级到本地后，已写入的本地数据**不会**自动迁移到 iCloud；用户后来登录 iCloud 也只能
  看到新数据。这是 CloudKit container 的预期行为，不是 bug。
- `NSPersistentCloudKitContainerOptions` 用 nil 清空，比"不创建带 options 的 description"
  改动更小，避免回退路径要重写整个 `lazy` 容器初始化逻辑。
