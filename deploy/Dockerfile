FROM python:3.12

ENV WEB_CONCURRENCY=4

ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt install -y libpq-dev

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/

ENV PATH="/app/bin/.venv/bin:$PATH"

ENV PYTHONPATH=/app

COPY ./src/python/joborm/*.py /app

# Not yet
#ENV UV_COMPILE_BYTECODE=1
#ENV UV_LINK_MODE=copy
#RUN --mount=type=cache,target=/root/.cache/uv \
#    --mount=type=bind,source=uv.lock,target=uv.lock \
#    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#    uv sync --frozen --no-install-project
#COPY ./src/python/joborm/pyproject.toml ./src/python/joborm/uv.lock ./src/python/joborm/alembic.ini /bin/app
#RUN --mount=type=cache,target=/root/.cache/uv \
#    uv sync

#RUN /bin/uv sync --frozen --no-install-project

COPY ./src/python/joborm/requirements.txt /app

RUN cd /app && \
    uv venv && \
    uv pip install --system -r /app/requirements.txt

USER 1001

CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
