FROM python:3.8

MAINTAINER Logmind Software <software@logmind.com>

RUN mkdir /src

ENV PYTHONPATH $PYTHONPATH:/src

RUN pip install --upgrade pip

ADD url_shortener /src/url_shortener
ADD requirements /src/url_shortener/requirements

WORKDIR /src/url_shortener

RUN pip install --upgrade pip && pip install -r requirements/prod.txt && rm -rf requirements

EXPOSE 8000

CMD sh -c 'uvicorn \
            url_shortener.asgi:application \
            --workers 16 \
            --root-path url_shortener.asgi'