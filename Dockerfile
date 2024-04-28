FROM python:alpine3.18

WORKDIR /app

RUN apk add --no-cache make

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt 

#RUN pip install --no-cache-dir -r requirements.txt -i http://mirrors.cloud.tencent.com/pypi/simple --trusted-host mirrors.cloud.tencent.com

CMD [ "python", "app.py" ]
