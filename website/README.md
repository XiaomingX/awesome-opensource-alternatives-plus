# 网站说明

本网站基于 [Docusaurus 2](https://docusaurus.io/) 构建，这是一个现代化的静态网站生成器。

### 安装依赖

运行以下命令安装所需依赖：

```bash
$ yarn
```

### 本地开发

运行以下命令启动本地开发环境：

```bash
$ yarn start
```

运行后将启动一个本地开发服务器，并自动在浏览器中打开页面。大多数代码更改无需重启服务器即可实时生效。

### 构建

运行以下命令生成静态文件：

```bash
$ yarn build
```

该命令会将生成的静态内容放入 `build` 文件夹中，可以通过任何静态文件托管服务进行部署。

### 部署

**使用 SSH 部署：**

```bash
$ USE_SSH=true yarn deploy
```

**不使用 SSH 部署：**

```bash
$ GIT_USER=<你的 GitHub 用户名> yarn deploy
```

如果使用 GitHub Pages 进行托管，上述命令可以快速构建网站并推送到 `gh-pages` 分支。