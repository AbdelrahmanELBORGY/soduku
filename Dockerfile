# 1. Use a lightweight Python base image
FROM python:3.9-slim

# 2. Set the directory inside the container
WORKDIR /app

# 3. Copy only the requirements first (this makes building faster)
COPY requirements.txt .

# 4. Install your Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your actual code (main.py, solver.py, etc.) into the container
COPY . .

# 6. Start the FastAPI server on port 7860 (Hugging Face default)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]