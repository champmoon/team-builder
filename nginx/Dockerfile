FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY certf.crt /etc/nginx/certf.crt
COPY certf.key /etc/nginx/certf.key

COPY nginx.conf /etc/nginx/conf.d

COPY assetlinks.json /usr/share/nginx/html/.well-known/assetlinks.json

COPY 3rj9_bJNOEfuoqzgq4Zmudc93aqUaibMf9NJiaZttF8 /usr/share/nginx/html/.well-known/acme-challenge/3rj9_bJNOEfuoqzgq4Zmudc93aqUaibMf9NJiaZttF8
