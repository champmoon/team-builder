FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY chain.pem /etc/nginx/chain.pem
COPY fullchain.pem /etc/nginx/fullchain.pem
COPY privkey.pem /etc/nginx/privkey.pem

COPY nginx.conf /etc/nginx/conf.d

COPY assetlinks.json /usr/share/nginx/html/.well-known/assetlinks.json
