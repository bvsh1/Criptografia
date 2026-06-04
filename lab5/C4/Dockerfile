FROM ubuntu:22.10
RUN sed -i -re 's/([a-z]{2}\.)?archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y openssh-server openssh-client tcpdump iproute2
RUN mkdir -p /var/run/sshd
RUN useradd -m -s /bin/bash prueba && echo "prueba:prueba" | chpasswd
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
