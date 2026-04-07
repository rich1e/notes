技术栈

- Vue 3.0
- Pnpm & Changesets

## 项目初始化

```sh
mkdir monorepo-starter && cd monorepo-starter
git init
git config --local user.name 'your-name'
git cofnig --local user.email 'your-email'
```

```sh
touch .gitignore .editorconfig .npmrc pnpm-workspace.yaml
echo 'node_modules' >> .gitignore
echo 'shamefully-hoist = true' >> .npmrc
```

```ini
# EditorConfig is awesome: https://EditorConfig.org

# top-most EditorConfig file
root = true

# Unix-style newlines with a newline ending every file
[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

# Matches multiple files with brace expansion notation
# 2 space indentation
[*.{js,ts,jsx,tsx,vue,md}]
indent_style = space
indent_size = 2

# Matches the exact files either package.json or .travis.yml
[{package.json,.travis.yml}]
indent_style = space
indent_size = 2
```

```

```yaml
packages:
  # all packages in direct subdirs of packages/
  - 'packages/*'
  # all packages in subdirs of components/
  - 'components/**'
  # exclude packages that are inside test directories
  - '!**/test/**'
```

[pnpm-workspace.yaml](https://pnpm.io/zh/pnpm-workspace_yaml)

```sh
npm set --init-license "MIT"
npm set --init-author-email "your-email"
npm set --init-author-name "your-name"
npm init -y
npm pkg set name=firmiana
```

[Creating a package.json file](https://docs.npmjs.com/creating-a-package-json-file)
[npm-pkg](https://docs.npmjs.com/cli/v7/commands/npm-pkg)

## ESLint

```sh
mkdir -p packages/eslint-config && cd packages/eslint-config && npm init -y && npm pkg set name=@firmiana/eslint-config
```

```sh
pnpm add eslint -D -w
pnpm add eslint -D --filter @firmiana/eslint-config
```

```sh
cd packages/eslint-config && npx eslint --init
```

![[assets/2023/Vue3 组件库/IMG-20260403174654592.png]]

默认配置文件 `.eslintrc.js` 如下，将文件名称修改为 `vue-ts.js`。

```js
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'plugin:vue/vue3-essential',
    'standard-with-typescript'
  ],
  overrides: [
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  plugins: [
    'vue'
  ],
  rules: {
  }
}
```

`package.json`

```json
{
  "name": "@firmiana/eslint-config",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "rich1e <yuqigong@outlook.com>",
  "license": "MIT",
  "devDependencies": {
    "@typescript-eslint/eslint-plugin": "^5.0.0",
    "eslint": "^8.35.0",
    "eslint-config-standard-with-typescript": "^34.0.0",
    "eslint-plugin-import": "^2.25.2",
    "eslint-plugin-n": "^15.0.0",
    "eslint-plugin-promise": "^6.0.0",
    "eslint-plugin-vue": "^9.9.0",
    "typescript": "*"
  }
}
```

至此，就完成了一个规则包的封装，我们在自身项目中使用它。

```sh
pnpm add @firmiana/eslint-config -D -w
```

在根目录下新建 `.eslintrc.js` 文件使用它。

```js
module.exports = {
  root: true,
  extends: "@firmiana/eslint-config",
};
```

再回到代码中选择 js 相关的代码就可以校验出来。

![[assets/2023/Vue3 组件库/IMG-20260403174654602.png]]

编辑器提示和自动修复，还需要安装 `vscode-eslint` 插件并添加以下配置。

```json
// .vscode/settings.json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

> Note: 配置完成后如果没有生效，重启 vscode 就可以了。

## Stylelint

```sh
pnpm add stylelint postcss -D -w
pnpm add stylelint postcss -D --filter @firmiana/stylelint-config
```


```sh
# 默认规则集
pnpm add stylelint-config-standard --filter @firmiana/stylelint-config
# 属性书写顺序规则集
pnpm add stylelint-order --filter @firmiana/stylelint-config
```

## Commitizen & Commitlint

## Husky & Lint-staged

```sh
npx husky add .husky/commit-msg "npx --no-install commitlint --edit $1"

npx husky add .husky/pre-commit "npx lint-staged"
```

[Husky Automatic (recommended)](https://typicode.github.io/husky/#/?id=automatic-recommended)

## Changesets

```sh
pnpm add -Dw @changesets/cli
```

```sh
git remote add origin git@github.com:rich1e/monorepo-starter.git
git branch -M main
git push -u origin main
```

参考

[从零搭建属于你自己的前端规范+自动化部署 - 掘金](https://juejin.cn/post/7207617774633107512)
[从零搭建属于你自己的前端规范+自动化部署 - 掘金](https://juejin.cn/post/7207617774633107512?)
[VUE3+TS项目内集成ESLint、Prettier、Stylelint、husky 、lint-staged以及Commitizen](https://juejin.cn/post/7205094404415488058)

[探索前端工程化，快速实现组件库开发 - \_小九的专栏 - 掘金](https://juejin.cn/column/7140103294965252109)
[🌳 巨树：基于ztree封装的 Vue 树形组件，轻松实现海量数据的高性能渲染。](https://github.com/tower1229/Vue-Giant-Tree)

[Element-plus组件二次封装项目实现过程 - 简书](https://www.jianshu.com/p/2ad8835b2e8b)
> - 伸缩菜单组件
> - 图标选择器组件
> - 表单组件
> - 弹窗表单组件
> - 表格组件
> - 日历组件

```ad-note
title: JSX & TSX

https://juejin.cn/post/6844903967361613832#heading-6
https://juejin.cn/post/6844903903201329166
https://juejin.cn/post/6916474993635229704
https://github.com/formilyjs/element-plus/blob/main/packages/components/src/submit/index.ts
https://cn.vuejs.org/api/render-function.html#h
https://blog.csdn.net/qq_21567385/article/details/108965319
https://juejin.cn/post/7188054070152822845
https://github.com/vuejs/babel-plugin-jsx
```

```ad-note
title: components

https://element-plus.org/zh-CN/component/button.html#button-%E5%B1%9E%E6%80%A7
https://juejin.cn/post/7181712900094951483
https://juejin.cn/post/7136467262826872868
https://juejin.cn/post/7137107018938056734#heading-1
https://juejin.cn/post/7113562222852309023
https://ououe.com/lib/element-pro-components.html
https://ououe.com/lib/components-helper.html
https://github.com/tolking/components-helper
https://github.com/tolking/element-pro-components/blob/main/package.json
https://github.com/jimbojsb/launchrocket
https://www.cnblogs.com/mate-ui/p/16969085.html

```

```ad-note
title: vuepress

https://vuepress.github.io/zh/reference/plugin/back-to-top.html
https://github.com/vuepress/vuepress-next/blob/61ee4e4f54c16746c3518f14f27d444ceea130c3/ecosystem/plugin-back-to-top/src/client/components/BackToTop.ts
https://xie.infoq.cn/article/af3e1ee1d2ecedbb5a84ea241
https://github.com/JS-banana/jack/blob/master/docs/.vuepress/enhanceApp.js
https://www.jianshu.com/p/650c3566de13
https://demo-block.seepine.com/guide/get-started.html
https://github.com/seepine/vuepress-plugin-demo-block-vue3
https://xinlei3166.github.io/vuepress-demo/guide/
https://juejin.cn/post/7145066680862031885
https://juejin.cn/post/7123094278619791367#heading-5
https://juejin.cn/post/7008361646968012808#heading-9
https://github.com/wocwin/t-ui-plus/blob/2bff18a21d8383a92f482b9fadbe9b8e9a0e41f2/packages/button/src/index.vue
http://localhost:8081/

```

```md
https://element-plus.org/zh-CN/component/button.html#button-%E5%B1%9E%E6%80%A7
https://juejin.cn/post/7181712900094951483
https://juejin.cn/post/7136467262826872868
https://juejin.cn/column/7130951037547970567
https://juejin.cn/post/7140639347937640479
https://juejin.cn/post/7136800894742036517#heading-11
https://stylelint.io/user-guide/cli/
https://github.com/stylelint/awesome-stylelint#custom-syntaxes
https://github.com/constverum/stylelint-config-rational-order
https://juejin.cn/post/7113562222852309023
https://ououe.com/lib/element-pro-components.html
https://ououe.com/lib/components-helper.html
https://github.com/tolking/components-helper
https://github.com/tolking/element-pro-components/blob/main/package.json
https://github.com/jimbojsb/launchrocket
https://www.cnblogs.com/mate-ui/p/16969085.html
https://vuepress-community.netlify.app/zh/
https://juejin.cn/post/7093920481899708447#heading-3
https://github.com/mqyqingfeng/Blog/issues/250
https://morioh.com/p/7a1e5ee5da30
https://www.cnblogs.com/zlp520/p/16615744.html
https://blog.csdn.net/qq_44209274/article/details/126683921
https://juejin.cn/post/7184392660939964474#heading-5
https://typescript-eslint.io/linting/typed-linting/monorepos/#one-tsconfigjson-per-package-and-an-optional-one-in-the-root
https://pnpm.io/zh/using-changesets
https://prettier.io/docs/en/install.html
https://github.com/prettier/eslint-config-prettier#installation
https://www.cnblogs.com/guwufeiyang/p/15882386.html
https://stackoverflow.com/questions/64116378/error-while-loading-rule-typescript-eslint-dot-notation
https://typicode.github.io/husky/#/?id=automatic-recommended

```

```md
https://vuepress.github.io/zh/reference/cli.html#dev
https://github.com/vuepress/vuepress-next/blob/61ee4e4f54c16746c3518f14f27d444ceea130c3/ecosystem/plugin-back-to-top/src/client/components/BackToTop.ts
https://xie.infoq.cn/article/af3e1ee1d2ecedbb5a84ea241
https://github.com/JS-banana/jack/blob/master/docs/.vuepress/enhanceApp.js
https://www.jianshu.com/p/650c3566de13
https://demo-block.seepine.com/guide/get-started.html#%E4%BD%9C%E7%94%A8
https://github.com/seepine/vuepress-plugin-demo-block-vue3/issues/1
https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/alert.md
https://juejin.cn/post/7145066680862031885
https://juejin.cn/post/7123094278619791367#heading-5
https://juejin.cn/post/7008361646968012808#heading-12
https://github.com/wocwin/t-ui-plus/blob/master/docs/.vitepress/config.ts
https://github.com/xinlei3166/vuepress-plugin-demoblock-plus
https://github.com/seepine/vuepress-plugin-demo-block-vue3
https://element-plus.org/zh-CN/component/button.html
https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/affix.md

```
