FROM python:3.8.16-slim AS build_imge

RUN apt-get update && apt-get install -y build-essential && apt-get clean

COPY requirements.txt .

RUN pip install --upgrade pip==25.0.1
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.8.16-slim

ARG USERNAME=magalu

RUN useradd -m $USERNAME

RUN rm -rf /etc/localtime && ln -s /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

COPY --from=build_imge /usr/local/lib/python3.8 /usr/local/lib/python3.8
COPY --from=build_imge /usr/local/bin/uwsgi /usr/local/bin/uwsgi

WORKDIR /usr/src/app

COPY . .

RUN chown $USERNAME:$USERNAME -R /usr/src/app

USER $USERNAME

EXPOSE 5000

CMD ["uwsgi", "--ini", "uwsgi.ini"]