FROM joyzoursky/python-chromedriver:3.9-alpine-selenium

WORKDIR /app
COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY src/ /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
