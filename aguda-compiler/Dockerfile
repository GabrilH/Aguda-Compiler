FROM python:3.13-alpine

# Install LLVM and other dependencies
RUN apk update && apk add --no-cache llvm15 llvm15-dev clang15 build-base && \
    ln -s /usr/bin/llvm-config-15 /usr/bin/llvm-config

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY src /app/src
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Set the default command to run main.py
ENTRYPOINT ["python", "main.py"]