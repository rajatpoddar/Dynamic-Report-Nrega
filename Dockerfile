FROM python:3.10-slim

WORKDIR /app

# Removed software-properties-common as it's not needed and causing the build to fail
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3737

HEALTHCHECK CMD curl --fail http://localhost:3737/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=3737", "--server.address=0.0.0.0"]