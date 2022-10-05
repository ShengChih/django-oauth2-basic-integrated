FROM python:latest
ENV TZ=Asia/Taipei
ARG GOOGLE_CLIENT_ID=
ARG GOOGLE_SECRET_KEY=
ARG FACEBOOK_CLIENT_ID=
ARG FACEBOOK_SECRET_KEY=
ARG ROOT_PASS=123456
ARG USER_PASS=123456
RUN apt-get update -qq && apt-get install -y sudo && \
    useradd -ms /bin/bash ec2-user && \
    sudo usermod -aG sudo,root ec2-user && \
    echo "root:$ROOT_PASS" | chpasswd && \
    mkdir -p /home/ec2-user/django_oauth2_backend/ && chown ec2-user: /home/ec2-user/django_oauth2_backend/ && \
    echo "ec2-user:$USER_PASS" | chpasswd
USER ec2-user
ENV PATH=/usr/local/bin:/usr/bin:/user/local/sbin:/home/ec2-user/.local/bin:$PATH \
    GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID \
    GOOGLE_SECRET_KEY=$GOOGLE_SECRET_KEY \
    FACEBOOK_CLIENT_ID=$FACEBOOK_CLIENT_ID \
    FACEBOOK_SECRET_KEY=$FACEBOOK_SECRET_KEY
WORKDIR /home/ec2-user/django_oauth2_backend/
COPY poetry.lock .
COPY poetry.toml .
COPY pyproject.toml .
RUN echo "$ROOT_PASS" | sudo -S /usr/local/bin/python -m pip install --upgrade pip && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    echo "$ROOT_PASS" | su -c 'poetry install'
CMD ["sleep", "infinity"]
# 不建立 virtualenv
# CMD ["poetry", "run", "uwsgi", "--ini", "uwsgi.ini"]
# 若建立 virtualenv
# CMD . .venv/bin/activate && exec python src/manage.py