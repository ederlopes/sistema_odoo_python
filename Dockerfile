FROM debian:stretch
LABEL maintainer="ABGF"
ENV LANG C.UTF-8

RUN echo $LANG UTF-8 > /etc/locale.gen && \
    apt-get update && \
    apt-get -y install locales python3 \
    python3-dev python3-pip mercurial \
    python3-psycopg2 libpq-dev git \
    build-essential autoconf libtool \
    pkg-config python3-opengl \
    python-pyrex python-pyside.qtopengl \
    qt4-dev-tools qt4-designer libqtgui4 \
    libqtcore4 libqt4-xml libqt4-test \
    libqt4-script libqt4-network libqt4-dbus \
    python-qt4 python-qt4-gl libgle3 firefox-esr \
    libssl-dev libsasl2-dev libldap2-dev vim && apt-get clean && \
    update-locale --reset LANG=$LANG

# deps, lessc, less-plugin-clean-css, wkhtmltopdf
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            ca-certificates \
            curl \
            dirmngr \
            fonts-noto-cjk \
            gnupg \
            libssl1.0-dev \
            node-less \
            python3-pip \
            python3-pyldap \
            python3-qrcode \
            python3-renderpm \
            python3-setuptools \
            python3-vobject \
            python3-watchdog \
            xz-utils \
            xvfb \
            virtualenv \
            python3-venv \
        && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb \
        && echo '7e35a63f9db14f93ec7feeb0fce76b30c08f2057 wkhtmltox.deb' | sha1sum -c - \
        && dpkg --force-depends -i wkhtmltox.deb\
        && apt-get -y install -f --no-install-recommends \
        && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# postgresql-client
RUN set -x; \
        echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' > etc/apt/sources.list.d/pgdg.list \
        && export GNUPGHOME="$(mktemp -d)" \
        && repokey='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8' \
        && gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" \
        && gpg --armor --export "${repokey}" | apt-key add - \
        && gpgconf --kill all \
        && rm -rf "$GNUPGHOME" \
        && apt-get update  \
        && apt-get install -y postgresql-client \
        && rm -rf /var/lib/apt/lists/*

# rtlcss
RUN set -x;\
    echo "deb http://deb.nodesource.com/node_8.x stretch main" > /etc/apt/sources.list.d/nodesource.list \
    && export GNUPGHOME="$(mktemp -d)" \
    && repokey='9FD3B784BC1C6FC31A8A0A1C1655A0AB68576280' \
    && gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" \
    && gpg --armor --export "${repokey}" | apt-key add - \
    && gpgconf --kill all \
    && rm -rf "$GNUPGHOME" \
    && apt-get update \
    && apt-get install -y nodejs \
    && npm install -g rtlcss \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /odoo

COPY buildout-docker.cfg /odoo/buildout.cfg
COPY default.cfg /odoo
COPY entrypoint.sh /odoo/entrypoint.sh
COPY dropdb.sh /odoo/dropdb.sh
COPY geckodriver /usr/local/bin/geckodriver

RUN python3 -m venv . && chmod +x /odoo/entrypoint.sh && /odoo/entrypoint.sh && /odoo/bin/pip3 install -U zc.buildout && /odoo/bin/buildout -N

EXPOSE 8069
COPY teste /odoo/teste
RUN bin/pip3 install psycopg2 pyvirtualdisplay selenium
CMD ["bin/python_odoo", "teste/test_docker_sce.py"]
#CMD ["/bin/bash"]
