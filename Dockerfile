FROM node:slim

# Set environment variables for reveal.js GitHub repo
ENV REPO=https://github.com/hakimel/reveal.js.git

# npm loglevel in base image is verbose, adjust to warnings only
ENV NPM_CONFIG_LOGLEVEL warn

RUN set -ex \
    \
    && apt-get update \
    \
# Install necessary utilities
    && apt-get install -y --no-install-recommends git bzip2 \
    \
# Fetch reveal.js
    && git clone https://github.com/hakimel/reveal.js.git \
    \
# Install dependencies
    && mkdir -p /reveal.js/node_modules \
    && npm install -g grunt-cli \
    && npm install --prefix /reveal.js \
    \
# Clean up
    && npm cache verify \
    && rm -rf /tmp/npm* /tmp/phantomjs \
    && apt-get purge -y git bzip2 \
    && rm -rf /var/lib/apt/lists/* \
    && chown -R node:node /reveal.js

RUN sed -i /reveal.js/Gruntfile.js -e "s/open: true/ open: false/"

WORKDIR /reveal.js

USER node

EXPOSE 8000

CMD [ "grunt", "serve" ]