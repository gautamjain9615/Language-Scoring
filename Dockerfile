FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libsndfile1-dev \
    default-jdk

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN mkdir /src
WORKDIR /src
ADD requirements.txt /src/
RUN pip install -r requirements.txt
ADD . /src/

EXPOSE 80

CMD ["python3","./manage.py", "runserver", "0.0.0.0:80"]