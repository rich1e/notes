---
title: iOS 网络编程
category: skills
tags: [ios, networking, urlsession, alamofire, rest, swift]
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-07-01T00:00:00Z
summary: iOS REST API 调用：URLSession（原生）与 Alamofire（第三方库）的 GET/POST 请求、JSON 解码、连接可达性检测（SCNetworkReachability）、App Transport Security 配置。
base_confidence: 0.86
lifecycle: draft
lifecycle_changed: "2026-07-01"
tier: supporting
provenance:
  extracted: 0.88
  inferred: 0.12
  ambiguous: 0.00
---

# iOS 网络编程

## REST 基础

REST（Representational State Transfer）是移动端与服务器通信的主流架构。

**HTTP 方法**：

| 方法 | 用途 | 是否有 Body |
|---|---|---|
| GET | 获取资源 | 否 |
| POST | 创建资源 | 是 |
| PUT | 替换资源 | 是 |
| PATCH | 部分更新 | 是 |
| DELETE | 删除资源 | 否 |

**常用内容类型**：JSON（最普遍）、XML、Binary（文件上传）。

## URLSession（原生）

### 基本 GET 请求

```swift
func fetchData(from urlString: String) async throws -> Data {
    guard let url = URL(string: urlString) else {
        throw URLError(.badURL)
    }
    let (data, response) = try await URLSession.shared.data(from: url)
    guard let http = response as? HTTPURLResponse,
          (200...299).contains(http.statusCode) else {
        throw URLError(.badServerResponse)
    }
    return data
}
```

### JSON 解码（Codable）

```swift
struct User: Codable {
    let id: Int
    let name: String
    let email: String
}

func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://jsonplaceholder.typicode.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}
```

### POST 请求

```swift
func createPost(title: String, body: String) async throws -> Post {
    var request = URLRequest(url: URL(string: "https://api.example.com/posts")!)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.httpBody = try JSONEncoder().encode(["title": title, "body": body])

    let (data, _) = try await URLSession.shared.data(for: request)
    return try JSONDecoder().decode(Post.self, from: data)
}
```

### URLSession 配置

```swift
let config = URLSessionConfiguration.default
config.timeoutIntervalForRequest = 30
config.waitsForConnectivity = true   // 等待网络恢复
let session = URLSession(configuration: config)
```

## 连接可达性检测

```swift
import SystemConfiguration

class Reachability {
    static func isConnectedToNetwork() -> Bool {
        var zeroAddress = sockaddr_in()
        zeroAddress.sin_len = UInt8(MemoryLayout<sockaddr_in>.size)
        zeroAddress.sin_family = sa_family_t(AF_INET)

        guard let reachability = withUnsafePointer(to: &zeroAddress, {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
                SCNetworkReachabilityCreateWithAddress(nil, $0)
            }
        }) else { return false }

        var flags: SCNetworkReachabilityFlags = []
        SCNetworkReachabilityGetFlags(reachability, &flags)
        return flags.contains(.reachable) && !flags.contains(.connectionRequired)
    }
}
```

## Alamofire（第三方库）

Alamofire 是 Swift HTTP 网络库，封装了 URLSession，语法简洁：

```swift
// 添加 SPM 依赖：https://github.com/Alamofire/Alamofire
import Alamofire

// GET 请求
AF.request("https://api.example.com/users")
    .validate(statusCode: 200..<300)
    .responseDecodable(of: [User].self) { response in
        switch response.result {
        case .success(let users):
            print("Fetched \(users.count) users")
        case .failure(let error):
            print("Error: \(error)")
        }
    }

// POST 请求
let parameters = ["username": "alice", "password": "secret"]
AF.request("https://api.example.com/login",
           method: .post,
           parameters: parameters,
           encoding: JSONEncoding.default)
    .responseDecodable(of: AuthResponse.self) { response in
        // handle response
    }
```

**Alamofire vs URLSession**：URLSession 无需外部依赖，适合简单场景；Alamofire 提供请求链式、自动重试、文件上传进度等高级功能。

## App Transport Security（ATS）

iOS 9+ 默认强制 HTTPS。如需访问 HTTP 端点，在 `Info.plist` 配置：

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <!-- 允许所有 HTTP（开发环境，上线前必须移除）-->
    <key>NSAllowsArbitraryLoads</key>
    <true/>
    
    <!-- 或仅允许特定域名 -->
    <key>NSExceptionDomains</key>
    <dict>
        <key>api.example.com</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <true/>
        </dict>
    </dict>
</dict>
```

⚠️ App Store 审核会检查 ATS 豁免，滥用会被拒绝。

## 认证头与 Token

```swift
var request = URLRequest(url: url)
request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
request.setValue("application/json", forHTTPHeaderField: "Accept")
```

## 关联页面

- [[concepts/swift-concurrency]] — async/await 与 URLSession
- [[skills/ios-multithreading]] — 网络请求线程调度（GCD）
- [[concepts/swift-fundamentals]] — Codable 协议
- [[entities/ios17-app-development-book]] — 来源书籍
