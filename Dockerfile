# dockerize fase api
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY . .

# Install any dependencies
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app"]