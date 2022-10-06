# Integrate Django and SocialProvider OAuth2 feature

# Build Django Backend Image
```

docker build -t django_oauth2_backend:latest \
    --build-arg GOOGLE_CLIENT_ID={google_client_id} \
    --build-arg GOOGLE_SECRET_KEY={google_secret_key} \
    --build-arg FACEBOOK_CLIENT_ID={facebook_client_id} \
    --build-arg FACEBOOK_SECRET_KEY={facebook_secret_key} \
    --build-arg ROOT_PASS={root_pass} \
    --build-arg USER_PASS={user_pass} \
    --build-arg DJANGO_SECRET_KEY={django_secret_key} .

docker-compose build \
    --build-arg GOOGLE_CLIENT_ID={google_client_id} \
    --build-arg GOOGLE_SECRET_KEY={google_secret_key} \
    --build-arg FACEBOOK_CLIENT_ID={facebook_client_id} \
    --build-arg FACEBOOK_SECRET_KEY={facebook_secret_key} \
    --build-arg ROOT_PASS={root_pass} \
    --build-arg USER_PASS={user_pass} \
    --build-arg DJANGO_SECRET_KEY={django_secret_key} .
```


# Certbot & Let's Encrypt nginx

## create https ssl
```
docker-compose run --rm  \
    certbot certonly --webroot --webroot-path /var/www/certbot/ \
    --dry-run -d {your.domain.name} -d {www.your.domain.name} -v

or 

docker-compose run --rm  \
    certbot certonly --manual -m {your_email} -d {your.domain.name} -d {www.your.domain.name}

chmod 777 -R ./certbot/conf/archive
```

## Renew 
```
docker-compose run --rm certbot renew
```

## Revoke
```
docker-compose run certbot revoke --cert-path /etc/letsencrypt/archive/{your.domain.name}/cert1.pem \
    --key-path /etc/letsencrypt/archive/{your.domain.name}/privkey1.pem --reason keycompromise
```
