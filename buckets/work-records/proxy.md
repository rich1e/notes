# Proxy

## subconverter（订阅转换）

Run the container detached, forward internal port 25500 to host port 25500

```sh
docker run -d --restart=always -p 25500:25500 tindy2013/subconverter:latest
```

Check its status

```sh
curl http://localhost:25500/version
```

## 相关笔记

- [[buckets/work-records/mac-tips]] — Mac 技巧（HTTPS 证书配置）
