FROM ubuntu:16.10

# Solución para repositorios EOL (End of Life)
RUN sed -i -re 's/([a-z]{2}\.)?archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list

# Instalación de cliente SSH y herramientas de red
RUN apt-get update && apt-get install -y openssh-client tcpdump iproute2

# Mantener el contenedor vivo
CMD ["tail", "-f", "/dev/null"]