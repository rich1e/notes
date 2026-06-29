# Mac Tips

## 快捷键

`Cmd + Shift + .` 查看隐藏文件

## 添加本地 HTTPS 证书（mkcert）

1. 解压 `mkcert.zip` 到任何地方

2. 获取 `mkcert` 的目录, 例如在 `/your-path/mkcert`

3. 执行 `export CAROOT="/your-path/mkcert"`

4. 安装 `mkcert`

```shell
# build from source code
git clone https://github.com/FiloSottile/mkcert && cd mkcert
go build -ldflags "-X main.Version=$(git describe --tags)"
```

5. 安装 `CA Certs`, 执行 `mkcert -install`

## 相关笔记

- [[buckets/work-records/proxy]] — 代理配置（本地网络相关）
- [[buckets/work-records/windows-settings]] — Windows 环境设置（对比参考）
