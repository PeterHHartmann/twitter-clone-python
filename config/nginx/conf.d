upstream twitter {
    server twitter-clone-app-1:3000;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://twitter
    }
}