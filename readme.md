# Forum

现网： [http://193.112.177.163](http://193.112.177.163)

一个简单的论坛项目。前端通过 vue + vuex + vue-router + axios + ElementUI + SCSS + webpack 开发，后端通过 python + flask + mysql 开发，最后通过 supervisor + gunicorn + nginx 实现服务器部署。

实现的功能有：

- [x] 用户登录/注册/注销
- [x] 用户主页/设置
- [x] 话题发表，话题删除（用户删除自己的话题），话题修改
- [x] 话题支持插入图片
- [x] 话题支持 markdown
- [x] 回复发表，回复删除
- [x] 用户通过在回复中 '@[用户名]' 可通知用户
- [x] 用户关注/取消关注
- [x] 支持游客模式


## 结构

	.
	├── misc
	├── server
	│   ├── models
	│   ├── images
	│   ├── routes
	│   ├── markdown_demo.md
	│   ├── app.py
	│   ├── config.py (需要自己配置，包含数据库的 database，密码，密钥)
	│   ├── reset.py
	│   └── utils.py
	├── view (这个 view 目录是编译后的文件）
	│   ├── static
	│   └── index.html
	├── get-pip.py
	├── deploy.sh
	├── database_secret.conf
	├── server.conf
	├── view.nginx
	└── wsgi.py


## 跨域

### 开发环境

前端项目中通过设置 webpack config 中的 proxyTable 解决开发中的跨域问题：

    dev: {
        ...
        proxyTable: {
            '/api': {
                target: 'http://127.0.0.1:2000',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        },
        ...
    }

### 部署

通过 nginx 的代理解决跨域问题:

    server {
        ...

        location /api {
            ...
            proxy-pass http://localhost:2000;
        }
    }


## 开发

### 后端

启动服务器，服务在 localhost:2000 可被访问

    python app.py


### 前端

安装

    npm install

运行，在浏览器访问 localhost:8080 可查看前端页面

    npm start

打包编译

    npm run build

查看编译报告

    npm run build --report

在dist文件夹下生成结果。

### 部署

将前端编译之后生成的 dist 文件夹改名为 view，并与 server 一起，上传到 linux 服务器的同级目录下。

之后，将本项目根目录下的：

	.
	├── get-pip.py
	├── deploy.sh
	├── database_secret.conf
	├── server.conf
	├── view.nginx
	└── wsgi.py

也与 view，server 放在同级目录下，执行

    bash deploy.sh

开始部署

部署完成之后，访问服务器的地址即可进入论坛。