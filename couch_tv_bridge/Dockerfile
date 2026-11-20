# couch-tv bridge as a Home Assistant add-on. Built on the Home Assistant machine itself.
FROM node:22-bookworm-slim
ARG COUCH_TV_VERSION=v0.13.8
RUN apt-get update \
 && apt-get install -y --no-install-recommends git python3 python3-venv ca-certificates \
 && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch "${COUCH_TV_VERSION}" https://github.com/Seagey/couch-tv.git /app
RUN python3 -m venv /venv && /venv/bin/pip install --no-cache-dir -r /app/bridge/requirements.txt
RUN cd /app/remote && npm ci --no-audit --no-fund && npm run build && rm -rf node_modules
COPY run.sh /run.sh
COPY make_config.py /make_config.py
RUN chmod 755 /run.sh
WORKDIR /app
CMD ["/run.sh"]
