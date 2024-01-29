FROM ghcr.io/arosbio/cpsign-cp-reg-server:latest-full

LABEL org.opencontainers.image.source=https://github.com/pharmbio/cplogd-v2.0
LABEL org.opencontainers.image.description="CPSign model for predicting cpLogD - version 2"
LABEL org.opencontainers.image.url=https://github.com/pharmbio/cplogd-v2.0
LABEL org.opencontainers.image.version=v2
LABEL org.opencontainers.image.authors="Staffan Arvidsson McShane"
LABEL org.opencontainers.image.title="cpLogD prediction service version 2"

# Copy the model itself to the image
COPY trained-model.jar /var/lib/jetty/model.jar

# Change to root user to create a new user and change directory ownership
USER root

ENV USER=jetty2
ENV HOME=/home/$USER

# Create the user 1000
RUN useradd -m -u 1000 $USER

# Set working directory (this is where the code should go)
WORKDIR $HOME/app
# Copy the required startup script 
COPY start-script.sh $HOME/app/start-script.sh
# Make startup script runnable and change user
RUN chmod +x start-script.sh \
    && chown -R $USER:$USER $HOME \
    && chown -R $USER:$USER /var/lib/jetty/ \
    && chown -R $USER:$USER /usr/local/jetty \
    && rm -rf /var/lib/apt/lists/*

# Set the required user
USER $USER

ENTRYPOINT ["./start-script.sh"]