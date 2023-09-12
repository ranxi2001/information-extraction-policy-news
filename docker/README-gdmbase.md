# 梦图数据库使用说明

在此，我们为您提供了如何使用梦图数据库的基本指导。以下是常见的操作和相应的命令行指令。

## 1. 连接到数据库

首先，您可以使用 `tmux` 来创建或连接到一个已存在的会话。

```bash
tmux a -t shell
```

> `tmux` 是一个终端复用器，它允许用户在单个终端窗口中启动多个独立的终端会话。这些会话可以独立运行，并且可以在它们之间轻松切换。此外，`tmux` 提供了会话的持久性，这意味着即使用户从远程连接断开或终端窗口被关闭，会话中运行的进程仍然可以继续运行，稍后用户可以重新连接到这些会话。
>
> 这里是 `tmux` 的一些关键特性和用途：
>
> 1. **会话管理**：创建、删除和切换会话。
> 2. **窗口和面板**：在一个会话中，用户可以创建多个窗口，每个窗口都像一个独立的终端。在窗口内，可以进一步将其划分为多个面板，这些面板在一个屏幕上并排显示。
> 3. **持久性**：在终端或SSH会话断开后，`tmux` 会话仍然存在，允许用户稍后重新连接。
> 4. **复制和粘贴**：在面板和窗口之间复制和粘贴文本。
> 5. **自定义和自动化**：通过 `tmux` 的配置文件，用户可以调整界面和设置按键绑定，以满足自己的需求。
>
> 在远程服务器工作、开发、或多任务操作时，`tmux` 都是一个非常有用的工具。
>
> 在 `tmux` 命令中，`a -t shell` 的含义如下：
>
> - `a`: 这是 `tmux` 命令的一个简写，代表 `attach-session`。这个命令的作用是连接到一个已经存在的 `tmux` 会话。
>
> - `-t shell`: 这里的 `-t` 是 `target-session` 的简写。它指定了要连接的会话的名称或标识符。在这个例子中，我们要连接的会话的名称是 `shell`。
>
> 所以，`tmux a -t shell` 的整体意思是连接到一个名为 `shell` 的已经存在的 `tmux` 会话。如果这个会话不存在，命令会返回一个错误。

接着，使用下列命令来连接到梦图数据库。

```bash
./cypher-shell -a bolt://124.126.103.210:4001 -u SYSDBA -p SYSDBA
```

## 2. 切换到目标数据库

要操作特定的数据库，您可以使用 `:use` 命令。例如，切换到名为 "demo" 的数据库：

```bash
:use demo
```

## 3. 查询数据库

### （1）获取所有节点 (Node)

要检索数据库中的所有节点，您可以使用以下命令：

```bash
MATCH (n)
RETURN n;
```

### （2）获取所有关系 (Link)

要检索数据库中的所有关系（有时也被称为边或链接），您可以使用以下命令：

```bash
MATCH (a)-[r]->(b)
RETURN a,r,b;
```

**结束语**

这只是梦图数据库使用的基础指南。为了深入了解和掌握更多高级功能，建议参考梦图数据库的官方文档或相关的培训材料。如果您在使用过程中遇到任何问题，欢迎随时提问和反馈。

# 附录-GDMBASE部署说明

### 一、tmux命令(第三方工具)

因为图库启动需要多个组件，需要用到tmux工具来进行窗口管理，该工具可以把启动完成的进行挂载在后台运行，常用命令如下：

#### 1、查看所有session

```
tmux ls
```

#### 2、新建session

```
tmux new -s session_name
```

#### 3、进入已创建的session

```
tmux a -t session_name
```

###  二、图库基本操作

#### 1、安装

安装包：`gdmbase_linux.x86_64_v3.3.17.tar.gz`

可以通过解压命令：`tar -zxvf xxx`进行解压，解压完成后目录如下：

![](https://raw.githubusercontent.com/ranxi2001/blog-imgs/main/img/20230912195421.png)

####  2、关于启动

所有启动的相关组件都在bin目录下，启动存储及服务组件，即完成`gdmbase`的启动，启动操作如下

(1).启动存储

在`gdmbase/bin`目录下，执行`./gstore`

(2).启动服务

在`gdmbase/bin`目录下，执行`./cypher-server`

(3).连接图库

在`gdmbase/bin`目录下，执行`./cypher-shell -a bolt://IP:4001 -u SYSDBA -p SYSDBA`

(4).默认账号密码：

账号：SYSDBA    密码：SYSDBA

(5).可视化

在`gdmbase/bin`目录下，执行`./console-server.sh`

启动成功后，在浏览器输入https://ip:8088

账号：SYSDBA    密码：SYSDBA

(6).手册地址：http://doc.gdmbase.com/ 

### 三、Python连接gdmbase

使用Python连接`gdmbase`，需要使用`pip`与`neo4j`的包，也需要修改`gdmbase/conf`目录下的`cypher-server.toml`文件，具体操作如下：

(1).修改`cypher-server.toml`配置文件

![](https://raw.githubusercontent.com/ranxi2001/blog-imgs/main/img/20230912200024.png)

![](https://raw.githubusercontent.com/ranxi2001/blog-imgs/main/img/20230912200043.png)

修改完成后在`bin`目录下，重启`cypher-server`

(2).引入`pip`及`neo4j`包

![](https://raw.githubusercontent.com/ranxi2001/blog-imgs/main/img/20230912200158.png)