# 融智图谱（前端）部署说明

本项目的前端基于`nginx`实现，但需要注意的是nginx在kylin v10国产服务器上并不能直接安装，需要通过编译安装来实现安装。以下是前端部署使用说明：

## 安装nginx

### 一、 编译环境配置

执行如下命令，安装依赖包。

```sh
yum install gcc gcc-c++ make unzip pcre pcre-devel zlib zlib-devel libxml2 libxml2-devel  readline readline-devel ncurses ncurses-devel perl-devel perl-ExtUtils-Embed openssl-devel -y
```

### 二、编译源代码

#### 1) 执行以下命令，获取安装包。

```sh
wget -c http://nginx.org/download/nginx-1.16.1.tar.gz
```

#### 2) 执行以下命令，解压安装包。

```sh
tar -zxvf nginx-1.16.1.tar.gz
```

#### 3) 执行以下命令，进入安装目录。

```sh
cd nginx-1.16.1
```

#### 4) 执行以下命令，编译安装nginx。

```sh
./configure
```

[![](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154314569-1459132140.png)](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154313912-565451428.png)

```sh
make -j4 && make install
```

[![](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154315882-997602911.png)](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154315195-327093492.png)

### 三、 测试已完成编译的软件

#### 1) 新增nginx用户

```sh
useradd nginx
```

#### 2) 执行以下命令，给nginx用户开启nginx安装目录权限。

```sh
chown nginx:nginx /usr/local/nginx
```

#### 3) 执行如下命令，查看nginx版本。

```sh
cd /usr/local/nginx/sbin/
./nginx -v
```

[![image](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154317015-471278630.png)](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154316516-112826154.png)

#### 4)启动nginx

```sh
cd /usr/local/nginx/sbin/
./nginx
```

[![image](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154318048-1252586630.png)](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154317499-1666288168.png)

#### 5)查看是否启动成功

```sh
ps -ef | grep nginx
```

[![image](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154319056-1524829242.png)](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154318538-1415576266.png)

最后在网页上访问自己的IP就可以了默认端口为80（出现如下欢迎界面就成功了！）

[![image](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154320230-961163220.png)](https://img2022.cnblogs.com/blog/2203909/202207/2203909-20220727154319608-317871596.png)

## 部署前端

我们的前端是静态网页，由`index.html`、`logo.png`、`style.css`三个文件组成。

![](https://img2023.cnblogs.com/blog/2910984/202309/2910984-20230911142505220-1677670470.png)

将其放至服务器`/usr/local/nginx/html`目录下即可输入ip地址访问网页。

![](https://img2023.cnblogs.com/blog/2910984/202309/2910984-20230911142254982-911479859.png)