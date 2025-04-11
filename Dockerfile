# Use a base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /workspace

# Copy the application files
COPY . /workspace

# Install dependencies
RUN pip install -r requirements.txt

# Set the default command
CMD ["pytest", "tests", "-v"]