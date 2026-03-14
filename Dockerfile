FROM python:3.9-slim

# Set the working directory inside the server
WORKDIR /app

# Copy the requirements file and install the tools
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code (main.py)
COPY . .

# Tell the server to start the engine on port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
