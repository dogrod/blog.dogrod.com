# https://docs.docker.com/compose/django/#define-the-project-components
FROM python:3

ENV PYTHONUNBUFFERED 1

# Bundle APP files
RUN mkdir -p /home/service
WORKDIR /home/service
# COPY . /home/service
ADD requirements.txt /home/service/

# Install app dependencies
RUN pip install -r requirements.txt

ADD . /home/service/

RUN ls -al -R

# EXPOSE 8000
# CMD ["uwsgi", "--ini", "uwsgi.ini"]