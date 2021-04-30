FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

ENV USER=nginxuser
ENV HOME=/app

RUN adduser -D $USER

RUN chown -R $USER:$USER /var/cache/nginx && \
    chown -R $USER:$USER /var/log/nginx && \
    chown -R $USER:$USER /etc/nginx/conf.d && \
    chmod -R 766 /var/log/nginx/

RUN touch /var/run/nginx.pid && \
    chown -R $USER:$USER /var/run/nginx.pid && \
    chown -R $USER:$USER /var/cache/nginx

USER $USER

WORKDIR $HOME