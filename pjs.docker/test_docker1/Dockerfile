# Build with: docker build -t pjs ./pjs.docker
# Run with:   docker run -v $(pwd):/wd pjs phantomjs_script.js

FROM ubuntu

COPY service_start.sh /root
RUN chmod 755 /root/service_start.sh

ENTRYPOINT /root/service_start.sh
WORKDIR /root


#VOLUME /wd
#WORKDIR /wd

#ENTRYPOINT /wd/service_start.sh

