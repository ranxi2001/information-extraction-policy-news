# 使用 PyTorch aarch64镜像作为基础
FROM kumatea/pytorch

# 其他 Docker 指令，例如设置工作目录、复制文件等。

# 设置工作目录
WORKDIR /app

# 将 uie 文件夹的内容复制到容器的 /app 目录中
COPY ./uie /app

# 安装项目所需的依赖
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 设置 Flask 环境变量
ENV FLASK_APP=/app/uie_pytorch/uie-backend-api4.py
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露端口 888
EXPOSE 888

# 运行 Flask 应用
CMD ["python", "/app/uie_pytorch/uie-backend-api4.py"]

