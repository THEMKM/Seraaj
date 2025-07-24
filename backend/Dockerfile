FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python - <<'EOF'
from sentence_transformers import SentenceTransformer
SentenceTransformer("all-mpnet-base-v2")
EOF
COPY . /code
ENV APP_ENV=prod
CMD ["python", "-m", "app.main"]
