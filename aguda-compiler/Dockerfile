FROM python:alpine

# Install LLVM and other dependencies
# RUN apk update && apk add --no-cache llvm clang

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY src /app/src
COPY main.py /app/main.py

# Install dependencies
RUN pip install ply

# Set the default command to run main.py
ENTRYPOINT ["python", "main.py"]