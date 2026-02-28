FROM python:3.12

# Dockar can output print(), django logs, errors without delay 
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl gnupg

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy requirements and install Python deps early
COPY ./requirements.txt .
RUN uv pip install pip --upgrade --system
RUN uv pip install -r requirements.txt --system

# Copy the rest of the app early
COPY . .

# Make a file executable
WORKDIR /app
RUN chmod +x entrypoint.sh

# port
EXPOSE 8000

CMD ["sh", "entrypoint.sh"]