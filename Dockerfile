FROM python:3.11-bookworm

RUN python --version
RUN pip --version
COPY requirements.txt .
RUN ls
RUN pip install -r requirements.txt

CMD ["python"]