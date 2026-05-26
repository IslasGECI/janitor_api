FROM rocker/tidyverse

RUN apt update && apt full-upgrade --yes && apt install --yes  \
    python3-pip \
    python3-venv
# Crear entorno virtual
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --upgrade pip
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /workdir
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    flake8 \
    mutmut \
    mypy \
    pylint \
    pytest \
    pytest-cov

RUN R -e "pak::pkg_install('readMS=IslasGECI/read_mapsource@latest')"
