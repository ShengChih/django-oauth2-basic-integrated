FROM python:latest
ENV TZ=Asia/Taipei
RUN apt-get update -qq && \
    apt-get install -y sudo
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
#    apt-get update -qq && \
#    apt-get install -y locales \
#        build-essential \
#        curl \
#        git \
#        sudo \
#        vim \
#        net-tools \
#        ncdu \
#        procps \
#        htop \
#        tmux
RUN useradd -ms /bin/bash ec2-user && \
    sudo usermod -aG sudo,root ec2-user && \
    echo "root:`tr -dc A-Za-z0-9 </dev/urandom | head -c 13`" > /home/ec2-user/root_passwd && \
    cat /home/ec2-user/root_passwd | chpasswd && \
    mkdir -p /home/ec2-user/django_oauth2_backend/ && chown ec2-user: /home/ec2-user/django_oauth2_backend/ && \
    echo "ec2-user:`tr -dc A-Za-z0-9 </dev/urandom | head -c 13`" > /home/ec2-user/ec2-user_passwd && \
    echo "ec2-user  ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers
USER ec2-user
ENV PATH=/usr/local/bin:/usr/bin:/user/local/sbin:/home/ec2-user/.local/bin::/home/ec2-user/.poetry/bin:$PATH
RUN sudo /usr/local/bin/python -m pip install --upgrade pip && \
    curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /home/ec2-user/django_oauth2_backend/
CMD ["sleep", "infinity"]