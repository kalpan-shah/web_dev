# Minimal Linux distribution
FROM debian:bookworm-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up environment variables so uv installs Python automatically
ENV UV_PYTHON_PREFERENCE=only-managed \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the dependencies file to the working directory
COPY uv.lock pyproject.toml ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy the content of the local src directory to the working directory
COPY ./app ./app

EXPOSE 8000

CMD ["uv", "run", "uvicorn","app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# build command: docker build -t todo-app:git-sha .