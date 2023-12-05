FROM python:latest
WORKDIR /app
EXPOSE 8000

RUN apt-get update && \
    apt-get install -y ffmpeg

COPY /Video/SP3 ./Video/SP3
COPY /FFMPEG_Converter_Python ./FFMPEG_Converter_Python
WORKDIR /app/Video/SP3

CMD python3 main.py