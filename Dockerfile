FROM python:3.11-slim

# Detect architecture and install corresponding browser/dependencies
RUN arch=$(dpkg --print-architecture) && \
    if [ "$arch" = "amd64" ]; then \
        # Local Docker (AMD64) -> Install official Google Chrome
        apt-get update && apt-get install -y curl gnupg unzip --no-install-recommends && \
        curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
        apt-get install -y ./google-chrome-stable_current_amd64.deb && \
        rm google-chrome-stable_current_amd64.deb && \
        rm -rf /var/lib/apt/lists/* ; \
    elif [ "$arch" = "arm64" ]; then \
        # Cloud Docker (ARM64) -> Install Chromium and Chromium-driver
        apt-get update && apt-get install -y chromium chromium-driver --no-install-recommends && \
        rm -rf /var/lib/apt/lists/* ; \
    else \
        echo "Unsupported architecture: $arch" && exit 1; \
    fi


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
