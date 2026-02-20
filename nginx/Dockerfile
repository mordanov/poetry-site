FROM nginx:alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY frontend/templates/index.html /var/www/html/index.html
COPY frontend/static /var/www/html/static
