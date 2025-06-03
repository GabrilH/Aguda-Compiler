FROM python:3.10-slim

# Install LLVM
RUN apt-get update && \
    apt-get install -y llvm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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