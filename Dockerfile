FROM python:3

WORKDIR /usr/src/app

ENV DISPLAY :0

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "parejas.py" ]