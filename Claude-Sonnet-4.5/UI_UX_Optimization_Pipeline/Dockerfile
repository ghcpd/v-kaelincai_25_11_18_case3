FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ ./src/
COPY tests/ ./tests/

# Create directories
RUN mkdir -p images_original images_optimized images_comparison results

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run tests by default
CMD ["python", "-m", "pytest", "tests/test_pipeline.py", "-v"]
