FROM python:alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY src /app/src
COPY test /app/test
COPY main.py /app/main.py
COPY run_main.sh /app/run_main.sh

# Install dependencies
RUN pip install ply

# Make the run script executable
RUN chmod +x run_main.sh

# Set the default command to the custom script
ENTRYPOINT ["./run_main.sh"]