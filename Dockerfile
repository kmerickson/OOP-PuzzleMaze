FROM python:3.10

RUN apt update \
  && apt install -y \
  g++ gcc make sqlite3 time curl git nano dos2unix \
  net-tools iputils-ping iproute2 sudo gdb less \
  # dependencies for pygame:
  python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev \
  libsdl1.2-dev libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev \
  libjpeg-dev libfreetype6-dev \
  && apt clean


# Install Java and Graphviz for plantuml
RUN apt install default-jre graphviz -y

ARG USER=user
ARG UID=1000
ARG GID=1000

# Set environment variables
ENV USER                ${USER}
ENV HOME                /home/${USER}

# Create user and setup permissions on /etc/sudoers
RUN useradd -m -s /bin/bash -N -u $UID $USER && \
  echo "${USER} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers && \
  chmod 0440 /etc/sudoers && \
  chmod g+w /etc/passwd 

WORKDIR ${HOME}

RUN pip install --upgrade pip
RUN pip install pygame

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install zsh - use "Bira" theme with some customization. 
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
  -t bira \
  -p git \
  -p ssh-agent \
  -p https://github.com/zsh-users/zsh-autosuggestions \
  -p https://github.com/zsh-users/zsh-completions

USER user

CMD zsh
