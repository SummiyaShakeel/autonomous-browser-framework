# Step 1: Utilize stable official Python image as base
FROM python:3.11-slim

# Step 2: Establish isolated workspace inside container
WORKDIR /app

# Step 3: Install system-level browser requirements and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Copy dependency configuration and install packages[cite: 1]
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Install Playwright and its native browser binaries[cite: 1]
RUN playwright install chromium
RUN playwright install-deps chromium

# Step 6: Copy remaining project files to the app directory[cite: 1]
COPY . .

# Step 7: Set production runtime execution entrypoint[cite: 1]
CMD ["python", "main.py"]