# CodeSandbox supports debian and ubuntu based images
FROM debian:bullseye
WORKDIR /app
COPY /project/shopping-cart/requirements.txt .
RUN pip install -r /project/shopping-cart/requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
