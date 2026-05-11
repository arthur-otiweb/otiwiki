#!/bin/bash
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3-pip python3-venv nginx redis-server postgresql supervisor

# Clonar repo
git clone https://github.com/arthur-otiweb/otiwiki /var/www/otiwiki
cd /var/www/otiwiki

# Configurar ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar Nginx
sudo tee /etc/nginx/sites-available/otiwiki << EOF
server {
    listen 80;
    server_name 204.157.109.19;
    
    location /static/ {
        alias /var/www/otiwiki/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/otiwiki/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/otiwiki /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Configurar Daphne com Supervisor
sudo tee /etc/supervisor/conf.d/otiwiki.conf << EOF
[program:otiwiki]
command=/var/www/otiwiki/venv/bin/daphne -b 127.0.0.1 -p 8000 wiki.asgi:application
directory=/var/www/otiwiki
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/otiwiki.err.log
stdout_logfile=/var/log/otiwiki.out.log
EOF

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start otiwiki

echo "✅ Deploy concluído! Acesse http://wiki.oesteti.com.br"