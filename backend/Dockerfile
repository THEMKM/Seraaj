FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code
ENV APP_ENV=prod
CMD ["python", "-m", "app.main"]
