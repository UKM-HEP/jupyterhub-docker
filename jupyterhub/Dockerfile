FROM jupyterhub/jupyterhub:2.3.0

COPY jupyterhub_config.py .

RUN /usr/bin/python3 -m pip install --upgrade pip

RUN pip3 install \
    jupyterhub-idle-culler \
    jupyterhub-nativeauthenticator \
    jhub_cas_authenticator \
    dockerspawner

CMD ["jupyterhub", "--f=/srv/jupyterhub/jupyterhub_config.py"]