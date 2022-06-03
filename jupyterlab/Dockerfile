# This will install:
# - CentOS 7
# - Jupyter 
# - ROOT

# To see the version numbers (which change as the EPEL and PyPI repositories evolve)
# start the Terminal from the Jupyter notebook and type (e.g.):

# rpm -q root
# pip3 show jupyter

# Using base docker stack configuration for the development
# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile

FROM centos:7

LABEL maintainer="Siewyan Hoh <shoh@ukm.edu.my>"

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

#WORKDIR /work

# Install packages from CentOS 7 base, EPEL, and SCL (for a later compiler version)
RUN yum -y update
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y install centos-release-scl

# The "native" gcc compiler in CentOS 7 doesn't support C++11, which is
# needed to compile at least one of the python packages below. Include the
# SCL development toolset, which includes a more advanced compiler. 
RUN yum -y install devtoolset-7-gcc*
SHELL [ "/usr/bin/scl", "enable", "devtoolset-7"]

# Install packages needed for ROOT
RUN yum -y install python3 python3-pip root which python3-root python3-devel python3-setuptools
RUN yum -y install root-tmva root-tmva-python root-minuit2 python3-jupyroot

# curl will be needed when we install python packages below.
RUN yum -y install curl libcurl libcurl-devel 

# Additional packages for some C++ work:
RUN yum -y install make boost-devel gsl-devel binutils-devel
# RUN yum -y install gcc-c++ gcc-gfortran

# The "native" version of cmake in CentOS 7 is old and doesn't have
# the necessary features to compile some of the python packages below.
# Set up cmake3 as default version of cmake.
RUN yum -y install cmake3 
RUN ln -sf /usr/bin/cmake3 /usr/bin/cmake

# Other Linux packages required for python package compilation.
RUN yum -y install python36-pillow-devel

# tini
# https://github.com/krallin/tini
RUN yum -y install tini sudo

# Wrap it up.
RUN yum clean all

# Install packages from PyPI. These are the ones needed for almost any
# Jupyter installation. 
RUN python3 -m pip install --upgrade pip
RUN pip3 install --upgrade wheel
RUN pip3 install --upgrade jupyter
RUN pip3 install --upgrade numpy scipy matplotlib 

# Install jupyterhub
RUN pip3 install jupyterhub==2.3.0

# These additional packages are handy, but not critical. 
RUN pip3 install --upgrade jupyterlab
# RUN pip3 install --upgrade iminuit pandas sympy terminado urllib3 pycurl tables
RUN pip3 install --upgrade iminuit pandas sympy terminado urllib3 pycurl
RUN pip3 install --upgrade rootpy rootkernel root-numpy uproot


########################################################################################

# COnfigure environment
ENV SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

ENV HOME="/home/${NB_USER}"

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Copy a script that we will use to correct permissions after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Enable prompt color in the skeleton .bashrc before creating the default NB_USER
# hadolint ignore=SC2016
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc

# Create NB_USER with name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd -l -m -s /bin/bash -N -u "${NB_UID}" "${NB_USER}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "${HOME}"

USER ${NB_UID}

# Setup work directory for backward-compatibility
RUN mkdir "/home/${NB_USER}/work" && \
    fix-permissions "${HOME}"

WORKDIR /tmp

RUN jupyter notebook --generate-config && \
    jupyter lab clean && \
    fix-permissions "${HOME}"

EXPOSE 8888

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

# Copy local files as late as possible to avoid cache busting
COPY start.sh start-notebook.sh start-singleuser.sh /usr/local/bin/
# Currently need to have both jupyter_notebook_config and jupyter_server_config to support classic and lab
COPY jupyter_server_config.py /etc/jupyter/

# Fix permissions on /etc/jupyter as root
USER root

# Legacy for Jupyter Notebook Server, see: [#1205](https://github.com/jupyter/docker-stacks/issues/1205)
RUN sed -re "s/c.ServerApp/c.NotebookApp/g" \
     /etc/jupyter/jupyter_server_config.py > /etc/jupyter/jupyter_notebook_config.py && \
     fix-permissions /etc/jupyter/ && \
     fix-permissions /usr/local/bin/

# HEALTHCHECK documentation: https://docs.docker.com/engine/reference/builder/#healthcheck
# This healtcheck works well for `lab`, `notebook`, `nbclassic`, `server` and `retro` jupyter commands
# https://github.com/jupyter/docker-stacks/issues/915#issuecomment-1068528799
HEALTHCHECK  --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -O- --no-verbose --tries=1 --no-check-certificate \
    http${GEN_CERT:+s}://localhost:8888${JUPYTERHUB_SERVICE_PREFIX:-/}api || exit 1

RUN fix-permissions "/home/${NB_USER}"

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}