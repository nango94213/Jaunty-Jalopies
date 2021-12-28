FROM python:3.9-alpine3.14

# Update Python
RUN echo http://dl-cdn.alpinelinux.org/alpine/v3.14/community >> /etc/apk/repositories \
  && apk --no-cache upgrade

# Add run-time dependencies.
RUN apk --no-cache add \
    bash \
    libpq \
    git

# Add build dependencies.
RUN apk --no-cache add --virtual .build-deps \
    alpine-sdk \
    postgresql-dev \
    python3-dev

WORKDIR /app

# Update pip.
RUN pip install --upgrade pip

# Install Python requirements.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Remove build dependencies.
RUN apk del .build-deps

# Add project code last to take advantage of cache
COPY . .

EXPOSE 8001

CMD gunicorn main:app --bind 0.0.0.0:8001 --reload -t 6000