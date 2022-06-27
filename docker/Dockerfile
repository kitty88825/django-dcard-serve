FROM python:3.8
WORKDIR /code

# Setup env
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y libpq-dev

# Install pipenv and compilation dependencies
RUN pip install --upgrade --no-cache-dir pip pipenv

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system
