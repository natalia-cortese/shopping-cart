# CodeSandbox supports debian and ubuntu based images
FROM debian:bullseye
WORKDIR /app
COPY /requirements.txt .
RUN pip install -r /requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
