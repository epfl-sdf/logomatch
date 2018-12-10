# Build with: docker build -t pjs ./pjs.docker
# Run with:   docker run -v $(pwd):/wd pjs phantomjs_script.js

FROM wernight/phantomjs
VOLUME /wd
WORKDIR /wd

ENTRYPOINT ["/usr/local/bin/phantomjs"]
