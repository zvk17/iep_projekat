FROM python:3
RUN mkdir -p /opt/src/daemon
WORKDIR /opt/src/daemon

COPY . .
ENV TZ="Europe/Belgrade"
RUN echo "Europe/Belgrade" > /etc/timezone

RUN pip install -r ./requirements.txt

#EXPOSE 7000
ENTRYPOINT ["python", "application.py"]
