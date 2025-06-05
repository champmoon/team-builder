#!/bin/bash

rm -rf /etc/letsencrypt/live/tbuilder.pro/*

certbot certonly --standalone --email antipov8v@gmail.com -d tbuilder.pro --key-type rsa --agree-tos

rm -rf /etc/nginx/cert.pem
rm -rf /etc/nginx/key.pem

cp /etc/letsencrypt/live/tbuilder.pro/fullchain.pem /etc/nginx/fullchain.pem
cp /etc/letsencrypt/live/tbuilder.pro/privkey.pem /etc/nginx/privkey.pem
