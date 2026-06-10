FROM python:3.11-slim

# Install system dependencies and curl
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unzip \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome stable (Selenium Manager will automatically manage the matching ChromeDriver)
RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependencies first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port 8080 for Google OAuth authentication callback
EXPOSE 8080

# Run the scheduler service
CMD ["python", "src/scheduler_service.py"]
