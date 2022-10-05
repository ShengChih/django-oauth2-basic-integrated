# Integrate Django and SocialProvider OAuth2 feature

# Build Django Backend Image
```

docker build -t django_oauth2_backend:latest \
    --build-arg GOOGLE_CLIENT_ID={google_client_id} \
    --build-arg GOOGLE_SECRET_KEY={google_secret_key} \
    --build-arg FACEBOOK_CLIENT_ID={facebook_client_id} \
    --build-arg FACEBOOK_SECRET_KEY={facebook_secret_key} \
    --build-arg ROOT_PASS={root_pass} \
    --build-arg USER_PASS={user_pass} .

docker-compose build \
    --build-arg GOOGLE_CLIENT_ID={google_client_id} \
    --build-arg GOOGLE_SECRET_KEY={google_secret_key} \
    --build-arg FACEBOOK_CLIENT_ID={facebook_client_id} \
    --build-arg FACEBOOK_SECRET_KEY={facebook_secret_key} \
    --build-arg ROOT_PASS={root_pass} \
    --build-arg USER_PASS={user_pass}
```