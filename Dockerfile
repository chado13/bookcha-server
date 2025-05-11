FROM --platform=linux/amd64 python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5.28 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN apt-get update && apt-get install --no-install-recommends -y build-essential git
WORKDIR /app
COPY ./uv.lock ./pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable --no-dev 

FROM --platform=linux/amd64 python:3.12-slim
WORKDIR /app
ENV PYTHONHASHSEED=random 
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:/app
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
RUN cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && echo "Asia/Seoul" > /etc/timezone
COPY . .
EXPOSE 3000

RUN chmod +x scripts/*.sh
CMD ["bash", "scripts/start.sh"]