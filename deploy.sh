set -ex
# clone 代码 或 上传 到 /var/www/forum

# 换源
ln -f -s /var/www/forum/misc/sources.list /etc/apt/sources.list
mkdir -p /root/.pip
ln -f -s /var/www/forum/misc/pip.conf /root/.pip/pip.conf

# 系统设置
apt-get update
apt-get -y install  zsh curl ufw
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 2000
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 装依赖
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update

debconf-set-selections /var/www/forum/database_secret.conf

apt-get install -y git supervisor nginx python3.6 mysql-server
python3.6 /var/www/forum/get-pip.py
pip3 install jinja2 flask gunicorn pymysql flask_sqlalchemy flask_admin gevent redis

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接，服务器服务
ln -s -f /var/www/forum/server.conf /etc/supervisor/conf.d/server.conf
# 页面 nginx
ln -s -f /var/www/forum/view.nginx /etc/nginx/sites-enabled/view

# 重置数据库
cd /var/www/forum/server
python3.6 reset.py

# 重启服务器
service supervisor restart
service nginx restart

echo 'deploy success'
echo 'ip'
hostname -I