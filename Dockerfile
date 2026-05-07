FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY scripts ./scripts
COPY configs ./configs
COPY examples ./examples
COPY docs ./docs
COPY templates ./templates
COPY executor.sh repo-metadata.json ./
RUN pip install --no-cache-dir -e '.[dev]'
CMD ["./executor.sh", "verify"]
