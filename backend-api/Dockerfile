FROM python:3.11

COPY ./requirements.txt /workspace/requirements.txt

RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY . /workspace

WORKDIR /workspace

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]