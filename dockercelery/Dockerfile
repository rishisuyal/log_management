FROM python:3.10-alpine

COPY ./app /usr/app/

WORKDIR /usr/app

RUN python3.10 -m pip install pip --upgrade

RUN pip install virtualenv

RUN python3.10 -m venv env

RUN . env/bin/activate
#COPY requirement.txt /usr/app/
RUN  pip install -r requirement.txt

EXPOSE 7474

CMD ["celery","-A","celery_app","worker","--loglevel=info"]
