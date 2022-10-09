FROM python:3.10

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY . .

ENTRYPOINT ["sh", 'entrypoint.sh']