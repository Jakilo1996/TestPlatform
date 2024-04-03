cd /opt/TestPlatform
pid=$(lsof -i :8000 | awk 'NR==2 {print $2}')
echo pid
if [-n pid]; then
  kill -9 pid
nohup uwsgi --ini /opt/TestPlatform/uwsgi_config.ini > /opt/log/uwsgi.log 2>&1 &
sudo systemctl reload nginx