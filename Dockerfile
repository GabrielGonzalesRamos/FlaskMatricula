FROM python:3.10.12-alpine

LABEL authors="Gabriel Gonzales <jose.gabriel.gonzales.ramos@gmail.com>"

RUN addgroup -S deploy && adduser -S deploy -G deploy

WORKDIR /home/deploy/app

COPY --chown=deploy:deploy requirements.txt .

RUN apk add --no-cache curl gpg unixodbc unixodbc-dev g++ python3-dev gcc && pip3 install --no-cache-dir -r requirements.txt && \
    curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.10.4.1-1_amd64.apk && \ 
    echo Y | apk add --allow-untrusted msodbcsql17_17.10.4.1-1_amd64.apk && \
    rm -rf msodbcsql17_17.10.4.1-1_amd64.apk

USER deploy

COPY --chown=deploy:deploy . .

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]