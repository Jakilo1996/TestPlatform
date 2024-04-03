# 创建依赖文件夹

cd /opt
mkdir python3.7
mkdir -r "log/log"fen
cd log
touch nginx_error.log nginx_proxy_access.log uwsgi.log
# 编译 python3.7 版本
cd /opt/TestPlatform/depends
tar -xfz Python-3.7.8-ubuntu2004.tgz -C /opt/python3.7
cd /opt/python3.7
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
sudo apt install build-essential
sudo apt update
sudo apt install openssl1.0
ln-s /usr/local/openssl/bin/openssl /usr/bin/openssl
./configure --enable-optimizations --prefix=/usr/local/opt/python-3.7 --with-openssl=/usr/local/bin/openssl
make
sudo make altinstall
# 下载 uwsgi
sudo apt install uwsgi
sudo apt install uwsgi-plugin-python3
# 下载 nginx
sudo apt install nginx
sudo systemctl status nginx
curl 127.0.0.1:80
# todo 修改配置文件 export 默认文件
sudo systemctl restart nginx

# TODO 下载安装 mysql，创建依赖用户，创建依赖表，为用户授权

# 下载 python 依赖包
source ./pip_install.sh
# TODO 修改其中一个依赖包的文件内容

# 验证 flask 本地文件启动
cd /opt/
# 配置 uwsgi 启动，并验证
nohup uwsgi --ini /opt/TestPlatform/uwsgi_config.ini > /opt/log/uwsgi.log 2>&1 &
curl 127.0.0.1:8000
# 配置 nginx 启动，并验证访问
sudo nginx -t
sudo systemctl reload nginx