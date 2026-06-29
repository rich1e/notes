# Node Commands

## npm

```node
npm install (with no args in a package dir)

npm install <tarball file>

npm install <tarball url>

npm install <folder>

npm install [@<scope>/]<name> [--save|--save-dev|--save-optional] [--save-exact]

npm install [@<scope>/]<name>@<tag>

npm install [@<scope>/]<name>@<version>

npm install [@<scope>/]<name>@<version range>

npm i (with any of the previous argument usage)
```

> [Command-line API | Node.js v20.2.0 Documentation](https://nodejs.org/api/cli.html)

## nvm

```sh
# 查询最新稳定版
nvm ls-remote | grep 'Latest LTS'
# 查看可用的（可下载的）全部node版本
nvm ls available
# 列出所有安装的版本
nvm ls
# 安装最新版本的 node
nvm install latest
# 安装当前稳定的 Node.js LTS 版本
nvm install --lts
```

> nvm 软件包 windows 平台的命令和其它平台的有区别

## lerna

```sh
# 清空 node_modules
lerna clean
```

## yarn workspace

```node
yarn workspace [package-name] [action] [...pkg]
```

[yarn workspace](https://yarnpkg.com/cli/workspace)
[Monorepo最佳实践之Yarn Workspaces - 掘金](https://juejin.cn/post/7011024137707585544)

## pnpm

```sh
pnpm init

# 安装公共依赖
pnpm install typescript -w -D

# 为某个项目安装依赖
pnpm --filter <workspace> <command>
# 缩写
pnpm -F <workspace> <command>

# Example
pnpm --filter math-lib add lodash
pnpm --filter math-lib add -D typescript @types/lodash
pnpm --filter calculator run test

# Support glob pattern
pnpm --filter pkg* run test

# 安装本地依赖
pnpm --filter calculator add math-lib --workspace

# List all workspaces in JSON format
pnpm m ls --depth -1 --json

# 列出这个包的源码位置，被monorepo内部哪些项目引用
pnpm why vue
```

## 镜像源

查看镜像源

```sh
npm config get registry
yarn config get registry
pnpm config get registry
```

设置镜像源

```sh
npm config set registry <registry-url>
yarn config set registry <registry-url>
pnpm config set registry <registry-url>
```

常用镜像

```sh
npm --- https://registry.npmjs.org/
cnpm --- https://r.cnpmjs.org/
taobao --- https://registry.npm.taobao.org/

# 淘宝镜像设置
npm config set registry https://registry.npmmirror.com/

# node-sass 淘宝镜像设置
npm config set sass_binary_site https://npm.taobao.org/mirrors/node-sass/
yarn config set sass_binary_site https://npm.taobao.org/mirrors/node-sass/
pnpm config set sass_binary_site https://npm.taobao.org/mirrors/node-sass/

# Chrome Driver 淘宝镜像设置
npm config set CHROMEDRIVER_CDNURL https://npm.taobao.org/mirrors/chromedriver

# Electron 淘宝镜像设置
npm config set ELECTRON_MIRROR http://npm.taobao.org/mirrors/electron/
npm config set ELECTRON_BUILDER_BINARIES_MIRROR https://npm.taobao.org/mirrors/electron-builder-binaries/
```

## 相关笔记

- [[buckets/work-records/javascript-async-await]] — async/await 原理（Generator + Promise）
- [[buckets/work-records/shell-scripts]] — Shell 脚本（node_modules 清理）
- [[buckets/work-records/command-tldr]] — tldr（node 客户端）
