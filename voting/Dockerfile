FROM python:3
RUN mkdir -p /opt/src/voting
WORKDIR /opt/src/voting

COPY . .
ENV TZ="Europe/Belgrade"
RUN echo "Europe/Belgrade" > /etc/timezone

RUN pip install -r ./requirements.txt

EXPOSE 7000
ENTRYPOINT ["python", "application.py"]
