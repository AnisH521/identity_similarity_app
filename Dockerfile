# An official Python runtime as a parent image
# Using slim reduces image size
FROM python:3.10-slim

# working directory in the container
WORKDIR /app

# System dependencies required by dlib and face_recognition
# - build-essential: Provides C/C++ compilers (like gcc)
# - cmake: Required by dlib for building
# - libsm6, libxext6, libxrender-dev: Often needed for libraries processing images (dependencies for OpenCV, which dlib sometimes uses parts of indirectly or shares dependencies with)
# - cleanup: Remove apt lists to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Python dependencies from requirements.txt
# --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]