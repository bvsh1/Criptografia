FROM ubuntu:20.10

# Solución para repositorios EOL
RUN sed -i -re 's/([a-z]{2}\.)?archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list

# Para evitar prompts interactivos de tzdata durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y openssh-client tcpdump iproute2

CMD ["tail", "-f", "/dev/null"]