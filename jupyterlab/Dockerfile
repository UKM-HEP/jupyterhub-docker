# This will install:
# - CentOS 7
# - Jupyter 

# To see the version numbers (which change as the EPEL and PyPI repositories evolve)
# start the Terminal from the Jupyter notebook and type (e.g.):

# rpm -q root
# pip3 show jupyter

# Using ROOT docker stack configuration for the development
# https://github.com/wgseligman/docker-jupyter-pyroot/blob/master/Dockerfile
# https://root.cern/install/dependencies/

ARG BASE_CONTAINER=siewyanhoh/jupyroot:latest
FROM $BASE_CONTAINER

LABEL maintainer="Siewyan Hoh <shoh@ukm.edu.my>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

RUN yum -y update
RUN yum -y install epel-release

# Install packages needed for ROOT
RUN yum -y install python3 python3-pip root which python3-root python3-devel
RUN yum -y install root-tmva root-tmva-python root-minuit2 python3-jupyroot

# curl will be needed when we install python packages below.
RUN yum -y install curl libcurl libcurl-devel 

# Additional packages for some C++ work:
RUN yum -y install make boost-devel gsl-devel binutils-devel 


# The "native" version of cmake in CentOS 7 is old and doesn't have
# the necessary features to compile some of the python packages below.
# Set up cmake3 as default version of cmake.
RUN yum -y install cmake3 
RUN ln -sf /usr/bin/cmake3 /usr/bin/cmake

# Other Linux packages required for python package compilation.
RUN yum -y install python36-pillow-devel

# Install packages from PyPI. These are the ones needed for almost any
RUN /usr/bin/python3 -m pip install --upgrade pip

RUN pip3 install --upgrade wheel
RUN pip3 install --upgrade numpy scipy matplotlib 

RUN touch /home/${NB_USER}/.cache/pip
RUN fix-permissions /home/${NB_USER}/.cache/pip

# These additional packages are handy, but not critical.
RUN pip3 install --upgrade iminuit pandas sympy terminado urllib3 pycurl
# RUN pip3 install --upgrade rootpy rootkernel root-numpy uproot
RUN pip3 install --upgrade rootkernel root-numpy uproot

# Wrap it up.
RUN yum clean all

RUN fix-permissions "/home/${NB_USER}"

USER ${NB_UID}

WORKDIR "${HOME}"