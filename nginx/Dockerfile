FROM nginx:1.23.3 

# RUN rm /etc/nginx/conf.d/default.conf

# COPY fullchain.pem /etc/nginx/fullchain.pem
# COPY privkey.pem /etc/nginx/privkey.pem

# COPY nginx.conf /etc/nginx/conf.d

COPY assetlinks.json /usr/share/nginx/html/.well-known/assetlinks.json
