FROM python:3.11-bookworm

RUN  pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["python"]
