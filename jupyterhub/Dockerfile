FROM jupyterhub/jupyterhub:2.3.0

# COPY jupyterhub_config.py .

RUN /usr/bin/python3 -m pip install --upgrade pip

RUN pip3 install \
    jsonschema \
    requests \
    ruamel.yaml \
    jupyterhub-idle-culler \
    jupyterhub-nativeauthenticator \
    jhub_cas_authenticator \
    oauthenticator \
    dockerspawner

# Create oauthenticator directory and put necessary files in it
RUN mkdir /srv/oauthenticator
RUN mkdir /srv/jupyterhub/shared
WORKDIR /srv/oauthenticator
ENV OAUTHENTICATOR_DIR /srv/oauthenticator
ADD jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
ADD addusers.sh /srv/oauthenticator/addusers.sh
ADD userlist /srv/oauthenticator/userlist
ADD ssl /srv/oauthenticator/ssl
RUN chmod 700 /srv/oauthenticator
RUN ["sh", "/srv/oauthenticator/addusers.sh"]

CMD ["jupyterhub", "--f=/srv/jupyterhub/jupyterhub_config.py"]