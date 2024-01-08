FROM ghcr.io/arosbio/cpsign-cp-reg-server:2.0.0-rc6

LABEL org.opencontainers.image.source=https://github.com/pharmbio/cplogd-v2.0
LABEL org.opencontainers.image.description="CPSign model for predicting cpLogD - version 2"
LABEL org.opencontainers.image.url=https://github.com/pharmbio/cplogd-v2.0
LABEL org.opencontainers.image.version=v2
LABEL org.opencontainers.image.authors="Staffan Arvidsson McShane"
LABEL org.opencontainers.image.title="cpLogD prediction service version 2"


COPY trained-model.jar /var/lib/jetty/model.jar