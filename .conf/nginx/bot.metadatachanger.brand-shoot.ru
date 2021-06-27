server {
    # прослушивание порта 80 (http)
    listen 80;
    server_name bot.metadatachanger.brand-shoot.ru www.bot.metadatachanger.brand-shoot.ru;
    location / {
        # перенаправлять любые запросы на один и тот же URL-адрес, как на https
        return 301 https://$host$request_uri;
    }
}

server {
    # прослушивание порта 443 (https)
    listen 443 ssl;
    server_name bot.metadatachanger.brand-shoot.ru www.bot.metadatachanger.brand-shoot.ru;

    # расположение self-signed SSL-сертификата
    ssl_certificate /etc/letsencrypt/live/bot.metadatachanger.brand-shoot.ru/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/bot.metadatachanger.brand-shoot.ru/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    # запись доступа и журналы ошибок в /var/log
    access_log /var/log/nginx_bot.metadatachanger.brand-shoot.ru_brandshoot.access;
    error_log /var/log/nginx_bot.metadatachanger.brand-shoot.ru_brandshoot.error;

    location / {
        # переадресация запросов приложений на сервер gunicorn
        proxy_pass http://127.0.0.1:9003;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # location /static {
    #     # обрабатывать статические файлы напрямую, без пересылки в приложение
    #     alias /root/<path_to_static>/static;
    #     expires 30d;
    # }    
}