FROM python:3.9-alpine3.13
LABEL maintainer="Ibory"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    # .tmp-buil-deps로 묶어서 설치한 패키지들(build-base postgresql-dev musl-dev)
    # 이 친구들은 psycops2를 설치하기 위해서만 필요한 패키지들이라 psycops2를 설치하고
    # 다시 삭제하는 것이 docker 이미지에 과부화를 막아준다.
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    #bash if문 []안에서 공백 주의해서 사용하자 무조건 공백!
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    # change owner의 명령어 root user-> django-user로
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol
ENV PATH="/py/bin:$PATH"

USER django-user
