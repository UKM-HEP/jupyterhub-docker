# This will install:
# - ROOT 6.26/00
# https://root.cern/install/dependencies/

ARG BASE_CONTAINER=siewyanhoh/jupycentos7:v1.0
FROM $BASE_CONTAINER

LABEL maintainer="Siewyan Hoh <shoh@ukm.edu.my>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

RUN yum -y update
RUN yum -y install epel-release

# Dependencies
RUN yum -y install git gcc-c++ gcc binutils \
libX11-devel libXpm-devel libXft-devel libXext-devel openssl-devel

# Optional packages
RUN yum -y install redhat-lsb-core gcc-gfortran pcre-devel \
mesa-libGL-devel mesa-libGLU-devel glew-devel ftgl-devel mysql-devel fftw-devel \
cfitsio-devel graphviz-devel libuuid-devel \
avahi-compat-libdns_sd-devel openldap-devel libxml2-devel gsl-devel readline-devel

# curl will be needed when we install python packages below.
RUN yum -y install curl libcurl libcurl-devel 

# Additional packages for some C++ work:
RUN yum -y install boost-devel gsl-devel binutils-devel 

# The "native" version of cmake in CentOS 7 is old and doesn't have
# the necessary features to compile some of the python packages below.
# Set up cmake3 as default version of cmake.
RUN yum -y install cmake3 
RUN ln -sf /usr/bin/cmake3 /usr/bin/cmake

# Upgrade PyPi just in case we need it
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN pip3 install --upgrade wheel
RUN touch /home/${NB_USER}/.cache/pip
RUN fix-permissions /home/${NB_USER}/.cache/pip

# Install Python 3 packages
RUN arch=$(uname -m) && \
    if [ "${arch}" == "aarch64" ]; then \
        # Prevent libmamba from sporadically hanging on arm64 under QEMU
        # <https://github.com/mamba-org/mamba/issues/1611>
        export G_SLICE=always-malloc; \
    fi && \
    mamba install --quiet --yes \
    'bokeh' \
    'conda-forge::blas=*=openblas' \
    'cython' \
    'dask' \
    'dill' \
    'h5py' \
    'ipympl'\
    'ipywidgets' \
    'matplotlib-base' \
    'numba' \
    'numexpr' \
    'pandas' \
    'patsy' \
    'protobuf' \
    'pytables' \
    'seaborn' \
    'sqlalchemy' \
    'statsmodels' \
    'sympy' \
    'widgetsnbextension'\
    'iminuit'\
    'pandas'\
    'sympy'\
    'terminado'\
    'urllib3'\
    'pycurl'\
    'uproot'\
    'root' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Wrap it up.
RUN yum clean all

RUN fix-permissions "/home/${NB_USER}"

USER ${NB_UID}

WORKDIR "${HOME}"